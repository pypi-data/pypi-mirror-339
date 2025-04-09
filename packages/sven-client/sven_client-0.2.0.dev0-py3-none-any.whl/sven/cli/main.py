#!/usr/bin/env python3
"""
Sven CLI - A command line utility for agent automation.
"""

import argparse
import logging
import sys
import warnings
from typing import List, Optional

from dotenv import load_dotenv

from sven.cli.auth import add_auth_parser, handle_auth
from sven.cli.client import add_client_parser, handle_client
from sven.cli.knowledge import add_knowledge_parser, handle_knowledge
from sven.cli.tools import add_tool_parser, handle_tool

# Configure logging
logging.basicConfig(level=logging.INFO)

# Suppress specific loggers
for logger_name in ["httpx", "httpcore", "langchain", "langchain_core"]:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

# Suppress LangChain beta warnings
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the application."""
    if args is None:
        args = sys.argv[1:]

    # Create the main parser with all subparsers
    parser = create_main_parser()

    # Parse arguments
    parsed_args = parser.parse_args(args)

    # Handle version command
    if hasattr(parsed_args, "version") and parsed_args.version:
        from sven import __version__

        print(f"Sven version {__version__}")
        return 0

    # Handle debug mode globally
    if hasattr(parsed_args, "debug") and parsed_args.debug:
        # Configure more verbose logging for debug mode
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.INFO)

    # If no command was specified, use client as default
    if not hasattr(parsed_args, "command") or not parsed_args.command:
        return handle_client(parsed_args)

    # Import the command handler
    if parsed_args.command == "tools":
        return handle_tool(parsed_args)
    elif parsed_args.command == "client":
        return handle_client(parsed_args)
    elif parsed_args.command == "knowledge":
        return handle_knowledge(parsed_args)
    elif parsed_args.command == "auth":
        return handle_auth(parsed_args)
    else:
        parser.print_help()
        return 1


class DotNotationArgumentParser(argparse.ArgumentParser):
    """Custom ArgumentParser that allows command.subcommand notation for commands."""

    def parse_args(self, args=None, namespace=None):
        """Parse arguments, expanding dot notation."""
        if args:
            # Handle dot notation by splitting commands
            for i, arg in enumerate(args):
                if arg.startswith("-") or i == 0:
                    continue

                if "." in arg and not arg.startswith("-"):
                    parts = arg.split(".")
                    args[i] = parts[0]
                    args[i + 1 : i + 1] = parts[1:]

        return super().parse_args(args, namespace)


def create_main_parser() -> DotNotationArgumentParser:
    """Create the main parser with all subparsers."""
    parser = DotNotationArgumentParser(
        prog="sven",
        description="Sven CLI - A command line utility for agent automation.",
    )

    # Add global arguments
    parser.add_argument(
        "--version", action="store_true", help="Show version information and exit"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode for detailed logging"
    )

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add parsers for each command
    add_tool_parser(subparsers)
    add_client_parser(subparsers)
    add_knowledge_parser(subparsers)
    add_auth_parser(subparsers)

    return parser


if __name__ == "__main__":
    sys.exit(main())
