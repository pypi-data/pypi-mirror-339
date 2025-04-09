"""
Authentication command parser and handler for the Sven CLI.
"""

import time
from argparse import Namespace
from typing import Any

import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

from sven.config import settings


def add_auth_parser(subparsers: Any) -> None:
    """Register the 'auth' command with the argument parser."""
    parser = subparsers.add_parser("auth", help="Authenticate with the Sven API")

    # Create subparsers for auth subcommands
    auth_subparsers = parser.add_subparsers(
        dest="auth_command", help="Auth subcommands"
    )

    # Register auth subcommands
    add_register_parser(auth_subparsers)
    add_login_parser(auth_subparsers)

    parser.set_defaults(command="auth")


def add_register_parser(subparsers: Any) -> None:
    """Register the 'register' subcommand for the auth command."""
    parser = subparsers.add_parser("register", help="Register a new user with email")

    parser.add_argument(
        "--email",
        type=str,
        required=True,
        help="Email address to register with",
    )


def add_login_parser(subparsers: Any) -> None:
    """Register the 'login' subcommand for the auth command."""
    parser = subparsers.add_parser("login", help="Login with email")

    parser.add_argument(
        "--email",
        type=str,
        help="Email address to login with",
    )


def handle_auth(args: Namespace) -> int:
    """Handle the 'auth' command for authentication."""
    # Check if an auth subcommand was specified
    if hasattr(args, "auth_command") and args.auth_command:
        if args.auth_command == "register":
            return handle_auth_register(args)
        elif args.auth_command == "login":
            return handle_auth_login(args)

    # If no subcommand specified, show help
    console = Console()
    console.print(
        "[yellow]Please specify an auth subcommand: register or login[/yellow]"
    )
    return 1


def handle_auth_register(args: Namespace) -> int:
    """Handle the 'auth register' command to register a new user."""
    console = Console()

    # Get the base URL from configuration
    base_url = settings.api_url
    email = args.email

    # Make the registration request
    try:
        response = requests.post(
            f"{base_url}/auth/register", params={"email": email, "base_url": base_url}
        )

        if response.status_code == 201:
            console.print(
                Panel(
                    f"[green]Registration initiated![/green]\n\n"
                    f"A verification email has been sent to [bold]{email}[/bold].\n"
                    f"Please check your email and click the verification link to complete registration.",
                    title="Registration",
                )
            )
            return 0
        else:
            console.print(
                Panel(
                    f"[red]Registration failed![/red]\n\n"
                    f"Error: {response.json().get('detail', 'Unknown error')}",
                    title="Registration Error",
                )
            )
            return 1
    except Exception as e:
        console.print(
            Panel(
                f"[red]Registration failed![/red]\n\n" f"Error: {str(e)}",
                title="Registration Error",
            )
        )
        return 1


def handle_auth_login(args: Namespace) -> int:
    """Handle the 'auth login' command to login a user and get an API key."""
    console = Console()

    # Get the base URL from configuration
    base_url = settings.api_url

    # If email is not provided, prompt for it
    email = args.email
    if not email:
        email = Prompt.ask("Enter your email address")

    # Make the login request
    try:
        response = requests.post(
            f"{base_url}/auth/login", params={"email": email, "base_url": base_url}
        )

        if response.status_code == 200:
            console.print(
                Panel(
                    f"A verification email has been sent to [bold]{email}[/bold].\n"
                    f"Please check your email and click the verification link.",
                    title="Login initiated",
                    border_style="green",
                )
            )

            # Ask if the user wants to wait for verification
            wait_for_verification = Prompt.ask(
                "Do you want to wait for email verification?",
                choices=["y", "n"],
                default="y",
            )

            if wait_for_verification.lower() == "y":
                # First, we need to get the verification token
                # This is a bit of a hack, but we'll prompt the user to enter the token from the URL
                console.print(
                    "\nAfter clicking the verification link, please copy the token from the URL and paste it here."
                )
                token = Prompt.ask("Enter the verification token")

                # Poll the server for verification status
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                ) as progress:
                    task = progress.add_task(
                        "Waiting for email verification...", total=None
                    )

                    # Now poll for verification status
                    max_attempts = 60  # 5 minutes (5 seconds * 60)
                    for _ in range(max_attempts):
                        try:
                            status_response = requests.get(
                                f"{base_url}/auth/verification-status/{token}"
                            )
                            status_data = status_response.json()

                            if status_data.get("verified", False):
                                # Verification successful, save the API key
                                api_key = status_data.get("api_key")

                                if api_key:
                                    settings.api_key = api_key
                                    settings.save()

                                    progress.update(task, completed=True)
                                    console.print(
                                        Panel(
                                            f"API key saved to [bold]{settings.config_file}[/bold]",
                                            title="Login successful",
                                            border_style="green",
                                        )
                                    )
                                    return 0
                                else:
                                    progress.update(task, completed=True)
                                    console.print(
                                        Panel(
                                            "[red]Login failed![/red]\n\n"
                                            "No API key received from server.",
                                            title="Login Error",
                                            border_style="red",
                                        )
                                    )
                                    return 1

                            # Wait before polling again
                            time.sleep(5)
                        except Exception as e:
                            progress.update(task, completed=True)
                            console.print(
                                Panel(
                                    f"[red]Login failed![/red]\n\n" f"Error: {str(e)}",
                                    title="Login Error",
                                )
                            )
                            return 1

                    # If we get here, verification timed out
                    progress.update(task, completed=True)
                    console.print(
                        Panel(
                            "[red]Login verification timed out![/red]\n\n"
                            "Please try again later.",
                            title="Login Error",
                        )
                    )
                    return 1
            else:
                console.print(
                    Panel(
                        "[yellow]Login initiated but not verified.[/yellow]\n\n"
                        "Please check your email and click the verification link to complete login.",
                        title="Login",
                    )
                )
                return 0
        else:
            console.print(
                Panel(
                    f"[red]Login failed![/red]\n\n"
                    f"Error: {response.json().get('detail', 'Unknown error')}",
                    title="Login Error",
                )
            )
            return 1
    except Exception as e:
        console.print(
            Panel(
                f"[red]Login failed![/red]\n\n" f"Error: {str(e)}",
                title="Login Error",
            )
        )
        return 1
