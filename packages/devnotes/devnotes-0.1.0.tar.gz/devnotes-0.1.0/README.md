# DevNotes

Un tool per gestire note di sviluppo e task di progetto.

## Caratteristiche

- Gestione dei task di progetto
- Analisi della struttura del codice
- Generazione di diagrammi Mermaid
- Visualizzazione delle relazioni tra funzioni

## Installazione

```bash
pip install devnotes
```

Oppure per lo sviluppo:

```bash
git clone https://github.com/tuousername/devnotes.git
cd devnotes
pip install -e ".[dev]"
```

## Test

Per eseguire i test:

```bash
pytest
```

Per eseguire i test con coverage:

```bash
pytest --cov=devnotes
```

## Utilizzo

### Inizializzazione

```bash
devnotes init
```

### Gestione dei task

```bash
# Aggiungere un nuovo task
devnotes task_add_interactive

# Visualizzare tutti i task
devnotes task_list

# Modificare un task esistente
devnotes task_edit

# Marcare un task come completato
devnotes task_done 001
```

### Analisi del codice

```bash
# Scansionare il progetto
devnotes scan

# Generare un diagramma delle chiamate tra funzioni
devnotes diagram_callgraph

# Generare un diagramma gerarchico
devnotes diagram_hierarchy
```

### Diagrammi

```bash
# Generare un diagramma basato sui task
devnotes diagram_generate

# Renderizzare un diagramma Mermaid in SVG
devnotes diagram_render --path .project/call_graph.mmd
```

## Configurazione

Le impostazioni sono salvate in `.project/settings.yaml`. È possibile aggiornare le impostazioni con:

```bash
devnotes update
```

## Requisiti

- Python 3.7+
- Mermaid CLI (opzionale, per la renderizzazione dei diagrammi)

## Licenza

MIT