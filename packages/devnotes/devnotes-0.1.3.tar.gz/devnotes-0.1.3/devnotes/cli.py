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

# Crea un gruppo di comandi per Trello
trello_app = typer.Typer()
app_cli.add_typer(trello_app, name="trello", help="Comandi per l'integrazione con Trello")


class DiagramType(str, Enum):
    """Tipi di diagrammi supportati"""

    TASKS = "tasks"
    CALLGRAPH = "callgraph"
    HIERARCHY = "hierarchy"


@app_cli.command()
def init(
    project_name: str = typer.Option(
        None, "--name", "-n", 
        help="Nome del progetto (es. 'MyApp')"
    )
):
    """Inizializza un nuovo progetto devnotes"""
    from rich.prompt import Prompt
    import os
    
    # Converti project_name in una stringa se non è None
    # Questo risolve il problema con typer.Option
    if project_name is not None:
        try:
            project_name = str(project_name)
        except:
            project_name = None
    
    # Se il nome del progetto non è stato fornito, chiediamolo all'utente
    if not project_name:
        # Ottieni il nome della directory corrente come suggerimento predefinito
        default_name = os.path.basename(os.getcwd())
        project_name = Prompt.ask("Nome del progetto", default=default_name)
    
    # Inizializza il progetto con il nome specificato
    ensure_storage(project_name=project_name)
    console.print(f"[bold green]Progetto '{project_name}' inizializzato in .project/[/bold green]")


@app_cli.command()
def update():
    """Aggiorna le impostazioni con i valori predefiniti mancanti e applica le migliorie"""
    update_settings()
    console.print("[bold green]Impostazioni aggiornate con successo![/bold green]")


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
    """
    Scansiona il progetto e genera un diagramma delle funzioni e delle classi.
    
    Cerca automaticamente i commenti con tag #TASK nel codice e li aggiunge come task.
    
    Formato supportato per i task nei commenti:
    #TASK: Titolo del task
    #TASK(tag1,tag2): Titolo del task
    """
    structure = scan_project_structure(extract_code_tasks=True)
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


# Comandi per l'integrazione con Trello
@trello_app.command("setup")
def trello_setup(
    quick: bool = typer.Option(
        False, "--quick", "-q", help="Configurazione rapida con mappatura automatica delle liste"
    )
):
    """Configura l'integrazione con Trello
    
    La modalità rapida tenta di mappare automaticamente le liste Trello agli stati dei task
    in base ai nomi comuni (es. "Da fare" -> "todo").
    """
    try:
        from .trello import setup_trello_integration
        setup_trello_integration(quick_setup=quick)
    except ImportError:
        console.print("[red]Modulo Trello non disponibile.[/red]")
        console.print("Assicurati di aver installato le dipendenze richieste:")
        console.print("pip install requests")


@trello_app.command("sync")
def trello_sync(
    direction: str = typer.Option(
        "both", "--direction", "-d", 
        help="Direzione della sincronizzazione: 'to' (locale → Trello), 'from' (Trello → locale), o 'both' (bidirezionale)"
    )
):
    """Sincronizza i task tra il sistema locale e Trello
    
    La sincronizzazione può essere:
    - Da locale a Trello (--direction=to)
    - Da Trello a locale (--direction=from)
    - Bidirezionale (--direction=both, default)
    """
    try:
        from .trello import sync_tasks_to_trello, sync_tasks_from_trello
        
        if direction.lower() in ["both", "to", "from"]:
            if direction.lower() in ["both", "to"]:
                console.print("[bold]Sincronizzazione da locale a Trello...[/bold]")
                sync_tasks_to_trello()
                
            if direction.lower() in ["both", "from"]:
                console.print("[bold]Sincronizzazione da Trello a locale...[/bold]")
                sync_tasks_from_trello()
                
            if direction.lower() == "both":
                console.print("[bold green]Sincronizzazione bidirezionale completata![/bold green]")
        else:
            console.print(f"[bold red]Direzione non valida: {direction}[/bold red]")
            console.print("Usa 'to', 'from' o 'both'")
    except ImportError:
        console.print("[red]Modulo Trello non disponibile.[/red]")
        console.print("Assicurati di aver installato le dipendenze richieste:")
        console.print("pip install requests")


# Manteniamo i vecchi comandi per retrocompatibilità, ma li marchiamo come deprecati
@trello_app.command("sync-to", deprecated=True, hidden=True)
def trello_sync_to():
    """[Deprecato] Usa 'sync --direction=to' invece"""
    console.print("[yellow]Comando deprecato. Usa 'devnotes trello sync --direction=to' invece.[/yellow]")
    trello_sync(direction="to")


@trello_app.command("sync-from", deprecated=True, hidden=True)
def trello_sync_from():
    """[Deprecato] Usa 'sync --direction=from' invece"""
    console.print("[yellow]Comando deprecato. Usa 'devnotes trello sync --direction=from' invece.[/yellow]")
    trello_sync(direction="from")


@trello_app.command("status")
def trello_status():
    """Mostra lo stato dell'integrazione con Trello"""
    from .config import load_settings
    settings = load_settings()
    trello_config = settings.get("trello", {})
    
    if not trello_config:
        console.print("[yellow]L'integrazione con Trello non è configurata.[/yellow]")
        console.print("Esegui 'devnotes trello setup' per configurarla.")
        return
    
    console.print("[bold]Stato dell'integrazione con Trello[/bold]")
    console.print(f"Abilitata: {trello_config.get('enabled', False)}")
    
    if trello_config.get("enabled", False):
        console.print(f"Board: {trello_config.get('board_name', 'N/A')}")
        console.print("\nMappatura stati:")
        for status, list_id in trello_config.get("status_to_list_map", {}).items():
            console.print(f"  - {status}: {list_id}")


@trello_app.command("create-board")
def trello_create_board():
    """Crea una nuova board Trello con le liste appropriate per DevNotes"""
    try:
        from .trello import create_devnotes_board
        create_devnotes_board()
    except ImportError:
        console.print("[red]Modulo Trello non disponibile.[/red]")
        console.print("Assicurati di aver installato le dipendenze richieste:")
        console.print("pip install requests")


@app_cli.command("set-project-name")
def set_project_name(
    name: str = typer.Argument(..., help="Nuovo nome del progetto")
):
    """Imposta o aggiorna il nome del progetto"""
    from .config import load_settings, SETTINGS_FILE
    import yaml
    
    # Carica le impostazioni attuali
    settings = load_settings()
    
    # Salva il vecchio nome per il report
    old_name = settings.get("project_name", "")
    
    # Aggiorna il nome del progetto
    settings["project_name"] = name
    
    # Salva le impostazioni
    with open(SETTINGS_FILE, "w") as f:
        yaml.safe_dump(settings, f)
    
    if old_name:
        console.print(f"[bold green]Nome del progetto aggiornato da '{old_name}' a '{name}'![/bold green]")
    else:
        console.print(f"[bold green]Nome del progetto impostato a '{name}'![/bold green]")
    
    # Chiedi se aggiornare anche i task su Trello
    from rich.prompt import Confirm
    if Confirm.ask("Vuoi aggiornare anche i task su Trello con il nuovo nome del progetto?"):
        from .trello import update_project_name_on_trello
        update_project_name_on_trello(name)


if __name__ == "__main__":
    app_cli()
