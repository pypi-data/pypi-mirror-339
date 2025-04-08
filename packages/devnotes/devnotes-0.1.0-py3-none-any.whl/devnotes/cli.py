"""
Modulo per l'interfaccia a riga di comando
"""

import typer
from rich.console import Console

from .config import ensure_storage, update_settings
from .tasks import display_tasks, add_task_interactive, edit_task, mark_task_done
from .analyzer import scan_project_structure
from .diagrams import (
    generate_task_diagram, render_mermaid_diagram, 
    generate_call_graph_diagram, generate_hierarchy_diagram
)

app_cli = typer.Typer()
console = Console()


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
def diagram_generate():
    """Genera un diagramma in formato Mermaid basato sui task"""
    output_file = generate_task_diagram()
    console.print(f"[bold green]Diagramma generato in {output_file}[/bold green]")


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
def diagram_callgraph():
    """Genera un file Mermaid .mmd con il call graph delle funzioni del progetto"""
    generate_call_graph_diagram()


@app_cli.command()
def diagram_render(
        path: str = typer.Option(".project/call_graph.mmd", help="Path al file .mmd"),
        open_browser: bool = typer.Option(True, help="Apri automaticamente il file SVG nel browser")
):
    """Renderizza un file Mermaid .mmd in SVG usando mmdc"""
    render_mermaid_diagram(path, open_browser)


@app_cli.command()
def diagram_hierarchy():
    """Genera un diagramma gerarchico Mermaid con file, classi e funzioni"""
    generate_hierarchy_diagram()


if __name__ == "__main__":
    app_cli()