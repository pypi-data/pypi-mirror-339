from pydantic import BaseModel
from typing import List, Union, Optional

from model_manager_client.enums import ProviderType, InvokeType


class TextInput(BaseModel):
    type: str = "input_text"  # 默认值
    text: str


class ImageInput(BaseModel):
    type: str = "input_image"  # 默认值
    image_url: str


class UserContext(BaseModel):
    org_id: str
    user_id: str


class ModelRequest(BaseModel):
    model_provider: ProviderType
    invoke_type: InvokeType = InvokeType.GENERATION
    model_name: Optional[str] = None
    input: List[Union[TextInput, ImageInput]]
    stream: bool = False  # 默认值
    instructions: Optional[str] = None
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    timeout: Optional[float] = None
    user_context: UserContext
    priority: Optional[int] = None
