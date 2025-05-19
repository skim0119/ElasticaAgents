import json
import re
from typing import Iterable, List, Type

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionContentPartParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartRefusalParam,
    ChatCompletionMessage,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolParam,
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
)
from mcp.types import (
    CallToolRequestParams,
    CallToolRequest,
    CallToolResult,
    EmbeddedResource,
    ImageContent,
    ModelPreferences,
    TextContent,
    TextResourceContents,
)

from mcp_agent.workflows.llm.augmented_llm import (
    AugmentedLLM,
    ModelT,
    MCPMessageParam,
    MCPMessageResult,
    ProviderToMCPConverter,
    RequestParams,
)
from mcp_agent.logging.logger import get_logger
from mcp_agent.workflows.llm.augmented_llm_openai import *


class OpenAIAugmentedLLMWithImage(OpenAIAugmentedLLM):
    """
    The basic building block of agentic systems is an LLM enhanced with augmentations
    such as retrieval, tools, and memory provided from a collection of MCP servers.
    This implementation uses OpenAI's ChatCompletion as the LLM.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def generate_str(
        self,
        message,
        request_params: RequestParams | None = None,
    ):
        """
        Process a query using an LLM and available tools.
        The default implementation uses OpenAI's ChatCompletion as the LLM.
        Override this method to use a different LLM.
        """

        #messages = []
        # Augment message with image
        #messages.append(ChatCompletionUserMessageParam(role="user", content=message))
        return super().generate_str(
            message=message,
            request_params=request_params,
         )
