"""
Modulo per l'analisi del codice sorgente e l'estrazione di informazioni
"""

import ast
import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo

import yaml
from rich.console import Console

from .config import (
    CALL_GRAPH_FILE,
    CALLS_FILE,
    MERMAID_HEADER,
    STORAGE_DIR,
    STRUCTURE_FILE,
    TASK_FILE,
    load_settings,
    load_tasks,
    save_tasks,
)
from .utils import sanitize_for_mermaid

console = Console()
UTC = ZoneInfo("UTC")


def extract_definitions(filepath):
    """Estrae le definizioni di funzioni e classi da un file Python"""
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)

    definitions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
            doc = ast.get_docstring(node) or ""
            short_doc = doc.strip().split("\n")[0] if doc else ""
            definitions.append((name, short_doc))
    return definitions


def generate_call_graph(base_path: str = "."):
    """Genera un grafo delle chiamate tra funzioni"""
    settings = load_settings()
    exclude_dirs = settings.get("scan", {}).get("exclude", [])
    exclude_builtins = settings.get("scan", {}).get("exclude_builtins", True)

    lines = [MERMAID_HEADER]
    nodes = {}
    edges = set()

    for root, _, files in os.walk(base_path):
        if any(excluded in root for excluded in exclude_dirs):
            continue
        for file in files:
            if not file.endswith(".py"):
                continue
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, base_path)
            base_id = rel_path.replace(".", "_").replace("/", "_")
            defined = extract_defined_names(abs_path)
            for name in defined:
                node_id = f"{base_id}_{name}"
                doc = ""
                with open(abs_path, "r", encoding="utf-8") as f:
                    try:
                        mod = ast.parse(f.read())
                        for n in mod.body:
                            if (
                                isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                                and n.name == name
                            ):
                                doc = ast.get_docstring(n) or ""
                    except Exception:
                        pass
                # Sanitizziamo la docstring per Mermaid
                doc = sanitize_for_mermaid(doc)
                label = f"{name}\\n{doc}" if doc else name
                nodes[node_id] = label

            calls = extract_call_relations(
                abs_path, defined_funcs=defined, exclude_builtins=exclude_builtins
            )
            for caller, callee in calls:
                caller_id = f"{base_id}_{caller}"
                callee_id = f"{base_id}_{callee}"
                edges.add((caller_id, callee_id))

    for node_id, label in nodes.items():
        lines.append(f'    {node_id}["{label}"]')
    for caller_id, callee_id in edges:
        lines.append(f"    {caller_id} --> {callee_id}")

    with open(CALL_GRAPH_FILE, "w") as f:
        f.write("\n".join(lines))

    console.print(f"[green]Call graph salvato in {CALL_GRAPH_FILE}[/green]")


def extract_structure_hierarchy(filepath):
    """Estrae la gerarchia strutturale da un file Python"""
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)
    attach_parents(tree)

    hierarchy = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            hierarchy.append(("class", node.name, ast.get_docstring(node) or ""))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parent = getattr(node, "parent", None)
            is_method = isinstance(parent, ast.ClassDef)
            hierarchy.append(
                (
                    "method" if is_method else "function",
                    node.name,
                    ast.get_docstring(node) or "",
                    parent.name if is_method else None,
                )
            )

    return hierarchy


def attach_parents(tree):
    """Aggiunge riferimenti ai nodi genitori nell'AST"""
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node


def extract_call_relations(filepath: str, defined_funcs=None, exclude_builtins=True):
    """Estrae le relazioni di chiamata tra funzioni"""
    if defined_funcs is None:
        defined_funcs = extract_defined_names(filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)

    class FunctionCallVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_function = None
            self.calls = []

        def visit_FunctionDef(self, node):
            self.current_function = node.name
            self.generic_visit(node)
            self.current_function = None

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                func_name = node.func.attr
            else:
                func_name = None
            if self.current_function and func_name in defined_funcs:
                self.calls.append((self.current_function, func_name))
            self.generic_visit(node)

    visitor = FunctionCallVisitor()
    visitor.visit(tree)
    return visitor.calls


def extract_defined_names(filepath):
    """Estrae i nomi delle funzioni definite in un file"""
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)
    return {
        n.name
        for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not n.name.startswith("__")
    }


def extract_tasks_from_comments(filepath, current_symbol=None):
    """
    Estrae i task dai commenti nel codice.
    Cerca i commenti che iniziano con #TASK e li converte in task.
    
    Formati supportati:
    #TASK: Titolo del task
    #TASK(tag1,tag2): Titolo del task
    #TASK(tag1,tag2)[due:2023-12-31][priority:high]: Titolo del task
    # DESCRIPTION: Questa è una descrizione più dettagliata del task
    # che può continuare su più righe finché le righe iniziano con # 
    
    Args:
        filepath: Percorso del file da analizzare
        current_symbol: Nome della funzione o classe corrente (opzionale)
        
    Returns:
        Lista di dizionari con i task estratti
    """
    tasks = []
    
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        
        # Ignora le linee che non iniziano con #TASK
        if not line.startswith('#TASK'):
            continue
            
        # Ignora le linee che hanno uno spazio prima di #TASK
        if line.startswith('# #TASK'):
            continue
        
        # Inizializza il task con i valori di default
        task = {
            "file": filepath,
            "line": i,
            "symbol": "",
            "tags": [],
            "description": "",
            "due": None,
            "priority": None,
            "status": "todo",
        }
        
        # Estrai i tag se presenti
        if '(' in line and ')' in line:
            # Formato: #TASK(tag1,tag2)
            tags_start = line.find('(') + 1
            tags_end = line.find(')', tags_start)
            tags_part = line[tags_start:tags_end]
            task["tags"] = [tag.strip() for tag in tags_part.split(',') if tag.strip()]
            # Rimuovi i tag dalla linea per l'elaborazione successiva
            line = line[:tags_start-1] + line[tags_end+1:]
        
        # Estrai i metadati tra parentesi quadre se presenti
        metadata_pattern = r'\[([^:]+):([^\]]+)\]'
        for match in re.finditer(metadata_pattern, line):
            key, value = match.groups()
            key = key.strip().lower()
            value = value.strip()
            
            if key == 'due':
                task["due"] = value
            elif key == 'priority':
                task["priority"] = value
            elif key == 'status':
                task["status"] = value
        
        # Rimuovi tutti i metadati tra parentesi quadre dalla linea
        line = re.sub(r'\[[^]]+\]', '', line)
        
        # Estrai il titolo
        if ':' in line:
            title_start = line.find(':') + 1
            task["title"] = line[title_start:].strip()
        else:
            # Formato non valido, salta questo task
            continue
        
        # Cerca una descrizione nelle righe successive
        description_lines = []
        while i < len(lines):
            next_line = lines[i].strip()
            if next_line.startswith('# DESCRIPTION:'):
                # Prima riga della descrizione
                desc_start = next_line.find(':') + 1
                description_lines.append(next_line[desc_start:].strip())
                i += 1
            elif next_line.startswith('#') and not next_line.startswith('#TASK'):
                # Continuazione della descrizione
                description_lines.append(next_line[1:].strip())
                i += 1
            else:
                # Fine della descrizione
                break
        
        if description_lines:
            task["description"] = '\n'.join(description_lines)
        
        # Trova il simbolo (funzione/classe) corrente
        symbol = current_symbol
        if not symbol:
            # Se non è stato fornito un simbolo, prova a determinarlo dal contesto
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if node.lineno <= task["line"] and (not hasattr(node, 'end_lineno') or node.end_lineno >= task["line"]):
                        symbol = node.name
                        break
        
        task["symbol"] = symbol or ""
        
        # Aggiungi il task alla lista
        tasks.append(task)
    
    return tasks


def scan_project_structure(base_path: str = ".", extract_code_tasks=True):
    """
    Scansiona la struttura del progetto ed estrae informazioni sulle definizioni
    
    Args:
        base_path: Percorso base del progetto
        extract_code_tasks: Se True, estrae i task dai commenti nel codice (default: True)
        
    Returns:
        Dizionario con la struttura del progetto
    """
    settings = load_settings()
    exclude_dirs = settings.get("scan", {}).get("exclude", [])
    structure = {}
    calls = {}
    
    # Se richiesto, estrai i task dai commenti
    if extract_code_tasks:
        extracted_tasks = []
        
    for root, _, files in os.walk(base_path):
        if any(excluded in root for excluded in exclude_dirs):
            continue
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_path)
                structure[rel_path] = extract_definitions(full_path)
                file_calls = extract_call_relations(full_path)
                # file_calls è una lista di tuple (caller, callee)
                for caller, callee in file_calls:
                    key = f"{rel_path}:{caller}"
                    if key not in calls:
                        calls[key] = []
                    calls[key].append(callee)
                
                # Se richiesto, estrai i task dai commenti
                if extract_code_tasks:
                    file_tasks = extract_tasks_from_comments(full_path)
                    for task in file_tasks:
                        task["file"] = rel_path  # Usa il percorso relativo
                        extracted_tasks.append(task)

    with open(STRUCTURE_FILE, "w") as f:
        yaml.safe_dump(structure, f)
    with open(CALLS_FILE, "w") as f:
        yaml.safe_dump(calls, f)
    
    # Se abbiamo estratto dei task, aggiungili al file dei task
    if extract_code_tasks and extracted_tasks:
        create_tasks_from_comments(extracted_tasks)
        console.print(f"[green]Estratti {len(extracted_tasks)} task dai commenti nel codice[/green]")

    return structure


def create_tasks_from_comments(extracted_tasks):
    """
    Crea task a partire dai commenti estratti dal codice
    
    Args:
        extracted_tasks: Lista di dizionari con i task estratti
    """
    if not extracted_tasks:
        return
        
    # Carica i task esistenti
    existing_tasks = load_tasks()
    
    # Crea un dizionario per verificare rapidamente se un task esiste già
    # Usiamo una combinazione di file, linea e titolo come chiave
    existing_task_keys = {
        f"{task.get('file', '')}:{task.get('line', '')}:{task.get('title', '')}": task
        for task in existing_tasks
    }
    
    # Contatori per le statistiche
    new_tasks_count = 0
    updated_tasks_count = 0
    
    for task_data in extracted_tasks:
        # Crea una chiave per verificare se il task esiste già
        task_key = f"{task_data.get('file', '')}:{task_data.get('line', '')}:{task_data.get('title', '')}"
        
        if task_key in existing_task_keys:
            # Il task esiste già, aggiorna i campi se necessario
            existing_task = existing_task_keys[task_key]
            updated = False
            
            # Aggiorna i tag se sono diversi
            if set(task_data.get('tags', [])) != set(existing_task.get('tags', [])):
                existing_task['tags'] = list(set(existing_task.get('tags', []) + task_data.get('tags', [])))
                updated = True
            
            # Aggiorna la descrizione se è stata fornita e diversa
            if task_data.get('description') and task_data['description'] != existing_task.get('description', ''):
                existing_task['description'] = task_data['description']
                updated = True
            
            # Aggiorna la data di scadenza se è stata fornita
            if task_data.get('due') and task_data['due'] != existing_task.get('due'):
                existing_task['due'] = task_data['due']
                updated = True
            
            # Aggiorna la priorità se è stata fornita
            if task_data.get('priority') and task_data['priority'] != existing_task.get('priority'):
                existing_task['priority'] = task_data['priority']
                updated = True
            
            # Aggiorna lo stato se è stato fornito e diverso da "done"
            # Non aggiorniamo lo stato se il task è già completato
            if task_data.get('status') and existing_task.get('status') != 'done':
                existing_task['status'] = task_data['status']
                updated = True
            
            if updated:
                updated_tasks_count += 1
        else:
            # Il task non esiste, creane uno nuovo
            task_id = f"{len(existing_tasks) + 1:03}"
            new_task = {
                "id": task_id,
                "title": task_data["title"],
                "file": task_data["file"],
                "line": task_data["line"],
                "symbol": task_data.get("symbol", ""),
                "description": task_data.get("description", ""),
                "tags": task_data.get("tags", []),
                "status": task_data.get("status", "todo"),
                "created_at": datetime.now(UTC).isoformat(),
            }
            
            # Aggiungi la data di scadenza se presente
            if task_data.get("due"):
                new_task["due"] = task_data["due"]
            
            # Aggiungi la priorità se presente
            if task_data.get("priority"):
                new_task["priority"] = task_data["priority"]
            
            existing_tasks.append(new_task)
            new_tasks_count += 1
    
    # Salva i task aggiornati
    if new_tasks_count > 0 or updated_tasks_count > 0:
        save_tasks(existing_tasks)
        console.print(f"[green]Aggiunti {new_tasks_count} nuovi task, aggiornati {updated_tasks_count} task esistenti[/green]")


def generate_hierarchical_mermaid(base_path: str = "."):
    """Genera un diagramma gerarchico in formato Mermaid"""
    lines = [MERMAID_HEADER]
    settings = load_settings()
    exclude_dirs = settings.get("scan", {}).get("exclude", [])
    node_map = {}
    edges = []

    for root, _, files in os.walk(base_path):
        if any(excluded in root for excluded in exclude_dirs):
            continue
        for file in files:
            if not file.endswith(".py"):
                continue
            rel_path = os.path.relpath(os.path.join(root, file), base_path)
            file_id = rel_path.replace(".", "_").replace("/", "_").replace("\\", "_")
            abs_path = os.path.join(root, file)
            with open(abs_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=abs_path)
                attach_parents(tree)
                items = extract_structure_hierarchy(abs_path)
                defined_funcs = extract_defined_names(abs_path)
                calls = extract_call_relations(abs_path, defined_funcs)
                lines.append(f"  subgraph {file_id}")
                class_map = {}
                current_class = None
                for kind, name, doc, *parent in items:
                    node_id = f"{file_id}_{name}"
                    node_map[name] = node_id
                    # Sanitizziamo la docstring per Mermaid
                    doc = sanitize_for_mermaid(doc)
                    label = f"{name}\\n{doc}" if doc else name
                    if kind == "class":
                        lines.append(f"    subgraph {node_id}[{label}]")
                        current_class = node_id
                        class_map[name] = node_id
                    elif kind == "method":
                        lines.append(f"      {node_id}[{label}]")
                    elif kind == "function":
                        if current_class:
                            lines.append("    end")
                            current_class = None
                        lines.append(f"    {node_id}[{label}]")
                if current_class:
                    lines.append("    end")
                lines.append("  end")

                for caller, callee in calls:
                    if caller in node_map and callee in node_map:
                        edges.append(f"  {node_map[caller]} --> {node_map[callee]}")

    lines.extend(edges)

    output_path = os.path.join(STORAGE_DIR, "structure_graph.mmd")
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    console.print(f"[green]Diagramma gerarchico salvato in {output_path}[/green]")
