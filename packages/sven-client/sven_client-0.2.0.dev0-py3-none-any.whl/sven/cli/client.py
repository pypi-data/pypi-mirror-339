"""
Client command parser and handler for the Sven CLI.
"""

from argparse import Namespace
from datetime import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from sven.api import ApiClient
from sven.client.client import SvenClient
from sven.config import settings


def add_client_parser(subparsers: Any) -> None:
    """Register the 'client' command with the argument parser."""
    parser = subparsers.add_parser("client", help="Connect to a coder agent API server")

    # Create subparsers for client subcommands
    client_subparsers = parser.add_subparsers(
        dest="client_command", help="Client subcommands"
    )

    # Register client subcommands
    add_list_models_parser(client_subparsers)

    # Add configuration file option
    parser.add_argument(
        "--config",
        type=str,
        help="Path to a configuration file (.sven.yml)",
    )

    # Add general client arguments (these will override config file values)
    parser.add_argument(
        "--working-directory",
        type=str,
        help="Working directory for the agent (default: current directory)",
    )

    parser.add_argument(
        "--messages",
        type=str,
        help="Path to a YAML file containing human/AI message pairs",
    )

    # Whether to run local agent or remote agent
    parser.add_argument(
        "--local",
        action="store_true",
        help="Run the agent locally (default: remote)",
    )

    parser.add_argument(
        "--model",
        type=str,
        help="Model to use (default from config: claude-3-7-sonnet-latest)",
    )

    parser.add_argument(
        "--persona",
        type=str,
        choices=[
            "blogger",
            "ceo",
            "coder",
            "assistant",
            "rubric-evaluator",
        ],
        help="Persona to use (default from config: coder)",
    )

    parser.set_defaults(command="client")


def add_list_models_parser(subparsers: Any) -> None:
    """Register the 'list-models' subcommand for the client command."""
    subparsers.add_parser("list-models", help="List all available models on the server")


def handle_client(args: Namespace) -> int:
    """Handle the 'client' command to connect to the coder agent API."""
    # Check if a client subcommand was specified
    if hasattr(args, "client_command") and args.client_command:
        if args.client_command == "list-models":
            return handle_client_list_models(args)

    # Default client behavior
    client = SvenClient(local=args.local)
    client.run(args)

    return 0


def handle_client_list_models(args: Namespace) -> int:
    """Handle the 'client list-models' command to list all available models."""
    console = Console()

    # Initialize client API
    api_url = settings.api_url
    api_key = settings.api_key
    client = ApiClient(api_url, api_key)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Fetching available models...", total=None)

        try:
            models = client.list_models()
            progress.update(task, completed=True)

            if not models:
                console.print(
                    Panel(
                        "[yellow]No models available or unable to fetch models from the server.[/yellow]",
                        title="Available Models",
                    )
                )
                return 1

            # Display models in a table
            console.print("\n[bold]Available Models:[/bold]")

            table = Table(show_header=True)
            table.add_column("Model ID", style="cyan")
            table.add_column("Owner", style="green")
            table.add_column("Created", style="yellow")

            for model in models:
                if isinstance(model, dict):
                    model_id = model.get("id", "Unknown")
                    owner = model.get("owned_by", "N/A")

                    # Format created timestamp if available
                    created_timestamp = model.get("created")
                    created_date = "N/A"
                    if created_timestamp:
                        try:
                            created_date = datetime.fromtimestamp(
                                created_timestamp
                            ).strftime("%Y-%m-%d")
                        except (ValueError, TypeError):
                            pass

                    table.add_row(model_id, owner, created_date)
                elif isinstance(model, str):
                    # If the model is just a string (model ID)
                    table.add_row(model, "N/A", "N/A")
                else:
                    # Try to convert to string as fallback
                    table.add_row(str(model), "N/A", "N/A")

            console.print(table)

            console.print(
                "\n[green]Use the model ID with the --model parameter when starting the client.[/green]"
            )
            return 0

        except Exception as e:
            progress.update(task, completed=True)
            console.print(
                Panel(
                    f"[red]Failed to list models![/red]\n\n" f"Error: {str(e)}",
                    title="Error",
                )
            )
            return 1
