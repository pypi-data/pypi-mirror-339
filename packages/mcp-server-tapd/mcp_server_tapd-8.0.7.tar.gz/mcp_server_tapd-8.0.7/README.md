# TAPD MCP Server

TAPD MCP Server 是一个 Model Context Protocol (MCP) 的实现，用于连接 TAPD（腾讯敏捷产品研发平台）与 AI 编码助手。通过这个服务器，您可以：

* 与 TAPD API 无缝集成，提升开发效率

## System requirements

* uv
* TAPD API Token 公司管理 -> API账号管理 https://open.tapd.cn/document/api-doc/API%E6%96%87%E6%A1%A3/API%E9%85%8D%E7%BD%AE%E6%8C%87%E5%BC%95.html

## Setup Guide
### Install uv
```
brew install uv
# OR
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Configuration and Usage
### Claude Desktop Setup
```
{
  "mcpServers": {
    "mcp-server-tapd": {
      "command": "uvx",
      "args": [
        "mcp-server-tapd",
        "--api-user=your_api_user",
        "--api-password=your_api_password",
        "--api-base-url=https://api.tapd.cn",
        "--tapd-base-url=https://www.tapd.cn"
      ]
    }
  }
}
```

### Cursor IDE Setup
1. Open Cursor Settings
2. Navigate to Features > MCP Servers
3. Click Add new MCP server

For stdio transport:
```
name: mcp-server-tapd
type: command
command: uvx mcp-server-tapd --api-user=your_api_user --api-password=your_api_password --api-base-url=https://api.tapd.cn --tapd-base-url=https://www.tapd.cn
```




