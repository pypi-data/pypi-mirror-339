"""
Modulo per la generazione e gestione dei diagrammi
"""

import os
import subprocess

from rich.console import Console

from .config import STORAGE_DIR, load_settings, load_tasks
from .utils import sanitize_for_mermaid

console = Console()


def generate_mermaid_diagram(tasks):
    """Genera un diagramma Mermaid basato sui task"""
    settings = load_settings()
    diagram_conf = settings.get("diagram", {})
    output_path = os.path.join(
        STORAGE_DIR, diagram_conf.get("output", "project_structure.mmd")
    )
    style = diagram_conf.get("style", "graph TD")
    lines = [style]
    for task in tasks:
        task_id = task["id"]
        title = sanitize_for_mermaid(task["title"])
        node = f"task_{task_id}[{title}]"
        lines.append(f"    {node}")
        if task.get("blocked_by"):
            blocker = task["blocked_by"]
            lines.append(f"    task_{blocker} --> task_{task_id}")
    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    return output_path


def render_mermaid_diagram(path, open_browser=True):
    """Renderizza un file Mermaid .mmd in SVG usando mmdc"""
    if not os.path.exists(path):
        console.print(f"[red]File {path} non trovato[/red]")
        return False

    output_svg = path.replace(".mmd", ".svg")
    try:
        subprocess.run(["mmdc", "-i", path, "-o", output_svg], check=True)
        console.print(f"[green]File SVG generato: {output_svg}[/green]")

        if open_browser:
            try:
                if os.name == "nt":  # Windows
                    os.startfile(output_svg)
                elif os.name == "posix":  # Linux, macOS
                    if "darwin" in os.uname().sysname.lower():  # macOS
                        subprocess.run(["open", output_svg])
                    else:  # Linux
                        subprocess.run(["xdg-open", output_svg])
            except Exception as e:
                console.print(f"[yellow]Impossibile aprire il browser: {e}[/yellow]")

        return True
    except FileNotFoundError:
        console.print(
            "[red]Mermaid CLI non trovata. Installa con "
            "'npm install -g @mermaid-js/mermaid-cli'[/red]"
        )
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Errore durante la generazione: {e}[/red]")

    return False


def generate_task_diagram():
    """Genera un diagramma in formato Mermaid basato sui task"""
    tasks = load_tasks()
    output_file = generate_mermaid_diagram(tasks)
    console.print(f"[bold green]Diagramma generato in {output_file}[/bold green]")
    return output_file


def generate_call_graph_diagram():
    """Genera un file Mermaid .mmd con il call graph delle funzioni del progetto"""
    # Importiamo qui per evitare l'importazione circolare
    from .analyzer import generate_call_graph

    generate_call_graph()


def generate_hierarchy_diagram():
    """Genera un diagramma gerarchico Mermaid con file, classi e funzioni"""
    # Importiamo qui per evitare l'importazione circolare
    from .analyzer import generate_hierarchical_mermaid

    generate_hierarchical_mermaid()
