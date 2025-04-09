import json
from typing import Any, AsyncIterator, Dict, Iterator, List

from agno.models.message import Message
from agno.tools import Toolkit
from agno.tools.function import Function, FunctionCall

from sven.api import ApiClient
from sven.api.schemas.agent import (
    AgentCompletionChunk,
    AgentCompletionRequest,
    AgentCompletionResponse,
    AgentTool,
    Environment,
)


class SvenAgent:
    def __init__(self, persona: str, tools: List[Toolkit]):
        self.persona = persona
        self.tools = tools
        self.api = ApiClient()
        self.tools_by_name: Dict[str, Function] = {}
        for toolkit in self.tools:
            for name, subtool in toolkit.functions.items():
                subtool.process_entrypoint()
                self.tools_by_name[name] = subtool

    def _toolkit_to_agent_tool(self, toolkit: Toolkit) -> AgentTool:
        serializable_functions = []

        for func in toolkit.functions.values():
            func.process_entrypoint()
            # Create a new Function without non-serializable attributes
            serializable_function = Function(
                name=func.name,
                description=func.description,
                parameters=func.parameters,
                strict=func.strict,
            )
            serializable_functions.append(serializable_function)

        return AgentTool(
            name=toolkit.name,
            functions=serializable_functions,
        )

    def execute_tool_locally(self, tool_call: Dict[str, Any]) -> Message:
        """Execute a tool locally and return the result as a Message."""
        from rich.console import Console

        from sven.client.components import MessageView

        console = Console()
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_id = tool_call.get("id")

        console.print(f"\n[bold yellow]Tool call:[/bold yellow] {tool_name}")
        console.print(f"[yellow]Arguments:[/yellow] {json.dumps(tool_args, indent=2)}")

        try:
            if tool_name in self.tools_by_name:
                tool = self.tools_by_name[tool_name]
                func = FunctionCall(function=tool, arguments=tool_args)
                func.execute()
                result = func.result
                response = Message(
                    role="tool",
                    content=result,
                    name=tool_name,
                    tool_call_id=tool_id,
                )
                console.print(MessageView(response))
                return response
            else:
                response = Message(
                    role="tool",
                    content=f"Error: Tool '{tool_name}' not found",
                    name=tool_name,
                    tool_call_id=tool_id,
                )
                console.print(MessageView(response))
                return response
        except Exception as e:
            response = Message(
                role="tool",
                content=f"Error executing tool: {e}",
                name=tool_name,
                tool_call_id=tool_id,
            )
            console.print(MessageView(response))
            return response

    def run(self, messages: List[Message] | str, stream: bool = False):
        if isinstance(messages, str):
            messages = [Message(role="user", content=messages)]

        agent_tools = [self._toolkit_to_agent_tool(tool) for tool in self.tools]

        completion = AgentCompletionRequest(
            model="claude-3-7-sonnet-latest",
            persona=self.persona,
            environment=Environment(working_directory=".", platform="linux"),
            messages=messages,
            tools=agent_tools,
        )
        response = self.api.agent.create_completion(completion, stream=stream)

        if not stream:
            # Check if response has any tool calls and execute them locally
            for message in response.messages:
                if hasattr(message, "tool_calls") and message.tool_calls:
                    for tool_call in message.tool_calls:
                        tool_response = self.execute_tool_locally(tool_call)
                        messages.append(tool_response)

            # Get final response after tool execution
            if any(msg.role == "tool" for msg in messages):
                completion = AgentCompletionRequest(
                    model="claude-3-7-sonnet-latest",
                    persona=self.persona,
                    environment=Environment(working_directory=".", platform="linux"),
                    messages=messages,
                    tools=agent_tools,
                )
                response = self.api.agent.create_completion(completion, stream=stream)

        return response

    async def arun(self, messages: List[Message] | str, stream: bool = False):
        if isinstance(messages, str):
            messages = [Message(role="user", content=messages)]

        agent_tools = [self._toolkit_to_agent_tool(tool) for tool in self.tools]

        completion = AgentCompletionRequest(
            model="claude-3-7-sonnet-latest",
            persona=self.persona,
            environment=Environment(working_directory=".", platform="linux"),
            messages=messages,
            tools=agent_tools,
        )
        response = await self.api.agent.create_completion_async(
            completion, stream=stream
        )

        if not stream:
            # Check if response has any tool calls and execute them locally
            for message in response.messages:
                if hasattr(message, "tool_calls") and message.tool_calls:
                    for tool_call in message.tool_calls:
                        tool_response = self.execute_tool_locally(tool_call)
                        messages.append(tool_response)

            # Get final response after tool execution
            if any(msg.role == "tool" for msg in messages):
                completion = AgentCompletionRequest(
                    model="claude-3-7-sonnet-latest",
                    persona=self.persona,
                    environment=Environment(working_directory=".", platform="linux"),
                    messages=messages,
                    tools=agent_tools,
                )
                response = await self.api.agent.create_completion_async(
                    completion, stream=stream
                )

        return response

    def print_response(
        self,
        messages: List[Message] | str,
        stream: bool = False,
    ):
        from rich.console import Group
        from rich.live import Live
        from rich.panel import Panel
        from rich.status import Status

        if isinstance(messages, str):
            messages = [Message(role="user", content=messages)]

        response_messages: List[Message] = []

        if stream:
            _content = ""
            _tool_calls = []
            with Live(refresh_per_second=10) as live:
                status = Status(
                    "Thinking...", spinner="aesthetic", speed=0.4, refresh_per_second=10
                )
                live.update(status)
                panels = [status]
                chunk_response: Iterator[AgentCompletionChunk] = self.run(
                    messages, stream=stream
                )

                panels = [status]

                tool_panel = Panel(
                    "",
                    title="Tool",
                    border_style="blue",
                )
                panels.append(tool_panel)

                response_panel = Panel(
                    "",
                    title="Response",
                    border_style="blue",
                )
                panels.append(response_panel)

                for chunk in chunk_response:
                    panels = [status]
                    if chunk.event == "ToolCallCompleted":
                        try:
                            live.stop()
                            # Extract tool information from the tools field instead of content
                            if chunk.tools and len(chunk.tools) > 0:
                                tool_info = chunk.tools[0]
                                tool_call = {
                                    "name": tool_info.get("tool_name"),
                                    "args": tool_info.get("tool_args", {}),
                                    "id": tool_info.get("tool_call_id"),
                                }
                                _tool_calls.append(tool_call)

                                # Execute the tool locally
                                tool_response = self.execute_tool_locally(tool_call)
                                response_messages.append(tool_response)

                                tool_panel = Panel(
                                    tool_response.content,
                                    title=f"Tool: {tool_response.name}",
                                    border_style="blue",
                                )
                            else:
                                tool_panel = Panel(
                                    "No tool information available",
                                    title="Tool",
                                    border_style="blue",
                                )
                        finally:
                            live.start()

                    panels.append(tool_panel)

                    if chunk.event in ["RunStarted", "RunResponse", "RunCompleted"]:
                        if chunk.event == "RunStarted":
                            _content = ""
                        if chunk.event == "RunResponse":
                            _content += chunk.content or ""
                        if chunk.event == "RunCompleted" and _content == "":
                            _content = chunk.content or ""

                        response_panel = Panel(
                            _content,
                            title="Response",
                            border_style="blue",
                        )

                    panels.append(response_panel)

                    live.update(Group(*panels))

            # Add the assistant response to messages
            assistant_message = Message(role="assistant", content=_content)
            if _tool_calls:
                assistant_message.tool_calls = _tool_calls
            response_messages.insert(0, assistant_message)

            return AgentCompletionResponse(messages=response_messages)

        with Live(refresh_per_second=10) as live:
            status = Status(
                "Thinking...", spinner="aesthetic", speed=0.4, refresh_per_second=10
            )
            live.update(status)
            panels = [status]
            response: AgentCompletionResponse = self.run(messages, stream=stream)

            for message in response.messages:
                response_panel = Panel(
                    message.content,
                    title=f"{message.role.capitalize()}",
                    border_style="blue",
                )
                panels.append(response_panel)
                live.update(Group(*panels))

            return response

    async def print_response_async(
        self,
        messages: List[Message] | str,
        stream: bool = False,
    ):
        from rich.console import Group
        from rich.live import Live
        from rich.panel import Panel
        from rich.status import Status

        if isinstance(messages, str):
            messages = [Message(role="user", content=messages)]

        if stream:
            _content = ""
            _tool_calls = []
            with Live(refresh_per_second=10) as live:
                status = Status(
                    "Thinking...", spinner="aesthetic", speed=0.4, refresh_per_second=10
                )
                live.update(status)
                panels = [status]
                chunk_response: AsyncIterator[AgentCompletionChunk] = await self.arun(
                    messages, stream=stream
                )

                panels = [status]

                tool_panel = Panel(
                    "",
                    title="Tool",
                    border_style="blue",
                )
                panels.append(tool_panel)

                response_panel = Panel(
                    "",
                    title="Response",
                    border_style="blue",
                )
                panels.append(response_panel)

                async for chunk in chunk_response:
                    panels = [status]

                    if chunk.event == "ToolCallCompleted":
                        # Extract tool information from the tools field instead of content
                        if chunk.tools and len(chunk.tools) > 0:
                            tool_info = chunk.tools[0]
                            tool_call = {
                                "name": tool_info.get("tool_name"),
                                "args": tool_info.get("tool_args", {}),
                                "id": tool_info.get("tool_call_id"),
                            }
                            _tool_calls.append(tool_call)

                            # Execute the tool locally
                            tool_response = self.execute_tool_locally(tool_call)
                            messages.append(tool_response)

                            tool_panel = Panel(
                                tool_response.content,
                                title=f"Tool: {tool_response.name}",
                                border_style="blue",
                            )
                        else:
                            tool_panel = Panel(
                                "No tool information available",
                                title="Tool",
                                border_style="blue",
                            )

                    panels.append(tool_panel)

                    if chunk.event in ["RunStarted", "RunResponse", "RunCompleted"]:
                        if chunk.event == "RunStarted":
                            _content = ""
                        if chunk.event == "RunResponse":
                            _content += chunk.content or ""
                        if chunk.event == "RunCompleted" and _content == "":
                            _content = chunk.content or ""

                        response_panel = Panel(
                            _content,
                            title="Response",
                            border_style="blue",
                        )

                    panels.append(response_panel)

                    live.update(Group(*panels))

            # Add the assistant response to messages
            assistant_message = Message(role="assistant", content=_content)
            if _tool_calls:
                assistant_message.tool_calls = _tool_calls

            return AgentCompletionResponse(messages=[assistant_message])

        with Live(refresh_per_second=10) as live:
            status = Status(
                "Thinking...", spinner="aesthetic", speed=0.4, refresh_per_second=10
            )
            live.update(status)
            panels = [status]
            response: AgentCompletionResponse = await self.arun(messages, stream=stream)

            for message in response.messages:
                response_panel = Panel(
                    message.content,
                    title=f"{message.role.capitalize()}",
                    border_style="blue",
                )
                panels.append(response_panel)
                live.update(Group(*panels))

            return response
