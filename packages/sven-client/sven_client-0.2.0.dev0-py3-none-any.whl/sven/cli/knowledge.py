"""
Knowledge command parser and handler for the Sven CLI.
"""

from argparse import Namespace
from typing import Any

from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.agent import AgentKnowledge
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.knowledge.text import TextKnowledgeBase
from agno.knowledge.url import UrlKnowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from rich.live import Live
from rich.panel import Panel
from rich.status import Status

from sven.cli.console import console
from sven.config import KnowledgeConfig, settings


def add_knowledge_parser(subparsers: Any) -> None:
    """Register the 'knowledge' command with the argument parser."""
    parser = subparsers.add_parser("knowledge", help="Work with the knowledge base")

    # Create subparsers for knowledge subcommands
    knowledge_subparsers = parser.add_subparsers(
        dest="knowledge_command", help="Knowledge subcommands"
    )

    update_parser = knowledge_subparsers.add_parser(
        "update", help="Update a knowledge base"
    )
    update_parser.add_argument(
        "name", type=str, help="Name of the knowledge base to update"
    )
    update_parser.add_argument(
        "--upsert", action="store_true", help="Upsert the knowledge base"
    )
    update_parser.add_argument(
        "--recreate", action="store_true", help="Recreate the knowledge base"
    )
    # Add Knowledge Command
    add_parser = knowledge_subparsers.add_parser("add", help="Add a new knowledge base")
    add_source_group = add_parser.add_mutually_exclusive_group(required=True)
    add_parser.add_argument("name", type=str, help="Name for the knowledge base")
    add_source_group.add_argument("--url", type=str, help="URL to fetch content from")
    add_source_group.add_argument(
        "--path", type=str, help="Path to a file to upload (PDF or Markdown)"
    )

    # Search Knowledge Command
    search_parser = knowledge_subparsers.add_parser(
        "search", help="Search the knowledge base"
    )
    search_parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Maximum number of results to return (default: 5)",
    )
    search_parser.add_argument(
        "name", type=str, help="Name of the knowledge base to search"
    )
    search_parser.add_argument("query", type=str, help="Search query")
    # List Knowledge Command
    knowledge_subparsers.add_parser("list", help="List all knowledge documents")

    # Delete Knowledge Command
    delete_parser = knowledge_subparsers.add_parser(
        "delete", help="Delete a knowledge base"
    )
    delete_parser.add_argument(
        "name", type=str, help="Name of the knowledge base to delete"
    )


def handle_knowledge(args: Namespace) -> int:
    """Handle the 'knowledge' command."""
    # Check if a knowledge subcommand was specified
    if not hasattr(args, "knowledge_command") or not args.knowledge_command:
        console.print(
            "[bold red]Error:[/bold red] No knowledge subcommand specified. "
            "Use 'sven knowledge --help' for more information."
        )
        return 1

    try:
        if args.knowledge_command == "add":
            return handle_knowledge_add(args)
        elif args.knowledge_command == "search":
            return handle_knowledge_search(args)
        elif args.knowledge_command == "list":
            return handle_knowledge_list(args)
        elif args.knowledge_command == "delete":
            return handle_knowledge_delete(args)
        elif args.knowledge_command == "update":
            return handle_knowledge_update(args)
        else:
            console.print(
                f"[bold red]Error:[/bold red] Unknown knowledge subcommand: {args.knowledge_command}"
            )
            return 1
    except Exception as e:
        import traceback

        traceback.print_exc()
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return 1


def _knowledge_base_from_config(config: KnowledgeConfig) -> AgentKnowledge:
    vector_db = LanceDb(
        table_name=config.name,
        uri=settings.sven_dir / "knowledge",
        search_type=SearchType.vector,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    )

    if config.url:
        # If it is a pdf document, use the PDFURLKnowledge class
        if config.url.endswith(".pdf"):
            knowledge_base = PDFUrlKnowledgeBase(urls=[config.url], vector_db=vector_db)
        else:
            knowledge_base = UrlKnowledge(urls=[config.url], vector_db=vector_db)
    elif config.path:
        if config.path.endswith(".pdf"):
            knowledge_base = PDFKnowledgeBase(path=config.path, vector_db=vector_db)
        else:
            knowledge_base = TextKnowledgeBase(
                path=config.path, formats=[".txt", ".md", ".rst"], vector_db=vector_db
            )
    return knowledge_base


def handle_knowledge_add(args: Namespace) -> int:
    """Handle the 'knowledge add' command."""
    knowledge_base: AgentKnowledge = None

    existing_config = settings.get_knowledge_base(args.name)
    if existing_config:
        console.print(
            f"[bold red]Error:[/bold red] Knowledge base already exists: {args.name}"
        )
        return 1

    try:
        knowledge_base = _knowledge_base_from_config(args)
        status = Status(
            "Loading...", spinner="aesthetic", speed=0.4, refresh_per_second=10
        )
        live = Live(status)
        live.start()
        knowledge_base.load()
        live.stop()
        console.print(
            f"[bold green]Successfully added knowledge base {args.name}[/bold green]\n"
        )
        settings.knowledge.append(
            KnowledgeConfig(name=args.name, url=args.url, path=args.path)
        )
        settings.save()
        console.print(
            f"[bold green][dim]Saved config to {settings.config_file}[/dim][/bold green]\n"
        )
        return 0
    except Exception as e:
        console.print(f"[bold red]Error adding knowledge:[/bold red] {str(e)}")
        return 1


def handle_knowledge_update(args: Namespace) -> int:
    """Handle the 'knowledge update' command."""
    try:
        config: KnowledgeConfig = settings.get_knowledge_base(args.name)
        if not config:
            console.print(
                f"[bold red]Error:[/bold red] Knowledge base not found: {args.name}"
            )
            return 1

        knowledge_base = _knowledge_base_from_config(config)
        status = Status(
            "Loading...", spinner="aesthetic", speed=0.4, refresh_per_second=10
        )
        live = Live(status)
        live.start()
        knowledge_base.load()
        live.stop()
        console.print(
            Panel(
                f"[bold green]Successfully updated knowledge base {config.name}[/bold green]\n"
            )
        )
        return 0
    except Exception as e:
        console.print(f"[bold red]Error updating knowledge:[/bold red] {str(e)}")
        return 1


def handle_knowledge_search(args: Namespace) -> int:
    """Handle the 'knowledge search' command."""
    try:
        config: KnowledgeConfig = settings.get_knowledge_base(args.name)
        if not config:
            console.print(
                f"[bold red]Error:[/bold red] Knowledge base not found: {args.name}"
            )
            return 1

        knowledge_base = _knowledge_base_from_config(config)

        with Status(
            "[bold blue]Searching knowledge base...[/bold blue]", spinner="dots"
        ) as status:
            results = knowledge_base.search(
                query=args.query, num_documents=args.max_results
            )

        if not results:
            console.print("[yellow]No results found.[/yellow]")
            return 0

        console.print(
            f'\n[bold green]Found {len(results)} results for query:[/bold green] [italic]"{args.query}"[/italic]\n'
        )

        for i, doc in enumerate(results, 1):
            # Create a panel for each document
            content = (
                doc.content[:500] + "..." if len(doc.content) > 500 else doc.content
            )

            metadata = ""
            if doc.meta_data:
                for key, value in doc.meta_data.items():
                    if key not in ["embedding", "usage"]:
                        metadata += f"\n[dim]{key}:[/dim] {value}"

            score = (
                f"\n[dim]Score:[/dim] {doc.reranking_score}"
                if doc.reranking_score
                else ""
            )

            panel = Panel(
                f"{content}",
                title=f"[bold]Result {i}: {doc.name if doc.name else 'Unnamed Document'}[/bold]",
                subtitle=f"{metadata}{score}",
                border_style="blue",
                expand=False,
            )
            console.print(panel)
            console.print("")  # Add spacing between results

        return 0
    except Exception as e:
        import traceback

        traceback.print_exc()
        console.print(f"[bold red]Error searching knowledge:[/bold red] {str(e)}")
        return 1


def handle_knowledge_list(args: Namespace) -> int:
    """Handle the 'knowledge list' command."""
    try:
        for config in settings.knowledge:
            knowledge_base = _knowledge_base_from_config(config)
            console.print(knowledge_base.name)
        return 0
    except Exception as e:
        console.print(f"[bold red]Error listing knowledge:[/bold red] {str(e)}")
        return 1


def handle_knowledge_delete(args: Namespace) -> int:
    """Handle the 'knowledge delete' command."""
    try:
        settings.knowledge = [
            config for config in settings.knowledge if config.name != args.name
        ]
        settings.save()
        console.print(
            f"[bold green]Successfully deleted knowledge base: {args.name}[/bold green]"
        )
        return 0
    except Exception as e:
        console.print(f"[bold red]Error deleting knowledge:[/bold red] {str(e)}")
        return 1
