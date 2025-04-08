# mcp-server-pe

使用mcp-server-pe，将PE平台智能体（Agent)、智能体（工作流）、工作流转化为可调用的工具。

## 使用方法：
1. [安装uv](https://docs.astral.sh/uv/getting-started/installation/)
2. 从PE平台获取对应app的调用API密钥
3. 在可以使用mcp server的客户端配置mcp-server-pe.
* cursor配置
```json
{
  "mcpServers": {
    "pe-mcp-server": {
      "command": "uvx",
      "args": [
        "mcp-server-pe",
        "--api-tokens",
        "<Api Key>"
        ],
    }
  }
}
```
可以在一个mcp server中同时配置多个API KEY，使用','分隔