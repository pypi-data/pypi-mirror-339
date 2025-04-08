import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)
import httpx
from httpx_sse import connect_sse
import json
from mcp_server_pe.schema_extract import get_app_info

PE_HOST = "https://x-ai.ke.com"


async def serve(api_tokens: str) -> None:
    tool_name_map = {}
    for api_token in api_tokens.split(","):
        app_info = get_app_info(api_token)
        tool_name_map[app_info.tool.name] = {
            "api_token": api_token,
            "mode": app_info.mode,
            "tool": app_info.tool
        }

    server = Server("mcp-pe-app")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            app_info['tool']
            for app_info in tool_name_map.values()
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name not in tool_name_map:
            raise ValueError(f"Unknown tool: {name}")
        api_token = tool_name_map[name]["api_token"]
        mode = tool_name_map[name]["mode"]
        if mode == 'agent-chat':
            query = arguments.pop("__agent_query_mcp_server")
            answer = call_agent_chat(api_token, query, arguments)
            return [TextContent(type="text", text=answer)]
        elif mode == 'advanced-chat':
            query = arguments.pop("__agent_query_mcp_server")
            answer = call_advanced_chat(api_token, query, arguments)
            return [TextContent(type="text", text=answer)]
        elif mode == 'workflow':
            answer = call_workflow(api_token, arguments)
            return [TextContent(type="text", text=answer)]
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def call_agent_chat(api_token, query, inputs):
        body = {
            "query": query,
            "user": "mcp_request",
            "inputs": inputs,
            "response_mode": "streaming",
        }
        host = os.environ.get("PE_HOST", PE_HOST)
        url = f"{host}/v1/chat-messages"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "invoke_from": "mcp_server"
        }
        with httpx.Client(timeout=60) as client:
            answer = ""
            with connect_sse(client, "POST", url, headers=headers, json=body,
                             timeout=60) as event_source:
                for sse in event_source.iter_sse():
                    if sse.event == 'message':
                        data = json.loads(sse.data)
                        if data["event"] == "agent_message":
                            answer += data["answer"]
            return answer

    def call_advanced_chat(api_token, query, inputs):
        body = {
            "query": query,
            "user": "mcp_request",
            "inputs": inputs,
            "response_mode": "streaming",
        }
        host = os.environ.get("PE_HOST", PE_HOST)
        url = f"{host}/v1/chat-messages"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "invoke_from": "mcp_server"
        }
        with httpx.Client(timeout=60) as client:
            answer = ""
            with connect_sse(client, "POST", url, headers=headers, json=body,
                             timeout=60) as event_source:
                for sse in event_source.iter_sse():
                    if sse.event == 'message':
                        data = json.loads(sse.data)
                        if data["event"] == "message":
                            answer += data["answer"]
            return answer

    def call_workflow(api_token, inputs):
        body = {
            "user": "mcp_request",
            "inputs": inputs,
            "response_mode": "blocking",
        }
        host = os.environ.get("PE_HOST", PE_HOST)
        url = f"{host}/v1/workflows/run"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "invoke_from": "mcp_server"
        }
        response = httpx.post(url, headers=headers, json=body, timeout=120)
        response.raise_for_status()
        data = response.json()
        if data['data']['error']:
            raise ValueError(data['data']['error'])
        outputs = data['data']["outputs"]
        return json.dumps(outputs, ensure_ascii=False)

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
