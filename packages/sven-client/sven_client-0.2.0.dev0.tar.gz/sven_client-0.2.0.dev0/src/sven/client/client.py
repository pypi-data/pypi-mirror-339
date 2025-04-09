"""
Command handler for the client that connects to the coder agent API.
"""

import argparse
import json
import os
import traceback
from typing import List

import yaml
from agno.agent.agent import Agent
from agno.models.message import Message
from agno.tools import Toolkit
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from sven.agent.local import LocalAgent
from sven.agent.sven import SvenAgent
from sven.tools.file import FileTools
from sven.tools.shell import ShellTools
from sven.tools.user_input import UserInputTools


class SvenClient:
    def __init__(
        self, persona: str = "search", tools: List[Toolkit] = None, local: bool = False
    ):
        # Initialize with defaults that can be overridden
        self.console = Console()
        self.working_directory = os.getcwd()
        self.persona = persona

        self.client_tools: List[Toolkit] = [
            UserInputTools(),
            FileTools(),
            ShellTools(),
        ] + (tools or [])

        self.agent: Agent = None

        if local:
            self.agent = LocalAgent(tools=self.client_tools)
        else:
            self.agent = SvenAgent(persona=persona, tools=self.client_tools)

        self.client_tools_by_name = {tool.name: tool for tool in self.client_tools}

        self.messages: List[Message] = []

    def load_messages_from_file(self, file_path: str):
        """Load messages from a YAML file containing user/AI message pairs."""

        with open(file_path) as f:
            data = yaml.safe_load(f)

            # Convert user/ai pairs to messages
            messages: List[Message] = []
            for k, v in data.items():
                if k == "user":
                    messages.append(Message(role="user", content=v))
                elif k == "ai":
                    messages.append(Message(role="assistant", content=v))

            print(f"Loaded {len(messages)} messages from {file_path}")
            self.messages = messages

    def run(self, args: argparse.Namespace) -> int:
        """Run the client."""
        # Update instance variables from args
        if hasattr(args, "working_directory") and args.working_directory:
            self.working_directory = args.working_directory
        if hasattr(args, "model") and args.model:
            self.model = args.model
        if hasattr(args, "persona") and args.persona:
            self.persona = args.persona
        if hasattr(args, "messages") and args.messages:
            self.load_messages_from_file(args.messages)

        # Display welcome message
        self.console.print(
            Panel(
                f"[bold]Sven Agent[/bold]\n"
                f"Working directory: [cyan]{self.working_directory}[/cyan]\n"
                f"Persona: [cyan]{self.persona}[/cyan]\n"
                f"Tools: [cyan]{', '.join(tool.name for tool in self.client_tools)}[/cyan]",
                title="Welcome",
                border_style="green",
            )
        )

        self.console.print(
            "[bold]Type your messages below. Press Ctrl+C to exit.[/bold]"
        )

        self.console.print(
            "[dim]Available commands: [/dim]"
            "[dim]/quit[/dim][dim], [/dim]"
            "[dim]/exit[/dim][dim], [/dim]"
            "[dim]/clear[/dim][dim], [/dim]"
            "[dim]/messages[/dim][dim], [/dim]"
            "[dim]/models[/dim]"
        )

        def handle_command(user_message):
            command = user_message.strip().lower()
            if command in ["/exit", "/quit"]:
                raise KeyboardInterrupt()

            if command in ["/messages"]:
                dicts = [message.model_dump() for message in self.messages]
                with open("messages.txt", "w") as f:
                    f.write(json.dumps(dicts))
                self.console.print(f"Saved {len(dicts)} messages to messages.txt")
                self.console.print(dicts)
                return 1

            if command in ["/clear"]:
                self.messages = []
                return 1
            return 0

        def read_user_input():
            user_message = Prompt.ask("\n[bold blue]You:[/bold blue] ")

            if handle_command(user_message):
                return 0

            self.messages.append(Message(role="user", content=user_message))
            return 1

        def process_chunk(chunk):
            self.console.print(Markdown(chunk.content))

        try:
            while True:
                # Get user input
                if not read_user_input():
                    continue

                self.agent.print_response(messages=self.messages, stream=True)
                # for response in self.agent.run(
                #    messages=self.messages, stream=True
                # ):
                #    self.console.print(response)
                #    self.messages.extend(response.messages)

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Session terminated by user[/yellow]")
        except Exception as e:
            traceback.print_exc()
            self.console.print(f"[bold red]Error during session: {str(e)}[/bold red]")
            return 1

        return 0

    # The execute_tool_locally method has been moved to SvenAgent class
