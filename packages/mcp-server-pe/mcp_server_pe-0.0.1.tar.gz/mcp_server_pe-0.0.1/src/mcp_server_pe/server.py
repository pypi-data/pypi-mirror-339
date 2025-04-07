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

PE_HOST = "https://x-ai.ke.com"


def convert_form_to_schema(form_data: list) -> dict:
    """
    将user_input_form转换为JSON Schema格式

    Args:
        form_data: 输入表单配置列表

    Returns:
        dict: JSON Schema格式的数据结构
    """
    schema = {
        "type": "object",
        "properties": {},
        "required": []
    }

    for field in form_data:
        field_type = list(field.keys())[0]  # 获取字段类型（text-input, number等）
        field_config = field[field_type]    # 获取字段配置

        # 获取通用属性
        field_name = field_config["variable"]
        field_label = field_config["label"]
        is_required = field_config.get("required", False)

        # 创建基础属性结构
        field_schema = {
            "description": field_label
        }

        # 根据不同类型设置特定属性
        if field_type in ["text-input", "paragraph"]:
            field_schema["type"] = "string"
            if "max_length" in field_config:
                field_schema["maxLength"] = field_config["max_length"]

        elif field_type == "number":
            field_schema["type"] = "number"

        elif field_type == "select":
            field_schema["type"] = "string"
            field_schema["enum"] = field_config["options"]

        # 设置默认值（如果有）
        if "default" in field_config and field_config["default"]:
            field_schema["default"] = field_config["default"]

        # 添加到schema中
        schema["properties"][field_name] = field_schema

        # 如果是必填字段，添加到required列表
        if is_required:
            schema["required"].append(field_name)


    return schema


def convert_node_variables_to_schema(node_variables: list) -> dict:
    schema = {
        "type": "object",
        "properties": {},
        "required": []
    }
    for variable in node_variables:
        name = variable["variable"]
        field_schema = {
            "description": variable["label"],
        }
        field_type = variable["type"]
        # 根据不同类型设置特定属性
        if field_type in ["text-input", "paragraph"]:
            field_schema["type"] = "string"
            if "max_length" in variable:
                field_schema["maxLength"] = variable["max_length"]

        elif field_type == "number":
            field_schema["type"] = "number"

        elif field_type == "select":
            field_schema["type"] = "string"
            field_schema["enum"] = variable["options"]

        # 设置默认值（如果有）
        if "default" in variable and variable["default"]:
            field_schema["default"] = variable["default"]
        schema["properties"][name] = field_schema
        is_required = variable.get("required", False)
        if is_required:
            schema["required"].append(name)
    return schema

def get_app_info(api_token: str) -> tuple[str, Tool]:
    host = os.environ.get("PE_HOST", PE_HOST)
    url = f"{host}/v1/app"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = httpx.get(url, headers=headers, timeout=5)
    response.raise_for_status()
    app_info = response.json()
    app_description = app_info["description"]
    app_name = app_info["name"]
    if app_info['mode'] == 'agent-chat':
        user_input_form = app_info["model_config"]["user_input_form"]
        schema = convert_form_to_schema(user_input_form)
        # add default query to agent
        key = "__agent_query_mcp_server"
        query_schema = {
            "type": "string",
            "description": "the question to reply by this tool",
        }
        schema["properties"][key] = query_schema
        schema["required"].append(key)
    elif app_info['mode'] == 'advanced-chat':
        schema = get_workflow_schema(api_token)
        key = "__agent_query_mcp_server"
        query_schema = {
            "type": "string",
            "description": "the question to reply by this tool",
        }
        schema["properties"][key] = query_schema
        schema["required"].append(key)
    elif app_info['mode'] == 'workflow':
        schema = get_workflow_schema(api_token)
    return app_info['mode'], Tool(
        name=app_name,
        description=app_description,
        inputSchema=schema
    )


def get_workflow_schema(api_token: str) -> dict:
    host = os.environ.get("PE_HOST", PE_HOST)
    url = f"{host}/v1/workflow"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = httpx.get(url, headers=headers, timeout=5)
    response.raise_for_status()
    workflow_info = response.json()
    start_node = [node for node in workflow_info['graph']
                  ['nodes'] if node['data']['type'] == 'start']
    if len(start_node) != 1:
        raise ValueError("Workflow must have exactly one start node")
    start_node = start_node[0]
    variables = start_node['data']['variables']
    schema = convert_node_variables_to_schema(variables)
    return schema



async def serve(api_token: str) -> None:
    tool_name_map = {}
    mode, tool = get_app_info(api_token)
    tool_name_map[tool.name] = {
        "api_token": api_token,
        "mode": mode,
    }

    server = Server("mcp-pe-app")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            tool
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

    def call_workflow(api_token,inputs):
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
