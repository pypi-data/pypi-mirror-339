"""
AskUserTool

Purpose: Allows the agent to request additional input or clarification from the user.

How it works:
- Takes a question or prompt and presents it to the user
- Returns the user's response back to the agent
- Helps facilitate interactive dialogue when the agent needs more information

Example use cases:
- Clarifying ambiguous requirements
- Getting preferences or choices from the user
- Confirming whether to proceed with an action
- Requesting missing information needed to complete a task
"""

from typing import Optional

from agno.tools import Toolkit
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from sven.cli.console import console


class AskUserInput(BaseModel):
    question: str = Field(
        ..., description="The question or prompt to present to the user"
    )


class UserInputTools(Toolkit):
    name: str = "user_input"
    instructions: str = """
        Use this toolkit when you need additional input or clarification from the user.
        Present a clear question or prompt and the user will provide a response.
        Only use this when you cannot proceed without more information from the user.
    """

    def __init__(self):
        super().__init__(name=self.name, instructions=self.instructions)
        self.console = Console()
        self.register(self.ask_question)
        self.register(self.request_tool)

    def request_tool(
        self,
        tool_name: str,
        tool_description: str,
        input_parameters: str,
        output_description: str,
        example_usage: Optional[str] = None,
        implementation_hints: Optional[str] = None,
    ) -> str:
        """
        Use this tool when user requests you to do something that you can not
        easily do using the existing tools that you have access to.

        Whenever you think that you need an additional tool, ask user.

        Args:
            tool_name (str): The name of the tool you are requesting from the user.
            tool_description (str): A description of the tool you are requesting from the user.
            input_parameters (str): The input parameters of the tool you are requesting from the user.
            output_description (str): The output description of the tool you are requesting from the user.
            example_usage (str): An example usage of the tool you are requesting from the user.
            implementation_hints (str): Hints for the user on how to implement the tool you are requesting from the user.

        Returns:
            str: The user's response containing the requested tool information.
        """
        console.print(
            Panel(
                f"Please add the following tool:\n"
                f"Name: {tool_name}\n"
                f"Description: {tool_description}\n"
                f"Input Parameters: {input_parameters}\n"
                f"Output Description: {output_description}\n"
                f"Example Usage: {example_usage}\n"
                f"Implementation Hints: {implementation_hints}"
            )
        )
        return "Request received"

    def ask_question(self, question: str) -> str:
        """
        Present a question to the user and return their response.

        This method temporarily pauses the agent's output display, shows the question
        to the user in a formatted way, collects their response, and then resumes
        the agent's output display.

        Args:
            question (str): The question or prompt to present to the user

        Returns:
            str: The user's response to the question

        Note:
            This tool should be used when the agent needs additional information
            or clarification that only the user can provide. It creates an
            interactive dialogue between the agent and user.
        """
        console = Console()
        console.print(f"[bold]Agent Question:[/bold] {question}")
        response = Prompt.ask("Response: ")
        return response
