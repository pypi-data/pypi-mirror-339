from setuptools import setup, find_packages

setup(
    name="model-manager-client",
    version="0.1.1",
    description="A Python SDK for interacting with the Model Manager gRPC service",
    author="Oscar Ou",
    author_email="oscar.ou@tamaredge.ai",
    packages=find_packages(),
    include_package_data=True,  # 包含非 .py 文件
    package_data={
        "model_manager_client": ["generated/*.py"],  # 包含 gRPC 生成文件
    },
    install_requires=[
        "grpcio",
        "grpcio-tools",
        "pydantic",
        "PyJWT"
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/oscarou1992/model-manager-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
