from typing import Any, Iterator, Optional, Union, Dict, List

from pydantic import BaseModel, ConfigDict


class ModelResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    content: Optional[str] = None  # 文本输出内容
    usage: Optional[Dict] = None  # tokens / 请求成本等（JSON）
    stream_response: Optional[Union[Iterator[str], Any]] = None  # 用于流式响应（同步 or 异步）
    raw_response: Optional[Union[Dict, List]] = None  # 模型服务商返回的原始结构（JSON）
    error: Optional[Any] = None
