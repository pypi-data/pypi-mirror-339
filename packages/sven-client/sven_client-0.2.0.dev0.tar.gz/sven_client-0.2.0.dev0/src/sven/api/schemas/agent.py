from typing import Any, Dict, List, Optional

from agno.models.message import Message
from agno.tools import Toolkit
from agno.tools.function import Function
from pydantic import BaseModel, Field


class Environment(BaseModel):
    working_directory: str
    platform: str


class AgentTool(BaseModel):
    name: str = Field(..., description="The name of the tool")
    functions: List[Function] = Field(..., description="The functions of the tool")

    def to_toolkit(self) -> Toolkit:
        toolkit = Toolkit(
            name=self.name,
        )

        def placeholder_function(**kwargs):
            return "__client_tool__"

        for f in self.functions:
            function = Function(
                name=f.name,
                description=f.description,
                parameters=f.parameters,
                entrypoint=placeholder_function,
                strict=f.strict,
                skip_entrypoint_processing=True,
                stop_after_tool_call=True,
            )
            toolkit.functions[f.name] = function
        return toolkit


class AgentCompletionRequest(BaseModel):
    model: str = Field(
        default="claude-3-7-sonnet-latest", description="The Claude model to use"
    )
    persona: str = Field(default="coder", description="The persona to use")
    environment: Environment = Field(..., description="The environment")
    tools: List[AgentTool] = Field(default=[], description="The tools to use")
    messages: List[Message] = Field(
        ..., description="The messages to send to the agent"
    )


class AgentCompletionResponse(BaseModel):
    messages: List[Message]


class ToolExecution(BaseModel):
    content: str = Field(..., description="The content of the tool execution")
    tool_call_id: str = Field(..., description="The ID of the tool call")
    tool_name: str = Field(..., description="The name of the tool")
    tool_args: Dict[str, Any] = Field(
        ..., description="The arguments passed to the tool"
    )
    tool_call_error: bool = Field(
        default=False, description="Whether the tool execution resulted in an error"
    )
    metrics: Dict[str, Any] = Field(
        ..., description="The metrics of the tool execution"
    )
    created_at: int = Field(..., description="The created at timestamp")


class AgentCompletionChunk(BaseModel):
    content: Optional[str] = Field(default=None, description="The content of the chunk")
    content_type: str = Field(..., description="The type of the content")
    event: str = Field(..., description="The event")
    model: str = Field(..., description="The model")
    run_id: str = Field(..., description="The run id")
    agent_id: str = Field(..., description="The agent id")
    session_id: str = Field(..., description="The session id")
    created_at: int = Field(..., description="The created at timestamp")
    # Optional fields for RunStarted and RunCompleted events
    tools: Optional[List[Any]] = Field(
        default=None,
        description="Tool executions in the run (for RunStarted and RunCompleted events)",
    )
    messages: Optional[List[Message]] = Field(
        default=None,
        description="Messages in the run (for RunStarted and RunCompleted events)",
    )
