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


def ensure_storage():
    """Assicura che la directory di storage esista e crea i file di base se necessario"""
    os.makedirs(STORAGE_DIR, exist_ok=True)
    if not os.path.exists(TASK_FILE):
        with open(TASK_FILE, "w") as f:
            yaml.dump([], f)
    if not os.path.exists(SETTINGS_FILE):
        default_settings = {
            "statuses": ["todo", "in_progress", "done", "blocked"],
            "default_status": "todo",
            "default_tags": [],
            "diagram": {
                "output": "project_structure.mmd",
                "style": "graph TD"
            },
            "scan": {
                "exclude": [".project", ".venv"],
                "exclude_stdlib_calls": True
            }
        }
        with open(SETTINGS_FILE, "w") as f:
            yaml.safe_dump(default_settings, f)


def update_settings():
    """Aggiorna le impostazioni con i valori predefiniti mancanti"""
    ensure_storage()
    with open(SETTINGS_FILE, "r") as f:
        current_settings = yaml.safe_load(f) or {}

    updated = False
    defaults = {
        "statuses": ["todo", "in_progress", "done", "blocked"],
        "default_status": "todo",
        "default_tags": [],
        "diagram": {
            "output": "project_structure.mmd",
            "style": "graph TD"
        },
        "scan": {
            "exclude": [".project", ".venv"],
            "exclude_stdlib_calls": True
        }
    }

    for key, value in defaults.items():
        if key not in current_settings:
            current_settings[key] = value
            updated = True
        elif isinstance(value, dict):
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