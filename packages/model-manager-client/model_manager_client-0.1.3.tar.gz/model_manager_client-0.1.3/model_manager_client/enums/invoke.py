from enum import Enum


class InvokeType(str, Enum):
    """模型调用类型枚举"""
    GENERATION = "generation"
