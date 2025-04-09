import asyncio
import atexit
import json
import logging
import os
import time

import grpc
from typing import Optional, AsyncIterator, Union

import jwt

from .exceptions import ConnectionError, ValidationError
from .schemas import ModelRequest, ModelResponse, TextInput, ImageInput
from .generated import model_service_pb2, model_service_pb2_grpc

logger = logging.getLogger("ModelManagerClient")


# JWT 处理类
class JWTAuthHandler:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def encode_token(self, payload: dict, expires_in: int = 3600) -> str:
        """生成带过期时间的 JWT Token"""
        payload = payload.copy()
        payload["exp"] = int(time.time()) + expires_in
        return jwt.encode(payload, self.secret_key, algorithm="HS256")


class ModelManagerClient:
    def __init__(
            self,
            server_address: Optional[str] = None,
            jwt_secret_key: Optional[str] = None,
            jwt_token: Optional[str] = None,
            default_payload: Optional[dict] = None,
            token_expires_in: int = 3600,
            max_retries: int = 3,  # 最大重试次数
            retry_delay: float = 1.0,  # 初始重试延迟（秒）
    ):
        # 服务端地址
        self.server_address = server_address or os.getenv("MODEL_MANAGER_SERVER_ADDRESS")
        if not self.server_address:
            raise ValueError("Server address must be provided via argument or environment variable.")

        # JWT 配置
        self.jwt_secret_key = jwt_secret_key or os.getenv("MODEL_MANAGER_SERVER_JWT_TOKEN")
        self.jwt_handler = JWTAuthHandler(self.jwt_secret_key)
        self.jwt_token = jwt_token  # 用户传入的 Token（可选）
        self.default_payload = default_payload
        self.token_expires_in = token_expires_in

        # 重试配置
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # 初始化 gRPC 通道
        self.channel: Optional[grpc.aio.Channel] = None
        self.stub: Optional[model_service_pb2_grpc.ModelServiceStub] = None
        self._closed = False

        # 注册进程退出自动关闭
        atexit.register(self._safe_sync_close)

    def _build_auth_metadata(self) -> list:
        if not self.jwt_token and self.jwt_handler:
            self.jwt_token = self.jwt_handler.encode_token(self.default_payload, expires_in=self.token_expires_in)
        return [("authorization", f"Bearer {self.jwt_token}")] if self.jwt_token else []

    async def _ensure_initialized(self):
        """初始化gRPC通道，带重试机制"""
        if self.channel and self.stub:
            return

        retry_count = 0
        while retry_count <= self.max_retries:
            try:
                self.channel = grpc.aio.insecure_channel(self.server_address)
                await self.channel.channel_ready()
                self.stub = model_service_pb2_grpc.ModelServiceStub(self.channel)
                logger.info(f"gRPC channel initialized to {self.server_address}")
                return
            except grpc.FutureTimeoutError as e:
                logger.warning(f"gRPC channel initialization timed out: {str(e)}")
            except grpc.RpcError as e:
                logger.warning(f"gRPC channel initialization failed: {str(e)}")
            except Exception as e:
                logger.warning(f"Unexpected error during channel initialization: {str(e)}")

            retry_count += 1
            if retry_count > self.max_retries:
                raise ConnectionError(f"Failed to initialize gRPC channel after {self.max_retries} retries.")

            # 指数退避：延迟时间 = retry_delay * (2 ^ (retry_count - 1))
            delay = self.retry_delay * (2 ** (retry_count - 1))
            logger.info(f"Retrying connection (attempt {retry_count}/{self.max_retries}) after {delay:.2f}s delay...")
            await asyncio.sleep(delay)

    async def _stream(self, model_request, metadata) -> AsyncIterator[ModelResponse]:
        try:
            async for response in self.stub.Invoke(model_request, metadata=metadata):
                yield ModelResponse(
                    content=response.content,
                    usage=json.loads(response.usage) if response.usage else None,
                    raw_response=json.loads(response.raw_response) if response.raw_response else None,
                    error=response.error or None,
                )
        except grpc.RpcError as e:
            raise ConnectionError(f"gRPC call failed: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Invalid input: {str(e)}")

    async def invoke(self, model_request: ModelRequest) -> Union[ModelResponse, AsyncIterator[ModelResponse]]:
        """
       通用调用模型方法。

        Args:
            model_request: ModelRequest 对象，包含请求参数。

        Yields:
            ModelResponse: 支持流式或非流式的模型响应

        Raises:
            ValidationError: 输入验证失败。
            ConnectionError: 连接服务端失败。
        """
        await self._ensure_initialized()

        if not self.default_payload:
            self.default_payload = {
                "org_id": model_request.user_context.org_id or "",
                "user_id": model_request.user_context.user_id or ""
            }

        # 构造 InputItem 列表
        input_items = []
        for item in model_request.input:
            if isinstance(item, TextInput):
                input_items.append(model_service_pb2.InputItem(
                    text=model_service_pb2.TextInput(
                        type=item.type,
                        text=item.text
                    )
                ))
            elif isinstance(item, ImageInput):
                input_items.append(model_service_pb2.InputItem(
                    image=model_service_pb2.ImageInput(
                        type=item.type,
                        image_url=item.image_url
                    )
                ))
            else:
                raise ValidationError("Invalid input type, must be TextInput or ImageInput.")

        request = model_service_pb2.ModelRequestItem(
            model_provider=model_request.model_provider.value,
            model_name=model_request.model_name or "",
            invoke_type=model_request.invoke_type.value,
            input=model_service_pb2.Input(contents=input_items),
            stream=model_request.stream,
            instructions=model_request.instructions or "",
            max_output_tokens=model_request.max_output_tokens or 0,
            temperature=model_request.temperature or 0.0,
            top_p=model_request.top_p or 0.0,
            timeout=model_request.timeout or 0.0,
            org_id=model_request.user_context.org_id,
            user_id=model_request.user_context.user_id,
            priority=model_request.priority or 0
        )

        metadata = self._build_auth_metadata()

        if model_request.stream:
            return self._stream(request, metadata)
        else:
            async for response in self.stub.Invoke(request, metadata=metadata):
                return ModelResponse(
                    content=response.content,
                    usage=json.loads(response.usage) if response.usage else None,
                    raw_response=json.loads(response.raw_response) if response.raw_response else None,
                    error=response.error or None,
                )

    async def close(self):
        """关闭 gRPC 通道"""
        await self.channel.close()

    def _safe_sync_close(self):
        """进程退出时自动关闭 channel（事件循环处理兼容）"""
        if self.channel and not self._closed:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.close())
                else:
                    loop.run_until_complete(self.close())
            except Exception as e:
                logger.warning(f"gRPC channel close failed at exit: {e}")
