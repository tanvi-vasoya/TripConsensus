from rich.console import Console
from rich.pretty import Pretty
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich import print_json

console = Console()


def info(message: str):
    console.print(f"[bold cyan]ℹ {message}[/bold cyan]")


def success(message: str):
    console.print(f"[bold green]✓ {message}[/bold green]")


def warning(message: str):
    console.print(f"[bold yellow]⚠ {message}[/bold yellow]")


def error(message: str):
    console.print(f"[bold red]✗ {message}[/bold red]")


def pretty(obj):
    console.print(Pretty(obj, expand_all=True))


def json(data):
    import json
    print_json(json.dumps(data, default=str))


def panel(title: str, message: str, style: str = "green"):
    console.print(
        Panel.fit(
            message,
            title=title,
            border_style=style,
        )
    )


def table(title: str, rows: list[tuple[str, str]]):
    t = Table(title=title)
    t.add_column("Field", style="cyan", no_wrap=True)
    t.add_column("Value", style="green")

    for field, value in rows:
        t.add_row(field, str(value))

    console.print(t)