"""
Modulo per l'analisi del codice sorgente e l'estrazione di informazioni
"""

import ast
import os

import yaml
from rich.console import Console

from .config import (
    CALL_GRAPH_FILE,
    CALLS_FILE,
    MERMAID_HEADER,
    STORAGE_DIR,
    STRUCTURE_FILE,
    load_settings,
)
from .utils import sanitize_for_mermaid

console = Console()


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


def scan_project_structure(base_path: str = "."):
    """Scansiona la struttura del progetto ed estrae informazioni sulle definizioni"""
    settings = load_settings()
    exclude_dirs = settings.get("scan", {}).get("exclude", [])
    structure = {}
    calls = {}
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

    with open(STRUCTURE_FILE, "w") as f:
        yaml.safe_dump(structure, f)
    with open(CALLS_FILE, "w") as f:
        yaml.safe_dump(calls, f)

    return structure


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
