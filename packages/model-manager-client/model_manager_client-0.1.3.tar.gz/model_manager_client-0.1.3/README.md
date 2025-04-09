# Model Manager Client

这是一个用于与 Model Manager gRPC 服务进行交互的 Python SDK。该客户端库提供了简单易用的接口来管理和操作模型。

## 功能特点

- 基于 gRPC 的高性能通信
- 类型安全的数据模型（使用 Pydantic）
- 完整的异常处理
- 简单易用的 API 接口

## 系统要求

- Python 3.8 或更高版本
- 支持的操作系统：跨平台（Windows、Linux、macOS）

## 安装

你可以通过 pip 安装此包：

```bash
pip install model-manager-client
```

## 项目结构

```
├── model_manager_client/
│   ├── generated/          # gRPC 生成的代码
│   ├── schemas/            # 数据模型定义
│   ├── enums/              # 枚举类型定义
│   ├── client.py           # 主要客户端实现
│   ├── exceptions.py       # 自定义异常
│   └── __init__.py
```

## 使用方法

### 基本设置

```python
from model_manager_client import ModelManagerClient

# 创建客户端实例
client = ModelManagerClient(
    server_address="localhost:50051",  # 服务器地址
    jwt_token="your-jwt-token"  # 可选的 JWT 认证令牌
)
```

### 流式调用示例

```python
import asyncio


async def invoke_example():
    from model_manager_client import ModelManagerClient
    from model_manager_client.schemas import ModelRequest, TextInput, UserContext
    from model_manager_client.enums.providers import ProviderType

    # 实例化客户端
    client = ModelManagerClient()

    # 组装请求参数
    request_data = ModelRequest(
        model_provider=ProviderType.OPENAI,  # 选择模型提供商
        input=[
            TextInput(text="你好，请介绍一下你自己。")
        ],
        user_context=UserContext(user_id="testllm", org_id="testllm"),
        stream=True,
    )

    # 发送请求并获取响应
    async for response in client.invoke(request_data):
        if response.error:
            print(f"错误: {response.error}")
        else:
            print(f"响应: {response.content}")
            if response.usage:
                print(f"Token 使用情况: {response.usage}")


# 运行示例
asyncio.run(invoke_example())
```

### 非流式调用示例

```python
import asyncio


async def non_stream_example():
    from model_manager_client import ModelManagerClient
    from model_manager_client.schemas import ModelRequest, TextInput, UserContext
    from model_manager_client.enums.providers import ProviderType

    # 实例化客户端
    client = ModelManagerClient()

    # 组装请求参数
    request_data = ModelRequest(
        model_provider=ProviderType.OPENAI,  # 选择模型提供商
        input=[
            TextInput(text="你好，请介绍一下你自己。")
        ],
        user_context=UserContext(user_id="testllm", org_id="testllm"),
        stream=False,  # 设置为非流式调用
    )

    # 发送请求并获取响应
    response = await client.invoke(request_data)
    if response.error:
        print(f"错误: {response.error}")
    else:
        print(f"响应: {response.content}")
        if response.usage:
            print(f"Token 使用情况: {response.usage}")


# 运行示例
asyncio.run(non_stream_example())
```

### 环境变量配置

你也可以通过环境变量来配置客户端：

```bash
export MODEL_MANAGER_SERVER_ADDRESS="localhost:50051"
export MODEL_MANAGER_SERVER_JWT_TOKEN="your-jwt-token"
```

然后创建客户端时可以不传参数：

```python
from model_manager_client import ModelManagerClient

client = ModelManagerClient()  # 将使用环境变量中的配置
```

## 开发

### 环境设置

1. 创建虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

2. 安装开发依赖：
```bash
pip install -e .
```

### 生成 gRPC 代码

运行以下命令生成 gRPC 相关代码：

```bash
python make_grpc.py
```

## 许可证

MIT License

## 作者

- Oscar Ou (oscar.ou@tamaredge.ai)

## 贡献

欢迎提交 Issue 和 Pull Request！ 