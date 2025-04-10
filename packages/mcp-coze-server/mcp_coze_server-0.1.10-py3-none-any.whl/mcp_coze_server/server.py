import logging
import os
import sys
from pathlib import Path
from typing import List, Optional, Union, Any, Dict

from cozepy import (
    COZE_CN_BASE_URL,
    AsyncCoze,
    AsyncTokenAuth,
    Message,
    ChatEventType,
    User,
    Workspace,
    Bot,
    Voice,
    File,
    BotKnowledge,
    BotPromptInfo,
)
from cozepy.bots import PluginIdInfo, WorkflowIdInfo, ModelInfoConfig
from mcp.server import FastMCP  # type: ignore
from pydantic import BaseModel  # type: ignore


class Config(BaseModel):
    api_token: str
    api_base: str

    @staticmethod
    def build():
        api_base = os.getenv("COZE_API_BASE") or COZE_CN_BASE_URL
        api_token = os.getenv("COZE_API_TOKEN") or ""

        for idx, val in enumerate(sys.argv):
            if val == "--coze-api-base" and idx + 1 < len(sys.argv):
                api_base = sys.argv[idx + 1]
            elif val == "--coze-api-token" and idx + 1 < len(sys.argv):
                api_token = sys.argv[idx + 1]
            elif val.startswith("--coze-api-base="):
                api_base = val.split("--coze-api-base=")[1]
            elif val.startswith("--coze-api-token="):
                api_token = val.split("--coze-api-token=")[1]

        return Config(
            api_base=api_base,
            api_token=api_token,
        )


class CozeServer(object):
    def __init__(self):
        self.logger = logging.getLogger("mcp-coze-server")
        self.coze = AsyncCoze(auth=AsyncTokenAuth(token=conf.api_token), base_url=conf.api_base)
    async def handle_request(self, method: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """处理其他请求"""
        self.logger.info(f"Received request: {method}")
        return {}

    async def bot_chat(self, bot_id: str, content: str) -> str:
        stream = self.coze.chat.stream(
            bot_id=str(bot_id),
            user_id="coze-mcp-server",
            additional_messages=[Message.build_user_question_text(content)],
        )
        msg = ""
        async for event in stream:
            if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                msg += event.message.content
        return msg

    async def workflow_chat(self, bot_id: str, workflow_id: str, content: str) -> str:
        conversation = await self.coze.conversations.create()
        stream = self.coze.workflows.chat.stream(
            workflow_id=str(workflow_id),
            user_id="coze-mcp-server",
            additional_messages=[Message.build_user_question_text(content)],
            bot_id=bot_id,
            conversation_id=conversation.id,
        )
        msg = ""
        async for event in stream:
            if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                msg += event.message.content
        return msg


mcp = FastMCP("mcp-coze-server")
conf = Config.build()
server = CozeServer()


def wrap_id(model: Union[BaseModel, List[BaseModel]], field: str = "id"):
    if isinstance(model, list):
        res = []
        for item in model:
            v = item.model_dump()
            v[field] = "id:" + v[field]
            res.append(v)
        return res
    v = model.model_dump()
    v[field] = "id:" + v[field]
    return v


def unwrap_id(value: str) -> str:
    if value and value.startswith("id:"):
        return str(value[3:])
    return str(value)


@mcp.tool(description="获取当前用户信息 | Get current user information")
async def get_me() -> User:
    return await server.coze.users.me()


@mcp.tool(description="列出所有工作空间 | List all workspaces")
async def list_workspaces() -> List[Workspace]:
    res = await server.coze.workspaces.list()
    items = [item async for item in res]
    return wrap_id(items)  # type: ignore


@mcp.tool(description="列出工作空间中的机器人 | List bots in workspace")
async def list_bots(workspace_id: str) -> List[Bot]:
    res = await server.coze.bots.list(space_id=unwrap_id(workspace_id))
    items = [item async for item in res]
    return wrap_id(items, "bot_id")  # type: ignore


@mcp.tool(description="获取机器人详情 | Get bot details")
async def retrieve_bot(bot_id: str) -> Bot:
    bot = await server.coze.bots.retrieve(bot_id=unwrap_id(bot_id))
    return wrap_id(bot, "bot_id")  # type: ignore


@mcp.tool(description="在工作空间中创建机器人 | Create bot in workspace")
async def create_bot(
    workspace_id: str,
    name: str,
    description: Optional[str] = None,
    prompt: Optional[str] = None,
    plugin_id_list: Optional[List[str]] = None,
    plugin_id_info_list: Optional[List[PluginIdInfo]] = None,
    workflow_id_list: Optional[List[str]] = None,
    workflow_id_info_list: Optional[List[WorkflowIdInfo]] = None,
    model_info_config: Optional[ModelInfoConfig] = None,
    icon_file_id: Optional[str] = None,
) -> Bot:
    """
    在工作空间中创建机器人 | Create a bot in workspace

    :param workspace_id: 工作空间ID | Workspace ID
    :param name: 机器人名称 | Bot name
    :param description: 机器人描述 | Bot description
    :param prompt: 机器人提示词 | Bot prompt
    :param plugin_id_list: 插件ID列表 | List of plugin IDs
    :param plugin_id_info_list: 插件配置列表 | List of plugin configurations
    :param workflow_id_list: 工作流ID列表 | List of workflow IDs
    :param workflow_id_info_list: 工作流配置列表 | List of workflow configurations
    :param model_info_config: 模型配置 | Model configuration
    :param icon_file_id: 头像文件ID | Avatar file ID
    :return: 机器人信息 | Bot information
    """
    bot = await server.coze.bots.create(
        space_id=unwrap_id(workspace_id),
        name=name,
        description=description,
        prompt_info=None if not prompt else BotPromptInfo(prompt=prompt),
        plugin_id_list=plugin_id_list,
        plugin_id_info_list=plugin_id_info_list,
        workflow_id_list=workflow_id_list,
        workflow_id_info_list=workflow_id_info_list,
        model_info_config=model_info_config,
        icon_file_id=icon_file_id,
    )
    return wrap_id(bot, "bot_id")  # type: ignore


@mcp.tool(description="更新机器人信息 | Update bot information")
async def update_bot(
    bot_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    prompt: Optional[str] = None,
    plugin_id_list: Optional[List[str]] = None,
    plugin_id_info_list: Optional[List[PluginIdInfo]] = None,
    workflow_id_list: Optional[List[str]] = None,
    workflow_id_info_list: Optional[List[WorkflowIdInfo]] = None,
    model_info_config: Optional[ModelInfoConfig] = None,
    icon_file_id: Optional[str] = None,
    knowledge: Optional[BotKnowledge] = None,
) -> None:
    """
    更新机器人配置信息 | Update bot configuration

    :param bot_id: 机器人ID | Bot ID
    :param name: 机器人名称 | Bot name
    :param description: 机器人描述 | Bot description
    :param prompt: 机器人提示词 | Bot prompt
    :param plugin_id_list: 插件ID列表 | List of plugin IDs
    :param plugin_id_info_list: 插件配置列表 | List of plugin configurations
    :param workflow_id_list: 工作流ID列表 | List of workflow IDs
    :param workflow_id_info_list: 工作流配置列表 | List of workflow configurations
    :param model_info_config: 模型配置 | Model configuration
    :param icon_file_id: 头像文件ID | Avatar file ID
    :param knowledge: 知识库配置 | Knowledge base configuration
    """
    await server.coze.bots.update(
        bot_id=unwrap_id(bot_id),
        name=name,
        description=description,
        prompt_info=None if not prompt else BotPromptInfo(prompt=prompt),
        plugin_id_list=plugin_id_list,
        plugin_id_info_list=plugin_id_info_list,
        workflow_id_list=workflow_id_list,
        workflow_id_info_list=workflow_id_info_list,
        model_info_config=model_info_config,
        icon_file_id=icon_file_id,
        knowledge=knowledge,
    )


@mcp.tool(description="发布机器人 | Publish bot")
async def publish_bot(bot_id: str) -> Bot:
    bot = await server.coze.bots.publish(
        bot_id=unwrap_id(bot_id),
    )
    return wrap_id(bot, "bot_id")  # type: ignore


@mcp.tool(description="与机器人对话 | Chat with bot")
async def chat_with_bot(
    bot_id: str,
    content: str,
) -> str:
    return await server.bot_chat(
        bot_id=unwrap_id(bot_id),
        content=content,
    )


@mcp.tool(description="与工作流对话 | Chat with workflow")
async def chat_with_workflow(
    bot_id: str,
    workflow_id: str,
    content: str,
) -> str:
    return await server.workflow_chat(
        bot_id=unwrap_id(bot_id),
        workflow_id=unwrap_id(workflow_id),
        content=content,
    )


@mcp.tool(description="列出所有可用的语音 | List all available voices")
async def list_voices() -> List[Voice]:
    res = await server.coze.audio.voices.list()
    items = [item async for item in res]
    return wrap_id(items, "voice_id")  # type: ignore


@mcp.tool(description="上传单个文件 | Upload single file")
async def upload_file(file_path: str) -> File:
    """
    上传单个文件到 Coze 平台 | Upload a single file to Coze platform

    :param file_path: 文件路径 | File path
    :return: 文件信息 | File information
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在 | File not found: {file_path}")
    
    file = await server.coze.files.upload(path)
    return wrap_id(file)  # type: ignore


@mcp.tool(description="批量上传文件 | Upload multiple files")
async def upload_files(file_paths: List[str]) -> List[File]:
    """
    批量上传文件到 Coze 平台 | Upload multiple files to Coze platform

    :param file_paths: 文件路径列表 | List of file paths
    :return: 文件信息列表 | List of file information
    """
    files = []
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在 | File not found: {file_path}")
        file = await server.coze.files.upload(path)
        files.append(file)
    
    return wrap_id(files)  # type: ignore


@mcp.tool(description="获取文件信息 | Get file information")
async def get_file(file_id: str) -> File:
    """
    获取文件信息 | Get file information

    :param file_id: 文件ID | File ID
    :return: 文件信息 | File information
    """
    file = await server.coze.files.retrieve(file_id=unwrap_id(file_id))
    return wrap_id(file)  # type: ignore


@mcp.tool(description="列出所有文件 | List all files")
async def list_files() -> List[File]:
    """
    列出所有上传的文件 | List all uploaded files

    :return: 文件信息列表 | List of file information
    """
    res = await server.coze.files.list()
    items = [item async for item in res]
    return wrap_id(items)  # type: ignore 