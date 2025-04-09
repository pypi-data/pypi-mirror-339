"""Main entry point for the Sven CLI."""

import sys

from sven.cli.main import main


def cli_entry_point():
    """Entry point for the CLI when installed via pip."""
    sys.exit(main())


if __name__ == "__main__":
    cli_entry_point()
