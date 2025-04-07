import os

import grpc
from typing import List, Iterator, Optional
from .exceptions import ConnectionError, ValidationError
from .schemas.inputs import ChatInput
from .schemas.outputs import ChatResponse, UsageInfo
from .generated import model_service_pb2, model_service_pb2_grpc


class ModelManagerClient:
    def __init__(self, server_address: Optional[str] = None, jwt_token: Optional[str] = None):
        self.server_address = server_address or os.getenv("MODEL_MANAGER_SERVER_ADDRESS")
        self.jwt_token = jwt_token or os.getenv("MODEL_MANAGER_SERVER_JWT_TOKEN")
        self.channel = grpc.aio.insecure_channel(self.server_address)
        self.stub = model_service_pb2_grpc.ModelServiceStub(self.channel)

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
                user=input_data.user or "",
                user_id=input_data.user_id or "",
                org_id=input_data.org_id or "",
                extra=input_data.extra or {},
            )

            # 添加认证元数据（如果提供 JWT）
            metadata = [("authorization", f"Bearer {self.jwt_token}")] if self.jwt_token else []

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
                        user=i.user or "",
                        user_id=i.user_id or "",
                        org_id=i.org_id or "",
                        extra=i.extra or {},
                    ) for i in inputs
                ]
            )

            # 添加认证元数据（如果提供 JWT）
            metadata = [("authorization", f"Bearer {self.jwt_token}")] if self.jwt_token else []

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
