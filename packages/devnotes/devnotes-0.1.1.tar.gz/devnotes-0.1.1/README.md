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

Per utilizzare la funzionalità di rendering dei diagrammi, è necessario installare `mermaid-cli`:

```bash
npm install -g @mermaid-js/mermaid-cli
```

Oppure per lo sviluppo:

```bash
git clone https://github.com/tuousername/devnotes.git
cd devnotes
pip install -e ".[dev]"
```

## Utilizzo

### Inizializzazione

```bash
devnotes init
```

### Gestione dei task

```bash
# Aggiungere un nuovo task
devnotes task-add-interactive

# Visualizzare tutti i task
devnotes task-list

# Modificare un task esistente
devnotes task-edit

# Marcare un task come completato
devnotes task-done 001
```

### Analisi del codice

```bash
# Scansionare il progetto
devnotes scan
```

### Diagrammi

```bash
# Generare un diagramma dei task
devnotes diagram tasks

# Generare un grafo delle chiamate
devnotes diagram callgraph

# Generare un diagramma gerarchico
devnotes diagram hierarchy

# Generare un diagramma e renderizzarlo
devnotes diagram tasks --render

# Generare un diagramma, renderizzarlo e aprilo nel browser
devnotes diagram callgraph --open

# Renderizzare un diagramma Mermaid in SVG
devnotes render --path .project/call_graph.mmd
```

## Configurazione

Le impostazioni sono salvate in `.project/settings.yaml`. È possibile aggiornare le impostazioni con:

```bash
devnotes update
```

## Build e Pubblicazione

### Utilizzo del Makefile

```bash
# Mostra i comandi disponibili
make help

# Esegui tutte le operazioni fino alla build
make all

# Pubblica su PyPI
make publish

# Pubblica su TestPyPI
make publish-test

# Installa in modalità sviluppo
make install-dev
```

### Utilizzo dello script Bash

```bash
# Rendi lo script eseguibile
chmod +x build_publish.sh

# Mostra i comandi disponibili
./build_publish.sh --help

# Esegui tutte le operazioni fino alla build
./build_publish.sh --all

# Pubblica su PyPI
./build_publish.sh --build --publish

# Pubblica su TestPyPI
./build_publish.sh --build --test-publish

# Installa in modalità sviluppo
./build_publish.sh --dev
```

## Requisiti

- Python 3.8+
- Mermaid CLI (opzionale, per la renderizzazione dei diagrammi)

## Licenza

MIT