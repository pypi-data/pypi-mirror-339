from typing import Any, Iterator, Optional, Union
from pydantic import BaseModel, ConfigDict


class UsageInfo(BaseModel):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class ChatResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: str  # e.g., "text", "json", "embedding", "stream"
    content: Optional[Any] = None  # 静态输出内容
    usage: Optional[UsageInfo] = None  # tokens / 请求成本等
    stream: Optional[Union[Iterator[str], Any]] = None  # 用于流式响应（同步 or 异步）
    raw_response: Optional[Any] = None  # 模型服务商返回的原始结构
    error: Optional[str] = None
