# DifyPy

Python SDK for Dify API- 简单易用的 Dify API 客户端

## 安装

```bash
pip install difypy
```

## 快速开始

```python
from dify_client import DifyClient

# 初始化客户端
client = DifyClient(
    api_key="your_api_key",
    base_url="https://your-dify-instance.com/v1"
)

# 运行工作流
response = client.workflows.run(
    inputs={"query": "你好"},
    user="user123"
)

# 打印结果
print(response.data)
```

## 功能特性

- 支持同步和异步操作
- 完整的工作流 API 支持
- 文件上传和管理
- 数据集操作
- 错误处理和重试机制
- 速率限制支持

## 文档

详细的 API 文档请参考 [Dify 官方文档](https://docs.dify.ai/)。

## 许可证

MIT 