import os
from mcp.types import (
    Tool,
)
import httpx
from pydantic import BaseModel
from pypinyin import lazy_pinyin
import re

PE_HOST = "https://x-ai.ke.com"


class AppToolInfo(BaseModel):
    mode: str
    tool: Tool


def get_app_info(api_token: str) -> AppToolInfo:
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
        schema = extract_tool_schema_from_agent_app(user_input_form)
        # add default query to agent
        key = "__agent_query_mcp_server"
        query_schema = {
            "type": "string",
            "description": "the question to reply by this tool",
        }
        schema["properties"][key] = query_schema
        schema["required"].append(key)
    elif app_info['mode'] == 'advanced-chat':
        schema = extract_tool_schema_from_workflow(api_token)
        key = "__agent_query_mcp_server"
        query_schema = {
            "type": "string",
            "description": "the question to reply by this tool",
        }
        schema["properties"][key] = query_schema
        schema["required"].append(key)
    elif app_info['mode'] == 'workflow':
        schema = extract_tool_schema_from_workflow(api_token)
    return AppToolInfo(
        mode=app_info['mode'],
        tool=Tool(
            name=convert_tool_name(app_name),
            description=app_description,
            inputSchema=schema
        )
    )


def convert_tool_name(name: str) -> str:
    """
    工具名称需转化为符合如下规范的名称
    The name of the function to be called. Must be a-z, A-Z, 0-9,
    or contain underscores and dashes, with a maximum length of 64.
    """
    # 将中文转换为拼音
    if any('\u4e00' <= char <= '\u9fff' for char in name):
        name = '_'.join(lazy_pinyin(name))

    # 将所有非法字符替换为下划线
    name = re.sub(r'[^a-zA-Z0-9\-_]', '_', name)

    # 确保不会有连续的下划线
    name = re.sub(r'_+', '_', name)

    # 去除首尾的下划线
    name = name.strip('_')

    # 如果名称为空，返回默认值
    if not name:
        name = 'unnamed_tool'

    # 确保长度不超过64
    if len(name) > 64:
        name = name[:64].rstrip('_')

    return name


def extract_tool_schema_from_agent_app(form_data: list) -> dict:
    """
    将agent app配置的user_input_form转换为JSON Schema格式

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


def extract_tool_schema_from_workflow(api_token: str) -> dict:
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

    def convert_node_variables_to_schema(node_variables: list) -> dict:
        """
        将start节点变量转换为JSON Schema格式

        Arguments:
            node_variables -- 节点配置

        Returns:
            dict: JSON Schema格式的数据结构
        """
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

    schema = convert_node_variables_to_schema(variables)
    return schema

__all__ = ["get_app_info", "AppToolInfo"]