from pydantic import BaseModel
from typing import List, Dict, Optional

from model_manager_client.enums.providers import ProviderType


class ChatMessage(BaseModel):
    role: str
    content: str


class BaseInput(BaseModel):
    provider: ProviderType
    model_name: Optional[str] = None  # 支持动态覆盖模型名
    user_context: Optional[Dict] = None
    priority: int = 1


class ChatInput(BaseInput):
    messages: List[ChatMessage]
    temperature: float = 1.0
    top_p: float = 1.0
    stream: bool = False

    max_tokens: Optional[int] = None
    stop: Optional[List[str]] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None
    extra: Optional[Dict] = None
    org_id: Optional[str] = None
    user_id: Optional[str] = None
