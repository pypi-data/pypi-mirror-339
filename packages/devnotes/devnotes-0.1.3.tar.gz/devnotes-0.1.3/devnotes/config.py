"""
Modulo per la gestione della configurazione e dei file di storage
"""

import os

import yaml
from rich.console import Console

console = Console()

# Costanti per i percorsi dei file
STORAGE_DIR = ".project"
TASK_FILE = os.path.join(STORAGE_DIR, "tasks.yaml")
SETTINGS_FILE = os.path.join(STORAGE_DIR, "settings.yaml")
STRUCTURE_FILE = os.path.join(STORAGE_DIR, "structure.yaml")
CALLS_FILE = os.path.join(STORAGE_DIR, "calls.yaml")
CALL_GRAPH_FILE = os.path.join(STORAGE_DIR, "call_graph.mmd")

# Costante per i diagrammi Mermaid
MERMAID_HEADER = "graph TD\n"


def ensure_storage(project_name: str = None):
    """Assicura che la directory di storage esista e crea i file necessari

    Args:
        project_name: Nome del progetto da salvare nelle impostazioni
    """
    # Assicuriamoci che project_name sia una stringa o None
    # Questo risolve il problema con typer.Option
    if project_name is not None and not isinstance(project_name, str):
        # Se è un oggetto typer.Option o altro, proviamo a convertirlo in stringa
        try:
            project_name = str(project_name)
        except:
            # In caso di errore, usiamo None
            project_name = None
    
    os.makedirs(STORAGE_DIR, exist_ok=True)
    if not os.path.exists(TASK_FILE):
        with open(TASK_FILE, "w") as f:
            yaml.safe_dump([], f)

    # Gestione del file di impostazioni
    if not os.path.exists(SETTINGS_FILE):
        # Se il file non esiste, crea le impostazioni predefinite
        # Assicuriamoci che tutti i valori siano serializzabili
        project_name_str = project_name if isinstance(project_name, str) else os.path.basename(os.getcwd())
        default_settings = {
            "project_name": project_name_str,
            "statuses": ["todo", "in_progress", "done", "blocked"],
            "default_status": "todo",
            "default_tags": [],
            "diagram": {"output": "project_structure.mmd", "style": "graph TD"},
            "scan": {"exclude": [".project", ".venv"], "exclude_stdlib_calls": True},
        }
        with open(SETTINGS_FILE, "w") as f:
            yaml.safe_dump(default_settings, f)
    elif project_name:
        # Se il file esiste e abbiamo un nome di progetto, aggiorniamo solo quello
        with open(SETTINGS_FILE, "r") as f:
            settings = yaml.safe_load(f) or {}

        # Assicuriamoci che project_name sia una stringa
        if isinstance(project_name, str):
            settings["project_name"] = project_name

        with open(SETTINGS_FILE, "w") as f:
            # Aggiungi i valori predefiniti mancanti
            yaml.safe_dump(settings, f)


def update_settings():
    """Aggiorna le impostazioni con i valori predefiniti mancanti"""
    ensure_storage()
    with open(SETTINGS_FILE, "r") as f:
        current_settings = yaml.safe_load(f) or {}

    updated = False
    defaults = {
        "project_name": os.path.basename(os.getcwd()),  # Nome della directory corrente come default
        "statuses": ["todo", "in_progress", "done", "blocked"],
        "default_status": "todo",
        "default_tags": [],
        "diagram": {"output": "project_structure.mmd", "style": "graph TD"},
        "scan": {"exclude": [".project", ".venv"], "exclude_stdlib_calls": True},
    }

    for key, value in defaults.items():
        if key not in current_settings:
            current_settings[key] = value
            updated = True

    # Aggiorna la configurazione di Trello se presente
    if "trello" in current_settings:
        trello_config = current_settings["trello"]

        # Verifica se i campi personalizzati sono configurati
        if "custom_fields" not in trello_config:
            # Aggiungiamo un placeholder vuoto per i campi personalizzati
            # Verranno popolati quando l'utente eseguirà create-board o setup
            trello_config["custom_fields"] = {}
            updated = True
            console.print("[yellow]Aggiunta configurazione per campi personalizzati Trello[/yellow]")
        # Verifichiamo che value sia un dizionario prima di iterare
        elif isinstance(trello_config, dict):
            for key, value in defaults.items():
                if isinstance(value, dict) and key in current_settings:
                    for subkey, subvalue in value.items():
                        if subkey not in current_settings[key]:
                            current_settings[key][subkey] = subvalue
                            updated = True

    if updated:
        with open(SETTINGS_FILE, "w") as f:
            yaml.safe_dump(current_settings, f)
        console.print("[yellow]Impostazioni aggiornate in settings.yaml[/yellow]")
    else:
        console.print("[green]Settings già aggiornati[/green]")


def load_tasks():
    """Carica i task dal file YAML"""
    ensure_storage()
    with open(TASK_FILE, "r") as f:
        return yaml.safe_load(f) or []


def save_tasks(tasks):
    """Salva i task nel file YAML"""
    with open(TASK_FILE, "w") as f:
        yaml.safe_dump(tasks, f)


def load_settings():
    """Carica le impostazioni dal file YAML"""
    ensure_storage()
    with open(SETTINGS_FILE, "r") as f:
        return yaml.safe_load(f) or {}