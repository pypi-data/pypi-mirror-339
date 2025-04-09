# TAPD MCP Server

TAPD 是腾讯敏捷研发管理平台，覆盖需求、计划、研发、测试、发布研发全生命周期。支持用自然语言与 TAPD 对话，实现需求、缺陷、任务、迭代等管理。

* 与 TAPD API 无缝集成，提升开发效率

## System requirements

* uv
* TAPD API Token

## Setup Guide
### Install uv
```
brew install uv
# OR
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Get TAPD API Token
Get API tokens from: https://www.tapd.cn/open_platform/open_api_redirect

1、未注册，引导注册 https://www.tapd.cn?from_partner=copilot&source=tapd_operation_copilot
2、已注册但未授权API，引导API配置：
1）登录TAPD，点击进入公司管理
2）进入“API账号管理”，复制API账号和API密钥


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




