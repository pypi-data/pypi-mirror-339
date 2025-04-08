"""
Modulo per l'interfaccia a riga di comando
"""

from enum import Enum

import typer
from rich.console import Console

from .analyzer import scan_project_structure
from .config import ensure_storage, update_settings
from .diagrams import (
    generate_call_graph_diagram,
    generate_hierarchy_diagram,
    generate_task_diagram,
    render_mermaid_diagram,
)
from .tasks import add_task_interactive, display_tasks, edit_task, mark_task_done

app_cli = typer.Typer()
console = Console()


class DiagramType(str, Enum):
    """Tipi di diagrammi supportati"""

    TASKS = "tasks"
    CALLGRAPH = "callgraph"
    HIERARCHY = "hierarchy"


@app_cli.command()
def init():
    """Inizializza un nuovo progetto devnotes"""
    ensure_storage()
    console.print("[bold green]Progetto inizializzato in .project/[/bold green]")


@app_cli.command()
def update():
    """Aggiorna le impostazioni con i valori predefiniti mancanti"""
    update_settings()


@app_cli.command()
def task_list():
    """Mostra tutti i task in formato tabellare"""
    display_tasks()


@app_cli.command()
def task_add_interactive():
    """Aggiunge un nuovo task in modo interattivo"""
    add_task_interactive()


@app_cli.command()
def task_edit():
    """Modifica un task esistente"""
    edit_task()


@app_cli.command()
def task_done(task_id: str):
    """Marca un task come completato"""
    mark_task_done(task_id)


@app_cli.command()
def scan():
    """Scansiona il progetto e genera un diagramma delle funzioni e delle classi"""
    structure = scan_project_structure()
    for filepath, symbols in structure.items():
        console.print(f"[bold yellow]{filepath}[/bold yellow]")
        for sym in symbols:
            console.print(f"  - {sym}")


@app_cli.command()
def diagram(
    type: DiagramType = typer.Argument(..., help="Tipo di diagramma da generare"),
    render: bool = typer.Option(
        False, "--render", "-r", help="Renderizza il diagramma in SVG"
    ),
    open_browser: bool = typer.Option(
        False, "--open", "-o", help="Apri il diagramma nel browser (implica --render)"
    ),
):
    """
    Genera un diagramma in formato Mermaid.

    Tipi di diagrammi supportati:
    - tasks: Diagramma dei task e delle loro dipendenze
    - callgraph: Grafo delle chiamate tra funzioni
    - hierarchy: Diagramma gerarchico di file, classi e funzioni
    """
    output_file = None

    if open_browser:
        render = True

    if type == DiagramType.TASKS:
        output_file = generate_task_diagram()
        console.print(
            f"[bold green]Diagramma dei task generato in {output_file}[/bold green]"
        )
    elif type == DiagramType.CALLGRAPH:
        generate_call_graph_diagram()
        output_file = ".project/call_graph.mmd"
        console.print(f"[bold green]Call graph generato in {output_file}[/bold green]")
    elif type == DiagramType.HIERARCHY:
        generate_hierarchy_diagram()
        output_file = ".project/structure_graph.mmd"
        console.print(
            f"[bold green]Diagramma gerarchico generato in {output_file}[/bold green]"
        )

    if render and output_file:
        render_mermaid_diagram(output_file, open_browser)


@app_cli.command()
def render(
    path: str = typer.Option(".project/call_graph.mmd", help="Path al file .mmd"),
    open_browser: bool = typer.Option(
        True, help="Apri automaticamente il file SVG nel browser"
    ),
):
    """Renderizza un file Mermaid .mmd in SVG usando mmdc"""
    render_mermaid_diagram(path, open_browser)


if __name__ == "__main__":
    app_cli()
