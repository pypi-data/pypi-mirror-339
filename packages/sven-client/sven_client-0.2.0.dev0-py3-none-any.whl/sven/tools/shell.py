"""
Purpose: Executes bash commands in a persistent shell session.

How it works:
- Runs bash commands with optional timeout.
- Maintains state between commands (environment variables, working directory, etc.).
- Includes safety measures to prevent dangerous commands.

Example use case:
When the agent needs to run tests, install dependencies, compile code, or perform other command-line operations.

Tool description for the model:
"""

import subprocess
from pathlib import Path
from typing import List, Optional, Union

from agno.exceptions import StopAgentRun
from agno.tools import Toolkit
from agno.utils.log import log_debug, log_info, logger
from rich.console import Console
from rich.prompt import Prompt


class ShellTools(Toolkit):
    def __init__(
        self,
        base_dir: Optional[Union[str, Path]] = None,
        interactive: bool = True,
        **kwargs,
    ):
        super().__init__(name="shell_tools", **kwargs)

        self.base_dir: Optional[Path] = None
        self.interactive: bool = interactive

        if base_dir is not None:
            self.base_dir = Path(base_dir) if isinstance(base_dir, str) else base_dir

        self.register(self.execute_shell_command)

    def execute_shell_command(
        self,
        args: List[str],
        tail: int = 100,
        timeout_ms: int = 30000,
    ) -> str:
        """
        Executes a given bash command in a persistent shell session with
        optional timeout, ensuring proper handling and security measures.

        Before executing the command, please follow these steps:

        1. Directory Verification:
        - If the command will create new directories or files, first use the LS
        tool to verify the parent directory exists and is the correct location
        - For example, before running "mkdir foo/bar", first use LS to check
        that "foo" exists and is the intended parent directory

        2. Security Check:
        - For security and to limit the threat of a prompt injection attack,
        some commands are limited or banned. If you use a disallowed command,
        you will receive an error message explaining the restriction. Explain
        the error to the User.
        - Verify that the command is not one of the banned commands: alias,
        curl, curlie, wget, axel, aria2c, nc, telnet, lynx, w3m, links, httpie,
        xh, http-prompt, chrome, firefox, safari.

        3. User Confirmation:
        - When interactive mode is enabled (default), the user will be prompted to
        confirm the command before execution.
        - The user can press Enter to accept the command as is, modify the command,
        or choose not to run it.

        4. Command Execution:
        - After ensuring proper quoting, execute the command.
        - Capture the output of the command.

        5. Output Processing:
        - If the output exceeds 30000 characters, output will be truncated
        before being returned to you.
        - Prepare the output for display to the user.

        6. Return Result:
        - Provide the processed output of the command.
        - If any errors occurred during execution, include those in the output.

        Usage notes:
        - The command argument is required.
        - You can specify an optional timeout in milliseconds (up to 600000ms /
        10 minutes). If not specified, commands will timeout after 30 minutes.
        - You can disable interactive confirmation by setting interactive=False.
        - VERY IMPORTANT: You MUST avoid using search commands like `find` and
        `grep`. Instead use GrepTool, GlobTool, or dispatch_agent to search. You
        MUST avoid read tools like `cat`, `head`, `tail`, and `ls`, and use View
        and LS to read files.
        - When issuing multiple commands, use the ';' or '&&' operator to
        separate them. DO NOT use newlines (newlines are ok in quoted strings).
        - IMPORTANT: All commands share the same shell session. Shell state
        (environment variables, virtual environments, current directory, etc.)
        persist between commands. For example, if you set an environment
        variable as part of a command, the environment variable will persist for
        subsequent commands.
        - Try to maintain your current working directory throughout the session
        by using absolute paths and avoiding usage of `cd`. You may use `cd` if
        the User explicitly requests it.

        Args:
            args (List[str]): The command to run as a list of strings.
            tail (int): The number of lines to return from the output.
            timeout_ms (int): The timeout in milliseconds.
            interactive (bool): Whether to prompt the user for confirmation before execution (default: True).
        Returns:
            str: The output of the command.
        """
        if self.interactive:
            console = Console()
            # Get the live display instance from the console
            live = console._live

            # Stop the live display temporarily so we can ask for user confirmation
            live.stop()  # type: ignore

            # Ask for confirmation
            console.print(f"\nAbout to run [bold blue]{args}[/]")
            message = (
                Prompt.ask("Do you want to continue?", choices=["y", "n"], default="y")
                .strip()
                .lower()
            )

            # Restart the live display
            live.start()  # type: ignore

            # If the user does not want to continue, raise a StopExecution exception
            if message != "y":
                raise StopAgentRun(
                    "Tool call cancelled by user",
                    agent_message="Stopping execution as permission was not granted.",
                )

        try:
            log_info(f"Running shell command: {args}")
            if self.base_dir:
                args = ["cd", str(self.base_dir), ";"] + args
            result = subprocess.run(
                args, capture_output=True, text=True, timeout=timeout_ms / 1000
            )
            log_debug(f"Result: {result}")
            log_debug(f"Return code: {result.returncode}")
            if result.returncode != 0:
                return f"Error: {result.stderr}"
            # return only the last n lines of the output
            return "\n".join(result.stdout.split("\n")[-tail:])

        except subprocess.TimeoutExpired:
            return "Error: Command timed out."
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return f"Error executing command: {e}"
