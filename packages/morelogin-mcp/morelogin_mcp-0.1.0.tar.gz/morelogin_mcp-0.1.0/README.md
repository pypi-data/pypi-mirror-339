# MoreLogin MCP API

这是一个基于 MoreLogin API 的 MCP 协议兼容实现，允许通过统一的 MCP 接口访问 MoreLogin 的功能。

## 功能特点

- 支持所有主要的 MoreLogin API 功能
- 符合 MCP 协议规范
- 异步处理请求
- 完整的错误处理
- 类型安全的请求和响应

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install morelogin-mcp
```

### 从源码安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/morelogin-mcp.git
cd morelogin-mcp
```

2. 安装依赖：
```bash
pip install -r requirements.txt
pip install -e .
```

## 使用方法

### 作为独立服务运行

1. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 MoreLogin API 密钥
```

2. 启动服务：
```bash
python -m morelogin_mcp.main
```

### 在 Cursor 中使用

1. 安装包：
```bash
pip install morelogin-mcp
```

2. 在您的代码中导入：
```python
from morelogin_mcp import MoreLoginClient, MCPHandler

# 创建客户端
client = MoreLoginClient(api_key="your_api_key")

# 创建处理器
handler = MCPHandler(client)

# 处理 MCP 请求
result = await handler.handle_request("create_profile", {
    "name": "测试配置文件",
    "browser": "chrome",
    "os": "windows"
})
```

### 发送 MCP 请求示例

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "create_profile",
    "params": {
      "name": "测试配置文件",
      "browser": "chrome",
      "os": "windows"
    }
  }'
```

## API 文档

### 支持的 MCP 方法

- `create_profile`: 创建浏览器配置文件
- `get_profile`: 获取浏览器配置文件
- `update_profile`: 更新浏览器配置文件
- `delete_profile`: 删除浏览器配置文件
- `create_proxy`: 创建代理
- `get_proxy`: 获取代理信息
- `update_proxy`: 更新代理
- `delete_proxy`: 删除代理
- `create_group`: 创建分组
- `get_group`: 获取分组信息
- `update_group`: 更新分组
- `delete_group`: 删除分组

## 开发

1. 安装开发依赖：
```bash
pip install -r requirements.txt
pip install -e .
```

2. 运行测试：
```bash
# TODO: 添加测试命令
```

## 发布到 MCP 网站

1. 构建发布包：
```bash
python setup.py sdist bdist_wheel
```

2. 上传到 PyPI：
```bash
twine upload dist/*
```

3. 在 MCP 网站上注册您的服务：
   - 提供服务的名称和描述
   - 提供 API 文档
   - 提供示例代码
   - 提供测试端点

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT 