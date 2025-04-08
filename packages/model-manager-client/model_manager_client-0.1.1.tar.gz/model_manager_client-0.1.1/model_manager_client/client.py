import logging
import os
import time

import grpc
from typing import List, Iterator, Optional

import jwt

from .exceptions import ConnectionError, ValidationError
from .schemas.inputs import ChatInput
from .schemas.outputs import ChatResponse, UsageInfo
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
    ):
        # 服务端地址
        self.server_address = server_address or os.getenv("MODEL_MANAGER_SERVER_ADDRESS")

        # JWT 配置
        self.jwt_secret_key = jwt_secret_key or os.getenv("MODEL_MANAGER_SERVER_JWT_TOKEN")
        self.jwt_handler = JWTAuthHandler(self.jwt_secret_key)
        self.jwt_token = jwt_token  # 用户传入的 Token（可选）
        self.default_payload = default_payload
        self.token_expires_in = token_expires_in

        # 初始化 gRPC 通道
        self.channel = None  # grpc.aio.insecure_channel(self.server_address)
        self.stub = None  # model_service_pb2_grpc.ModelServiceStub(self.channel)

    def _build_auth_metadata(self) -> list:
        if not self.jwt_token and self.jwt_handler:
            self.jwt_token = self.jwt_handler.encode_token(self.default_payload, expires_in=self.token_expires_in)
        return [("authorization", f"Bearer {self.jwt_token}")] if self.jwt_token else []

    async def _build_channel(self):
        try:
            logger.info(f"Building gRPC channel to {self.server_address}")
            self.channel = grpc.aio.insecure_channel(self.server_address)
            # 等待通道就绪
            await self.channel.channel_ready()  # 异步等待通道连接
            self.stub = model_service_pb2_grpc.ModelServiceStub(self.channel)
            logger.info("gRPC channel initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize gRPC channel to {self.server_address}: {e}")
            raise ConnectionError(f"Failed to initialize gRPC channel: {e}")

    async def chat(self, input_data: ChatInput) -> Iterator[ChatResponse]:
        """
        流式调用 Chat 方法。

        Args:
            input_data: ChatInput 对象，包含请求参数。

        Yields:
            ChatResponse: 流式返回的响应对象。

        Raises:
            ValidationError: 输入验证失败。
            ConnectionError: 连接服务端失败。
        """
        try:
            # 组装用户信息
            if not self.default_payload:
                self.default_payload = {
                    "org_id": input_data.org_id or "",
                    "user_id": input_data.user_id or ""
                }
            if not self.channel:  # 仅在未初始化时构建通道
                await self._build_channel()  # 使用 await 调用异步方法

            # 构建 gRPC 请求
            request = model_service_pb2.ChatInputItem(
                provider=input_data.provider,
                model_name=input_data.model_name or "",
                priority=input_data.priority,
                messages=[model_service_pb2.ChatMessage(role=m.role, content=m.content) for m in input_data.messages],
                temperature=input_data.temperature,
                top_p=input_data.top_p,
                stream=input_data.stream,
                max_tokens=input_data.max_tokens or 0,
                stop=input_data.stop or [],
                logit_bias=input_data.logit_bias or {},
                # user=input_data.user or "",
                extra=input_data.extra or {},
            )

            # 添加认证元数据
            metadata = self._build_auth_metadata()

            # 调用 gRPC 服务
            async for response in self.stub.Chat(request, metadata=metadata):
                yield ChatResponse(
                    type=response.type,
                    content=response.content,
                    usage=UsageInfo(
                        prompt_tokens=response.usage.prompt_tokens,
                        completion_tokens=response.usage.completion_tokens,
                        total_tokens=response.usage.total_tokens,
                    ),
                    raw_response=response.raw_response,
                    error=response.error or None,
                )
        except grpc.RpcError as e:
            raise ConnectionError(f"gRPC call failed: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Invalid input: {str(e)}")

    async def batch_chat(self, inputs: List[ChatInput]) -> List[ChatResponse]:
        """
        批量调用 BatchChat 方法。

        Args:
            inputs: List[ChatInput]，包含多个请求参数。

        Returns:
            List[ChatResponse]: 批量返回的响应列表。

        Raises:
            ValidationError: 输入验证失败。
            ConnectionError: 连接服务端失败。
        """
        try:
            # 组装用户信息
            if not self.default_payload and inputs:
                self.default_payload = {
                    "org_id": inputs[0].org_id or "",
                    "user_id": inputs[0].user_id or ""
                }
            if not self.channel:  # 仅在未初始化时构建通道
                await self._build_channel()  # 使用 await 调用异步方法

            # 构建 gRPC 请求
            request = model_service_pb2.ChatRequest(
                items=[
                    model_service_pb2.ChatInputItem(
                        provider=i.provider,
                        model_name=i.model_name or "",
                        priority=i.priority,
                        messages=[model_service_pb2.ChatMessage(role=m.role, content=m.content) for m in i.messages],
                        temperature=i.temperature,
                        top_p=i.top_p,
                        stream=i.stream,
                        max_tokens=i.max_tokens or 0,
                        stop=i.stop or [],
                        logit_bias=i.logit_bias or {},
                        # user=i.user or "",
                        extra=i.extra or {},
                    ) for i in inputs
                ]
            )

            # 添加认证元数据
            metadata = self._build_auth_metadata()

            # 调用 gRPC 服务
            response = await self.stub.BatchChat(request, metadata=metadata)
            return [
                ChatResponse(
                    type=item.type,
                    content=item.content,
                    usage=UsageInfo(
                        prompt_tokens=item.usage.prompt_tokens,
                        completion_tokens=item.usage.completion_tokens,
                        total_tokens=item.usage.total_tokens,
                    ),
                    raw_response=item.raw_response,
                    error=item.error or None,
                ) for item in response.items
            ]
        except grpc.RpcError as e:
            raise ConnectionError(f"gRPC call failed: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Invalid input: {str(e)}")

    async def close(self):
        """关闭 gRPC 通道"""
        await self.channel.close()
