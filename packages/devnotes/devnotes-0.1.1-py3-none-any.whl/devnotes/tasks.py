"""
Modulo per la gestione dei task
"""

import re
from datetime import UTC, datetime

from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

from .analyzer import scan_project_structure
from .config import load_settings, load_tasks, save_tasks

console = Console()


def parse_due_date(due_input: str):
    """Analizza una stringa di data di scadenza e la converte in formato ISO"""
    try:
        if due_input.lower() in ["", "none"]:
            return None
        if "domani" in due_input:
            return (datetime.now() + relativedelta(days=1)).isoformat()
        if match := re.match(r"tra (\d+) giorni", due_input):
            days = int(match.group(1))
            return (datetime.now() + relativedelta(days=days)).isoformat()

        # Gestione dei mesi in italiano
        mesi_italiani = {
            "gennaio": "january",
            "febbraio": "february",
            "marzo": "march",
            "aprile": "april",
            "maggio": "may",
            "giugno": "june",
            "luglio": "july",
            "agosto": "august",
            "settembre": "september",
            "ottobre": "october",
            "novembre": "november",
            "dicembre": "december",
        }

        # Converti i nomi dei mesi italiani in inglese
        input_lower = due_input.lower()
        for mese_it, mese_en in mesi_italiani.items():
            if mese_it in input_lower:
                due_input = input_lower.replace(mese_it, mese_en)
                break

        return date_parser.parse(due_input).isoformat()
    except Exception:
        # Per debug, puoi decommentare la riga seguente
        # print(f"Errore nel parsing della data: {e}")
        return None


def choose_status(settings):
    """Mostra un menu per scegliere lo stato del task"""
    statuses = settings.get("statuses", ["todo", "done"])
    status_colors = settings.get(
        "status_colors",
        {"todo": "yellow", "in_progress": "cyan", "done": "green", "blocked": "red"},
    )
    console.print("Scegli lo stato:")
    for idx, status in enumerate(statuses, 1):
        color = status_colors.get(status, "white")
        console.print(f"[{color}]{idx}. {status}[/{color}]")
    choice = IntPrompt.ask(
        "Numero", choices=[str(i) for i in range(1, len(statuses) + 1)]
    )
    return statuses[int(choice) - 1]


def display_tasks():
    """Mostra tutti i task in formato tabellare"""
    tasks = load_tasks()
    table = Table(title="Elenco Task")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Titolo", style="white")
    table.add_column("File", style="yellow")
    table.add_column("Funzione/Classe", style="blue")
    table.add_column("Stato", style="magenta")
    table.add_column("Tag", style="green")
    table.add_column("Bloccato da", style="red")
    table.add_column("Scadenza", style="bright_cyan")
    table.add_column("Creato il", style="dim")

    for task in tasks:
        table.add_row(
            task["id"],
            task["title"],
            task.get("file", "-"),
            task.get("symbol", "-"),
            task.get("status", "-"),
            ", ".join(task.get("tags", [])),
            task.get("blocked_by", "-"),
            task.get("due", "-"),
            task["created_at"][:19],
        )

    console.print(table)


def add_task_interactive():
    """Aggiunge un nuovo task in modo interattivo"""
    tasks = load_tasks()
    settings = load_settings()
    structure = scan_project_structure()

    title = Prompt.ask("Titolo del task")
    description = Prompt.ask("Descrizione", default="")
    tag_input = Prompt.ask("Tag (separati da virgola)", default="")
    tags = [t.strip() for t in tag_input.split(",") if t.strip()]
    due_input = Prompt.ask(
        "Scadenza (es. 'domani', 'tra 7 giorni', '2025-04-08 17:30')", default=""
    )
    due = parse_due_date(due_input)

    file_completer = WordCompleter(list(structure.keys()), ignore_case=True)
    file = prompt("Seleziona file: ", completer=file_completer)
    symbol_completer = WordCompleter(
        [s[0] for s in structure.get(file, [])], ignore_case=True
    )
    symbol = prompt("Seleziona funzione/classe: ", completer=symbol_completer)

    statuses = settings.get("statuses", ["todo", "done"])
    status_colors = settings.get(
        "status_colors",
        {"todo": "yellow", "in_progress": "cyan", "done": "green", "blocked": "red"},
    )
    console.print("\nScegli lo stato:")
    for idx, status in enumerate(statuses, 1):
        color = status_colors.get(status, "white")
        console.print(f"[{color}]{idx}. {status}[/{color}]")
    status_idx = IntPrompt.ask(
        "Numero", choices=[str(i) for i in range(1, len(statuses) + 1)]
    )
    status = statuses[status_idx - 1]

    task_ids = [t["id"] for t in tasks]
    blocked_by_completer = WordCompleter(task_ids, ignore_case=True)
    blocked_by = prompt("Bloccato da (ID task): ", completer=blocked_by_completer)

    task_id = f"{len(tasks) + 1:03}"
    tasks.append(
        {
            "id": task_id,
            "title": title,
            "file": file,
            "symbol": symbol,
            "description": description,
            "tags": tags or settings.get("default_tags", []),
            "due": due,
            "blocked_by": blocked_by or None,
            "status": status,
            "created_at": datetime.now(UTC).isoformat(),
        }
    )
    save_tasks(tasks)
    console.print(f"[green]Task '{title}' aggiunto con ID {task_id}[/green]")


def edit_task():
    """Modifica un task esistente"""
    tasks = load_tasks()
    settings = load_settings()

    if not tasks:
        console.print("[red]Nessun task presente da modificare.[/red]")
        return

    display_keys = [f"{t['id']} - {t['title']}" for t in tasks]
    task_lookup = {f"{t['id']} - {t['title']}": t for t in tasks}
    id_title_completer = WordCompleter(display_keys, ignore_case=True)

    selection = prompt(
        "ID o titolo del task da modificare: ", completer=id_title_completer
    )

    task = task_lookup.get(selection.strip())
    if not task:
        task = next(
            (
                t
                for t in tasks
                if t["id"] == selection.strip()
                or t["title"].lower().strip() == selection.lower().strip()
            ),
            None,
        )

    if not task:
        console.print("[red]Task non trovato.[/red]")
        return

    task_id = task["id"]
    console.print(f"[cyan]Modifica del task {task_id} - {task['title']}[/cyan]")

    task["title"] = Prompt.ask("Titolo", default=task["title"])
    task["description"] = Prompt.ask("Descrizione", default=task.get("description", ""))
    tag_input = Prompt.ask(
        "Tag (separati da virgola)", default=", ".join(task.get("tags", []))
    )
    task["tags"] = [t.strip() for t in tag_input.split(",") if t.strip()]

    due_input = Prompt.ask(
        "Scadenza (es. 'domani', 'tra 7 giorni')", default=task.get("due") or ""
    )
    task["due"] = parse_due_date(due_input)

    structure = scan_project_structure()
    file_completer = WordCompleter(list(structure.keys()), ignore_case=True)
    task["file"] = prompt(
        "File: ", completer=file_completer, default=task.get("file") or ""
    )

    symbol_completer = WordCompleter(
        [s[0] for s in structure.get(task["file"], [])], ignore_case=True
    )
    task["symbol"] = prompt(
        "Funzione/classe: ",
        completer=symbol_completer,
        default=task.get("symbol") or "",
    )

    statuses = settings.get("statuses", ["todo", "done"])
    status_colors = settings.get(
        "status_colors",
        {"todo": "yellow", "in_progress": "cyan", "done": "green", "blocked": "red"},
    )
    console.print("\nScegli lo stato:")
    for idx, status in enumerate(statuses, 1):
        color = status_colors.get(status, "white")
        console.print(f"[{color}]{idx}. {status}[/{color}]")
    status_idx = IntPrompt.ask(
        "Numero", choices=[str(i) for i in range(1, len(statuses) + 1)]
    )
    task["status"] = statuses[status_idx - 1]

    task_ids = [t["id"] for t in tasks if t["id"] != task_id]
    blocked_by_completer = WordCompleter(task_ids, ignore_case=True)
    task["blocked_by"] = (
        prompt(
            "Bloccato da (ID): ",
            completer=blocked_by_completer,
            default=task.get("blocked_by") or "",
        )
        or None
    )

    save_tasks(tasks)
    console.print(f"[green]Task {task_id} aggiornato con successo![green]")


def mark_task_done(task_id: str):
    """Marca un task come completato"""
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            found = True
            break
    if found:
        save_tasks(tasks)
        console.print(f"[bold green]Task {task_id} completato![bold green]")
    else:
        console.print(f"[bold red]Task {task_id} non trovato.[bold red]")
