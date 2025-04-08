"""
Modulo per l'integrazione con Trello
"""

import os
import requests
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.progress import Progress
from rich.prompt import Prompt, Confirm

from .config import load_settings, load_tasks, save_tasks

console = Console()

class TrelloClient:
    """Client per l'API di Trello"""
    
    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token
        self.base_url = "https://api.trello.com/1"
        
    def _get_auth_params(self) -> Dict[str, str]:
        """Restituisce i parametri di autenticazione per le richieste API"""
        return {
            "key": self.api_key,
            "token": self.token
        }
        
    def get_boards(self) -> List[Dict[str, Any]]:
        """Ottiene la lista delle board dell'utente"""
        url = f"{self.base_url}/members/me/boards"
        params = self._get_auth_params()
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def create_board(self, name: str, desc: str = "", default_lists: bool = False) -> Dict[str, Any]:
        """Crea una nuova board"""
        url = f"{self.base_url}/boards"
        params = {
            **self._get_auth_params(),
            "name": name,
            "desc": desc,
            "defaultLists": str(default_lists).lower()
        }
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_lists(self, board_id: str) -> List[Dict[str, Any]]:
        """Ottiene le liste di una board"""
        url = f"{self.base_url}/boards/{board_id}/lists"
        params = self._get_auth_params()
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def create_list(self, board_id: str, name: str, pos: str = "bottom") -> Dict[str, Any]:
        """Crea una nuova lista in una board"""
        url = f"{self.base_url}/lists"
        params = {
            **self._get_auth_params(),
            "idBoard": board_id,
            "name": name,
            "pos": pos
        }
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_cards(self, list_id: str) -> List[Dict[str, Any]]:
        """Ottiene le card di una lista"""
        url = f"{self.base_url}/lists/{list_id}/cards"
        params = self._get_auth_params()
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
        
    def get_card(self, card_id: str) -> Dict[str, Any]:
        """Ottiene i dettagli di una card specifica"""
        url = f"{self.base_url}/cards/{card_id}"
        params = self._get_auth_params()
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def create_card(self, list_id: str, name: str, desc: str = "", due: Optional[str] = None, 
                   labels: Optional[List[str]] = None, pos: str = "bottom") -> Dict[str, Any]:
        """Crea una nuova card in una lista"""
        url = f"{self.base_url}/cards"
        params = {
            **self._get_auth_params(),
            "idList": list_id,
            "name": name,
            "desc": desc,
            "pos": pos
        }
        
        if due:
            params["due"] = due
            
        if labels:
            params["idLabels"] = ",".join(labels)
            
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def update_card(self, card_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiorna una card esistente"""
        url = f"{self.base_url}/cards/{card_id}"
        params = {**self._get_auth_params(), **data}
        response = requests.put(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def delete_card(self, card_id: str) -> Dict[str, Any]:
        """Elimina una card"""
        url = f"{self.base_url}/cards/{card_id}"
        params = self._get_auth_params()
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_labels(self, board_id: str) -> List[Dict[str, Any]]:
        """Ottiene le etichette di una board"""
        url = f"{self.base_url}/boards/{board_id}/labels"
        params = self._get_auth_params()
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def create_label(self, board_id: str, name: str, color: str) -> Dict[str, Any]:
        """Crea una nuova etichetta in una board"""
        url = f"{self.base_url}/labels"
        params = {
            **self._get_auth_params(),
            "idBoard": board_id,
            "name": name,
            "color": color
        }
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json()
    
    # Metodi per i campi personalizzati
    
    def get_custom_fields(self, board_id: str) -> List[Dict[str, Any]]:
        """Ottiene i campi personalizzati di una board"""
        url = f"{self.base_url}/boards/{board_id}/customFields"
        params = self._get_auth_params()
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def create_custom_field(self, board_id: str, name: str, field_type: str, 
                           display_cardfront: bool = True, options: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea un nuovo campo personalizzato in una board
        
        Args:
            board_id: ID della board
            name: Nome del campo
            field_type: Tipo del campo (text, number, date, checkbox, list)
            display_cardfront: Se mostrare il campo sul fronte della card
            options: Opzioni per i campi di tipo 'list'
        """
        url = f"{self.base_url}/customFields"
        
        data = {
            "idModel": board_id,
            "modelType": "board",
            "name": name,
            "type": field_type,
            "pos": "bottom",
            "display_cardfront": display_cardfront
        }
        
        if options and field_type == "list":
            data["options"] = options
        
        params = self._get_auth_params()
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    
    def set_custom_field_value(self, card_id: str, field_id: str, value: Any) -> Dict[str, Any]:
        """Imposta il valore di un campo personalizzato per una card
        
        Args:
            card_id: ID della card
            field_id: ID del campo personalizzato
            value: Valore da impostare (il formato dipende dal tipo di campo)
        """
        url = f"{self.base_url}/card/{card_id}/customField/{field_id}/item"
        
        # Il formato del valore dipende dal tipo di campo
        if isinstance(value, bool):
            data = {"value": {"checked": "true" if value else "false"}}
        elif isinstance(value, (int, float)):
            data = {"value": {"number": str(value)}}
        elif isinstance(value, dict) and "id" in value:  # Per i campi di tipo 'list'
            data = {"idValue": value["id"]}
        else:
            data = {"value": {"text": str(value)}}
        
        params = self._get_auth_params()
        response = requests.put(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_custom_field_value(self, card_id: str, field_id: str) -> Dict[str, Any]:
        """Ottiene il valore di un campo personalizzato per una card"""
        url = f"{self.base_url}/cards/{card_id}/customField/{field_id}/item"
        params = self._get_auth_params()
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    # Metodi per i campi personalizzati
    
    def get_custom_fields(self, board_id: str) -> List[Dict[str, Any]]:
        """Ottiene i campi personalizzati di una board"""
        url = f"{self.base_url}/boards/{board_id}/customFields"
        params = self._get_auth_params()
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def create_custom_field(self, board_id: str, name: str, field_type: str, 
                           display_cardfront: bool = True, options: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Crea un nuovo campo personalizzato in una board
        
        Args:
            board_id: ID della board
            name: Nome del campo
            field_type: Tipo del campo (text, number, date, checkbox, list)
            display_cardfront: Se mostrare il campo sul fronte della card
            options: Opzioni per i campi di tipo 'list'
        """
        url = f"{self.base_url}/customFields"
        
        data = {
            "idModel": board_id,
            "modelType": "board",
            "name": name,
            "type": field_type,
            "pos": "bottom",
            "display_cardfront": display_cardfront
        }
        
        if options and field_type == "list":
            data["options"] = options
        
        params = self._get_auth_params()
        response = requests.post(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    
    def set_custom_field_value(self, card_id: str, field_id: str, value: Any) -> Dict[str, Any]:
        """Imposta il valore di un campo personalizzato per una card
        
        Args:
            card_id: ID della card
            field_id: ID del campo personalizzato
            value: Valore da impostare (il formato dipende dal tipo di campo)
        """
        url = f"{self.base_url}/card/{card_id}/customField/{field_id}/item"
        
        # Il formato del valore dipende dal tipo di campo
        if isinstance(value, bool):
            data = {"value": {"checked": "true" if value else "false"}}
        elif isinstance(value, (int, float)):
            data = {"value": {"number": str(value)}}
        elif isinstance(value, dict) and "id" in value:  # Per i campi di tipo 'list'
            data = {"idValue": value["id"]}
        else:
            data = {"value": {"text": str(value)}}
        
        params = self._get_auth_params()
        response = requests.put(url, params=params, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_custom_field_value(self, card_id: str, field_id: str) -> Dict[str, Any]:
        """Ottiene il valore di un campo personalizzato per una card"""
        url = f"{self.base_url}/cards/{card_id}/customField/{field_id}/item"
        params = self._get_auth_params()
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()


def setup_trello_integration(quick_setup: bool = False):
    """Configura l'integrazione con Trello
    
    Args:
        quick_setup: Se True, tenta di mappare automaticamente le liste in base ai nomi
    """
    console.print("[bold]Configurazione dell'integrazione con Trello[/bold]")
    
    # Ottieni le credenziali
    if quick_setup:
        console.print("[yellow]Per la configurazione rapida, è necessario avere già creato una board Trello con liste appropriate.[/yellow]")
    
    console.print("Per utilizzare questa funzionalità, è necessario ottenere una API key e un token da Trello.")
    console.print("1. Visita https://trello.com/app-key per ottenere la tua API key")
    console.print("2. Clicca su 'Token' per generare un token per questa applicazione")
    
    # Verifica se ci sono credenziali salvate
    settings = load_settings()
    trello_config = settings.get("trello", {})
    
    default_api_key = trello_config.get("api_key", "")
    default_token = trello_config.get("token", "")
    
    api_key = Prompt.ask("Inserisci la tua API key di Trello", default=default_api_key)
    token = Prompt.ask("Inserisci il tuo token di Trello", default=default_token)
    
    # Verifica le credenziali
    try:
        client = TrelloClient(api_key, token)
        boards = client.get_boards()
        
        console.print("[green]Connessione a Trello riuscita![/green]")
        console.print(f"Trovate {len(boards)} board")
        
        # Mostra le board disponibili
        for i, board in enumerate(boards, 1):
            console.print(f"{i}. {board['name']}")
            
        # Selezione della board
        default_board_idx = 1
        # Se c'è una board già configurata, imposta quella come default
        if trello_config.get("board_id"):
            for i, board in enumerate(boards, 1):
                if board["id"] == trello_config.get("board_id"):
                    default_board_idx = i
                    break
                    
        board_idx = int(Prompt.ask("Seleziona il numero della board da utilizzare", default=str(default_board_idx)))
        selected_board = boards[board_idx - 1]
        
        # Ottieni le liste della board
        lists = client.get_lists(selected_board["id"])
        console.print(f"La board '{selected_board['name']}' ha {len(lists)} liste:")
        
        # Mappatura delle liste agli stati dei task
        settings = load_settings()
        statuses = settings.get("statuses", ["todo", "in_progress", "done", "blocked"])
        
        # Crea un dizionario con i nomi delle liste
        list_dict = {lst["name"].lower(): lst["id"] for lst in lists}
        
        # Mappatura comune dei nomi delle liste agli stati
        common_list_names = {
            "todo": ["todo", "da fare", "to do", "backlog", "nuovi", "new"],
            "in_progress": ["in progress", "in corso", "doing", "wip", "in lavorazione"],
            "done": ["done", "completati", "completed", "fatto", "finito"],
            "blocked": ["blocked", "bloccati", "on hold", "in attesa", "waiting"]
        }
        
        status_to_list_map = {}
        
        if quick_setup:
            # Tenta di mappare automaticamente le liste in base ai nomi
            for status in statuses:
                found = False
                for name in common_list_names.get(status, [status]):
                    if name in list_dict:
                        status_to_list_map[status] = list_dict[name]
                        console.print(f"[green]Stato '{status}' mappato automaticamente alla lista '{name}'[/green]")
                        found = True
                        break
                
                if not found:
                    # Se non trova una corrispondenza esatta, cerca una corrispondenza parziale
                    for list_name in list_dict:
                        for name in common_list_names.get(status, [status]):
                            if name in list_name:
                                status_to_list_map[status] = list_dict[list_name]
                                console.print(f"[green]Stato '{status}' mappato alla lista '{list_name}'[/green]")
                                found = True
                                break
                        if found:
                            break
                
                # Se ancora non trova, chiede all'utente
                if not found:
                    console.print(f"[yellow]Non è stato possibile mappare automaticamente lo stato '{status}'[/yellow]")
                    console.print(f"\nSeleziona la lista per lo stato '{status}':")
                    for i, lst in enumerate(lists, 1):
                        console.print(f"{i}. {lst['name']}")
                    list_idx = int(Prompt.ask(f"Lista per '{status}'", default="1"))
                    status_to_list_map[status] = lists[list_idx - 1]["id"]
        else:
            # Configurazione manuale
            for status in statuses:
                # Suggerisci una lista in base ai nomi comuni
                default_list_idx = 1
                suggested_list_name = None
                
                for name in common_list_names.get(status, [status]):
                    for i, lst in enumerate(lists, 1):
                        if name.lower() in lst["name"].lower():
                            default_list_idx = i
                            suggested_list_name = lst["name"]
                            break
                    if suggested_list_name:
                        break
                
                console.print(f"\nSeleziona la lista per lo stato '{status}':")
                for i, lst in enumerate(lists, 1):
                    marker = "→ " if i == default_list_idx else "  "
                    console.print(f"{marker}{i}. {lst['name']}")
                
                list_idx = int(Prompt.ask(f"Lista per '{status}'", default=str(default_list_idx)))
                status_to_list_map[status] = lists[list_idx - 1]["id"]
        
        # Salva la configurazione
        trello_config = {
            "api_key": api_key,
            "token": token,
            "board_id": selected_board["id"],
            "board_name": selected_board["name"],
            "status_to_list_map": status_to_list_map,
            "enabled": True
        }
        
        # Aggiorna le impostazioni
        settings["trello"] = trello_config
            
            # Aggiungi il nome del progetto
            project_name = settings.get("project_name", "")
            if project_name:
                description += f"\n\nProgetto: {project_name}"
                
        
        # Salva le impostazioni
        from .config import SETTINGS_FILE
        import yaml
        with open(SETTINGS_FILE, "w") as f:
            yaml.safe_dump(settings, f)
            
        console.print("[bold green]Configurazione di Trello salvata con successo![/bold green]")
        
        # Chiedi se sincronizzare subito
        if Confirm.ask("Vuoi sincronizzare i task esistenti con Trello ora?"):
            console.print("[bold]Sincronizzazione bidirezionale in corso...[/bold]")
            # Prima sincronizziamo da locale a Trello
            sync_tasks_to_trello()
            # Poi sincronizziamo da Trello a locale per assicurarci che tutto sia allineato
            sync_tasks_from_trello()
            console.print("[bold green]Sincronizzazione completata![/bold green]")
            
    except Exception as e:
        console.print(f"[bold red]Errore durante la configurazione: {str(e)}[/bold red]")
        console.print("[yellow]Suggerimento: verifica che l'API key e il token siano corretti.[/yellow]")
        return


def get_trello_client() -> Optional[TrelloClient]:
    """Ottiene un client Trello configurato dalle impostazioni"""
    settings = load_settings()
    trello_config = settings.get("trello", {})
    
    if not trello_config.get("enabled", False):
        console.print("[yellow]L'integrazione con Trello non è abilitata.[/yellow]")
        console.print("Esegui 'devnotes trello-setup' per configurarla.")
        return None
    
    api_key = trello_config.get("api_key")
    token = trello_config.get("token")
    
    if not api_key or not token:
        console.print("[yellow]Configurazione di Trello incompleta.[/yellow]")
        console.print("Esegui 'devnotes trello-setup' per configurarla.")
        return None
    
    return TrelloClient(api_key, token)


def sync_tasks_to_trello():
    """Sincronizza i task locali con Trello"""
    client = get_trello_client()
    if not client:
        return
    
    tasks = load_tasks()
    settings = load_settings()
    trello_config = settings.get("trello", {})
    status_to_list_map = trello_config.get("status_to_list_map", {})
    
    with Progress() as progress:
        task_progress = progress.add_task("[cyan]Sincronizzazione task con Trello...", total=len(tasks))
        
        for task in tasks:
            # Salta i task che hanno già un ID Trello e non sono stati modificati
            if "trello_id" in task and not task.get("local_modified", False):
                progress.update(task_progress, advance=1)
                continue
            
            status = task.get("status", "todo")
            list_id = status_to_list_map.get(status)
            
            if not list_id:
                console.print(f"[yellow]Nessuna lista mappata per lo stato '{status}'[/yellow]")
                progress.update(task_progress, advance=1)
                continue
            
            # Prepara la descrizione
            description = task.get("description", "")
            
            # Aggiungi il nome del progetto
            project_name = settings.get("project_name", "")
            if project_name:
                description += f"\n\nProgetto: {project_name}"
                
            if task.get("file"):
                description += f"\nFile: {task['file']}"
            if task.get("symbol"):
                description += f"\nFunzione/Classe: {task['symbol']}"
            if task.get("tags"):
                description += f"\nTag: {', '.join(task['tags'])}"
            if task.get("blocked_by"):
                description += f"\nBloccato da: Task #{task['blocked_by']}"
            
            # Aggiungi un riferimento all'ID locale
            description += f"\n\nID DevNotes: {task['id']}"
            
            try:
                # Ottieni i campi personalizzati configurati
                custom_fields = trello_config.get("custom_fields", {})
                
                if "trello_id" in task:
                    # Aggiorna la card esistente
                    card_data = {
                        "name": task["title"],
                        "desc": description,
                        "idList": list_id
                    }
                    
                    if task.get("due"):
                        card_data["due"] = task["due"]
                    
                    card = client.update_card(task["trello_id"], card_data)
                else:
                    # Crea una nuova card
                    card = client.create_card(
                        list_id=list_id,
                        name=task["title"],
                        desc=description,
                        due=task.get("due")
                    )
                    
                    # Salva l'ID della card Trello nel task
                    task["trello_id"] = card["id"]
                    task["trello_url"] = card["url"]
                
                # Aggiorna i campi personalizzati se sono configurati
                if custom_fields:
                    try:
                        # Imposta il campo progetto
                        if "project" in custom_fields:
                            client.set_custom_field_value(
                                card_id=card["id"],
                                field_id=custom_fields["project"],
                                value=settings.get("project_name", "")
                            )
                        
                        # Imposta il campo file
                        if "file" in custom_fields and task.get("file"):
                            client.set_custom_field_value(
                                card_id=card["id"],
                                field_id=custom_fields["file"],
                                value=task["file"]
                            )
                        
                        # Imposta il campo funzione/classe
                        if "symbol" in custom_fields and task.get("symbol"):
                            client.set_custom_field_value(
                                card_id=card["id"],
                                field_id=custom_fields["symbol"],
                                value=task["symbol"]
                            )
                        
                        # Imposta il campo ID DevNotes
                        if "devnotes_id" in custom_fields:
                            client.set_custom_field_value(
                                card_id=card["id"],
                                field_id=custom_fields["devnotes_id"],
                                value=task["id"]
                            )
                    except Exception as e:
                        console.print(f"[yellow]Errore durante l'aggiornamento dei campi personalizzati: {str(e)}[/yellow]")
                
                # Rimuovi il flag di modifica locale
                if "local_modified" in task:
                    del task["local_modified"]
                    
            except Exception as e:
                console.print(f"[red]Errore durante la sincronizzazione del task {task['id']}: {str(e)}[/red]")
            
            progress.update(task_progress, advance=1)
    
    # Salva i task aggiornati
    save_tasks(tasks)
    console.print("[bold green]Sincronizzazione con Trello completata![/bold green]")


def sync_tasks_from_trello():
    """Sincronizza i task da Trello al sistema locale"""
    client = get_trello_client()
    if not client:
        return
    
    settings = load_settings()
    trello_config = settings.get("trello", {})
    status_to_list_map = trello_config.get("status_to_list_map", {})
    
    # Inverti la mappa per ottenere list_id -> status
    list_to_status_map = {list_id: status for status, list_id in status_to_list_map.items()}
    
    tasks = load_tasks()
    
    # Crea un dizionario di task esistenti per ID Trello
    existing_tasks_by_trello_id = {task.get("trello_id"): task for task in tasks if "trello_id" in task}
    
    # Ottieni tutte le card dalle liste configurate
    all_cards = []
    
    with Progress() as progress:
        list_progress = progress.add_task("[cyan]Recupero liste da Trello...", total=len(status_to_list_map))
        
        for list_id in status_to_list_map.values():
            try:
                cards = client.get_cards(list_id)
                all_cards.extend(cards)
            except Exception as e:
                console.print(f"[red]Errore durante il recupero delle card dalla lista {list_id}: {str(e)}[/red]")
            
            # Crea i campi personalizzati
            task3 = progress.add_task("[cyan]Creazione dei campi personalizzati...", total=4)
            
            try:
                # Campo per il progetto
                project_field = client.create_custom_field(
                    board_id=board["id"],
                    name="Progetto",
                    field_type="text",
                    display_cardfront=True
                )
                progress.update(task3, advance=1)
                
                # Campo per il file
                file_field = client.create_custom_field(
                    board_id=board["id"],
                    name="File",
                    field_type="text",
                    display_cardfront=True
                )
                progress.update(task3, advance=1)
                
                # Campo per la funzione/classe
                symbol_field = client.create_custom_field(
                    board_id=board["id"],
                    name="Funzione/Classe",
                    field_type="text",
                    display_cardfront=True
                )
                progress.update(task3, advance=1)
                
                # Campo per l'ID DevNotes
                id_field = client.create_custom_field(
                    board_id=board["id"],
                    name="ID DevNotes",
                    field_type="text",
                    display_cardfront=True
                )
                progress.update(task3, advance=1)
                
                # Salva gli ID dei campi personalizzati
                custom_fields = {
                    "project": project_field["id"],
                    "file": file_field["id"],
                    "symbol": symbol_field["id"],
                    "devnotes_id": id_field["id"]
                }
            except Exception as e:
                console.print(f"[yellow]Errore durante la creazione dei campi personalizzati: {str(e)}[/yellow]")
                console.print("[yellow]I campi personalizzati non saranno disponibili.[/yellow]")
                custom_fields = {}
                # Completiamo comunque la barra di progresso
                progress.update(task3, completed=4)
            
            progress.update(list_progress, advance=1)
    
    # Aggiorna i task esistenti e crea nuovi task
    new_tasks = []
    updated_tasks = []
    
    with Progress() as progress:
        card_progress = progress.add_task("[cyan]Elaborazione card Trello...", total=len(all_cards))
        
        for card in all_cards:
            progress.update(card_progress, advance=1)
            
            # Salta le card che sono già sincronizzate e non sono state modificate su Trello
            if card["id"] in existing_tasks_by_trello_id:
                task = existing_tasks_by_trello_id[card["id"]]
                
                # Controlla se il task è stato modificato localmente
                if task.get("local_modified", False):
                    continue
                
                # Aggiorna il task esistente
                task["title"] = card["name"]
                task["description"] = card.get("desc", "")
                task["due"] = card.get("due")
                task["status"] = list_to_status_map.get(card["idList"], "todo")
                task["trello_url"] = card["url"]
                
                updated_tasks.append(task["id"])
            else:
                # Estrai l'ID DevNotes dalla descrizione se presente
                devnotes_id = None
                description = card.get("desc", "")
                import re
                if match := re.search(r"ID DevNotes: (\d+)", description):
                    devnotes_id = match.group(1)
                
                # Se l'ID è stato trovato ma non è nella mappa, potrebbe essere stato rinominato
                if devnotes_id:
                    existing_task = next((t for t in tasks if t["id"] == devnotes_id), None)
                    if existing_task:
                        existing_task["trello_id"] = card["id"]
                        existing_task["title"] = card["name"]
                        existing_task["description"] = description
                        existing_task["due"] = card.get("due")
                        existing_task["status"] = list_to_status_map.get(card["idList"], "todo")
                        existing_task["trello_url"] = card["url"]
                        
                        updated_tasks.append(existing_task["id"])
                        continue
                
                # Crea un nuovo task
                new_task = {
                    "id": f"{len(tasks) + len(new_tasks) + 1:03}",
                    "title": card["name"],
                    "description": description,
                    "due": card.get("due"),
                    "status": list_to_status_map.get(card["idList"], "todo"),
                    "trello_id": card["id"],
                    "trello_url": card["url"],
                    "created_at": datetime.now(UTC).isoformat(),
                    "tags": []
                }
                
                new_tasks.append(new_task)
    
    # Aggiungi i nuovi task alla lista
    tasks.extend(new_tasks)
    
    # Salva i task aggiornati
    save_tasks(tasks)
    
    console.print(f"[bold green]Sincronizzazione da Trello completata![/bold green]")
    console.print(f"[green]Task aggiornati: {len(updated_tasks)}[/green]")
    console.print(f"[green]Nuovi task: {len(new_tasks)}[/green]")


def mark_task_modified(task_id: str):
    """Marca un task come modificato localmente per la prossima sincronizzazione"""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["local_modified"] = True
            break
    save_tasks(tasks)


def create_devnotes_board():
    """Crea una nuova board Trello con le liste appropriate per DevNotes"""
    client = get_trello_client()
    if not client:
        return
    
    # Chiedi il nome della board
    board_name = Prompt.ask("Nome della nuova board", default="DevNotes")
    
    try:
        with Progress() as progress:
            task1 = progress.add_task("[cyan]Creazione della board...", total=1)
            
            # Crea la board
            board = client.create_board(
                name=board_name,
                desc="Board per la gestione dei task di DevNotes",
                default_lists=False
            )
            
            progress.update(task1, completed=1)
            
            # Ottieni gli stati dei task dalle impostazioni
            settings = load_settings()
            statuses = settings.get("statuses", ["todo", "in_progress", "done", "blocked"])
            
            # Mappa degli stati ai nomi delle liste
            status_to_list_name = {
                "todo": "Da fare",
                "in_progress": "In corso",
                "done": "Completati",
                "blocked": "Bloccati"
            }
            
            # Crea le liste
            task2 = progress.add_task("[cyan]Creazione delle liste...", total=len(statuses))
            
            status_to_list_map                "custom_fields": custom_fields,
 = {}
            for i, status in enumerate(statuses):
                list_name = status_to_list_name.get(status, status.capitalize())
                trello_list = client.create_list(
                    board_id=board["id"],
                    name=list_name,
                    pos=str(i)
                )
                status_to_list_map[status] = trello_list["id"]
                progress.update(task2, advance=1)
            
            # Crea i campi personalizzati
            task3 = progress.add_task("[cyan]Creazione dei campi personalizzati...", total=4)
            
            try:
                # Campo per il progetto
                project_field = client.create_custom_field(
                    board_id=board["id"],
                    name="Progetto",
                    field_type="text",
                    display_cardfront=True
                )
                progress.update(task3, advance=1)
                
                # Campo per il file
                file_field = client.create_custom_field(
                    board_id=board["id"],
                    name="File",
                    field_type="text",
                    display_cardfront=True
                )
                progress.update(task3, advance=1)
                
                # Campo per la funzione/classe
                symbol_field = client.create_custom_field(
                    board_id=board["id"],
                    name="Funzione/Classe",
                    field_type="text",
                    display_cardfront=True
                )
                progress.update(task3, advance=1)
                
                # Campo per l'ID DevNotes
                id_field = client.create_custom_field(
                    board_id=board["id"],
                    name="ID DevNotes",
                    field_type="text",
                    display_cardfront=True
                )
                progress.update(task3, advance=1)
                
                # Salva gli ID dei campi personalizzati
                custom_fields = {
                    "project": project_field["id"],
                    "file": file_field["id"],
                    "symbol": symbol_field["id"],
                    "devnotes_id": id_field["id"]
                }
            except Exception as e:
                console.print(f"[yellow]Errore durante la creazione dei campi personalizzati: {str(e)}[/yellow]")
                console.print("[yellow]I campi personalizzati non saranno disponibili.[/yellow]")
                custom_fields = {}
                # Completiamo comunque la barra di progresso
                progress.update(task3, completed=4)
            
            # Salva la configurazione
            trello_config = {
                "api_key": client.api_key,
                "token": client.token,
                "board_id": board["id"],
                "board_name": board["name"],
                "status_to_list_map": status_to_list_map,
                "custom_fields": custom_fields,
                "enabled": True
            }
            
            # Aggiorna le impostazioni
            settings["trello"] = trello_config
            
            # Salva le impostazioni
            from .config import SETTINGS_FILE
            import yaml
            with open(SETTINGS_FILE, "w") as f:
                yaml.safe_dump(settings, f)
        
        console.print(f"[bold green]Board '{board_name}' creata con successo![/bold green]")
        console.print(f"URL: {board.get('url', 'N/A')}")
        
        # Chiedi se sincronizzare subito
        if Confirm.ask("Vuoi sincronizzare i task esistenti con Trello ora?"):
            console.print("[bold]Sincronizzazione bidirezionale in corso...[/bold]")
            # Prima sincronizziamo da locale a Trello
            sync_tasks_to_trello()
            # Poi sincronizziamo da Trello a locale per assicurarci che tutto sia allineato
            sync_tasks_from_trello()
            console.print("[bold green]Sincronizzazione completata![/bold green]")
            
    except Exception as e:
        console.print(f"[bold red]Errore durante la creazione della board: {str(e)}[/bold red]")
        return