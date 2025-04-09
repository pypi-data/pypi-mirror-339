"""
Schema definitions for the API
"""

from .inputs import TextInput, ImageInput, UserContext, ModelRequest
from .outputs import ModelResponse

__all__ = [
    # Model Inputs
    "TextInput",
    "ImageInput",
    "UserContext",
    "ModelRequest",
    # Model Outputs
    "ModelResponse",
]
