"""
Test di integrazione per DevNotes
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

import yaml

from devnotes.cli import init
from devnotes.config import ensure_storage, load_settings, load_tasks, save_tasks
from devnotes.tasks import add_task_interactive, edit_task, mark_task_done


class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Creiamo una directory temporanea per i test
        self.test_dir = tempfile.mkdtemp()
        # Salviamo la directory corrente
        self.original_dir = os.getcwd()
        # Ci spostiamo nella directory temporanea
        os.chdir(self.test_dir)
        # Patchamo la costante STORAGE_DIR per usare un percorso relativo
        self.storage_patcher = patch("devnotes.config.STORAGE_DIR", ".project")
        self.storage_patcher.start()

    def tearDown(self):
        # Ripristiniamo la directory originale
        os.chdir(self.original_dir)
        # Rimuoviamo la directory temporanea
        shutil.rmtree(self.test_dir)
        # Stoppiamo il patch
        self.storage_patcher.stop()

    def test_project_initialization(self):
        """Verifica che l'inizializzazione del progetto funzioni correttamente"""
        # Verifichiamo che la directory di storage non esista ancora
        self.assertFalse(os.path.exists(".project"))

        # Inizializziamo il progetto
        with patch("devnotes.cli.console.print"):
            init()

        # Verifichiamo che la directory di storage sia stata creata
        self.assertTrue(os.path.exists(".project"))

        # Verifichiamo che i file necessari siano stati creati
        self.assertTrue(os.path.exists(os.path.join(".project", "tasks.yaml")))
        self.assertTrue(os.path.exists(os.path.join(".project", "settings.yaml")))

        # Verifichiamo che le impostazioni siano state inizializzate correttamente
        settings = load_settings()
        self.assertIn("statuses", settings)
        self.assertIn("default_status", settings)
        self.assertIn("diagram", settings)
        self.assertIn("scan", settings)

        # Verifichiamo che il file tasks.yaml sia vuoto
        tasks = load_tasks()
        self.assertEqual(len(tasks), 0)

    @patch("devnotes.tasks.Prompt.ask")
    @patch("devnotes.tasks.prompt")
    @patch("devnotes.tasks.IntPrompt.ask")
    @patch("devnotes.tasks.scan_project_structure")
    def test_add_task(self, mock_scan, mock_int_prompt, mock_prompt, mock_ask):
        """Verifica che l'aggiunta di un task funzioni correttamente"""
        # Inizializziamo il progetto
        ensure_storage()

        # Configuriamo i mock per simulare l'input dell'utente
        mock_ask.side_effect = [
            "Test task",  # Titolo
            "Descrizione del task",  # Descrizione
            "test, example",  # Tag
            "31 dicembre 2025",  # Scadenza
        ]
        mock_prompt.side_effect = [
            "test_file.py",  # File
            "test_function",  # Funzione
            "",  # Bloccato da
        ]
        mock_int_prompt.return_value = 1  # Stato (todo)

        # Configuriamo il mock per scan_project_structure
        mock_scan.return_value = {"test_file.py": [("test_function", "Test function")]}

        # Eseguiamo la funzione da testare
        with patch("devnotes.tasks.console.print"):
            add_task_interactive()

        # Verifichiamo che il task sia stato aggiunto
        tasks = load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Test task")
        self.assertEqual(tasks[0]["description"], "Descrizione del task")
        self.assertEqual(tasks[0]["tags"], ["test", "example"])
        self.assertIn("2025", tasks[0]["due"])
        self.assertEqual(tasks[0]["file"], "test_file.py")
        self.assertEqual(tasks[0]["symbol"], "test_function")
        self.assertEqual(tasks[0]["status"], "todo")
        self.assertIsNone(tasks[0]["blocked_by"])

    @patch("devnotes.tasks.Prompt.ask")
    @patch("devnotes.tasks.prompt")
    @patch("devnotes.tasks.IntPrompt.ask")
    @patch("devnotes.tasks.scan_project_structure")
    def test_edit_task(self, mock_scan, mock_int_prompt, mock_prompt, mock_ask):
        """Verifica che la modifica di un task funzioni correttamente"""
        # Inizializziamo il progetto
        ensure_storage()

        # Creiamo un task di esempio
        tasks = [
            {
                "id": "001",
                "title": "Task originale",
                "description": "Descrizione originale",
                "tags": ["original"],
                "due": "2025-01-01T00:00:00",
                "file": "original_file.py",
                "symbol": "original_function",
                "status": "todo",
                "blocked_by": None,
                "created_at": "2023-01-01T00:00:00",
            }
        ]
        save_tasks(tasks)

        # Configuriamo i mock per simulare l'input dell'utente
        mock_ask.side_effect = [
            "Task modificato",  # Titolo
            "Descrizione modificata",  # Descrizione
            "modified, updated",  # Tag
            "31 dicembre 2026",  # Scadenza
        ]
        mock_prompt.side_effect = [
            "001",  # ID del task da modificare
            "modified_file.py",  # File
            "modified_function",  # Funzione
            "",  # Bloccato da
        ]
        mock_int_prompt.return_value = 2  # Stato (in_progress)

        # Configuriamo il mock per scan_project_structure
        mock_scan.return_value = {
            "modified_file.py": [("modified_function", "Modified function")]
        }

        # Eseguiamo la funzione da testare
        with patch("devnotes.tasks.console.print"):
            edit_task()

        # Verifichiamo che il task sia stato modificato
        tasks = load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Task modificato")
        self.assertEqual(tasks[0]["description"], "Descrizione modificata")
        self.assertEqual(tasks[0]["tags"], ["modified", "updated"])
        self.assertIn("2026", tasks[0]["due"])
        self.assertEqual(tasks[0]["file"], "modified_file.py")
        self.assertEqual(tasks[0]["symbol"], "modified_function")
        self.assertEqual(tasks[0]["status"], "in_progress")
        self.assertIsNone(tasks[0]["blocked_by"])
        # Verifichiamo che l'ID e la data di creazione non siano stati modificati
        self.assertEqual(tasks[0]["id"], "001")
        self.assertEqual(tasks[0]["created_at"], "2023-01-01T00:00:00")

    def test_mark_task_done(self):
        """Verifica che la marcatura di un task come completato funzioni"""
        # Inizializziamo il progetto
        ensure_storage()

        # Creiamo un task di esempio
        tasks = [
            {
                "id": "001",
                "title": "Task da completare",
                "status": "todo",
                "created_at": "2023-01-01T00:00:00",
            }
        ]
        save_tasks(tasks)

        # Eseguiamo la funzione da testare
        with patch("devnotes.tasks.console.print"):
            mark_task_done("001")

        # Verifichiamo che il task sia stato marcato come completato
        tasks = load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["status"], "done")

    def test_mark_nonexistent_task_done(self):
        """Verifica che la marcatura di un task inesistente gestisca l'errore"""
        # Inizializziamo il progetto
        ensure_storage()

        # Creiamo un task di esempio
        tasks = [
            {
                "id": "001",
                "title": "Task esistente",
                "status": "todo",
                "created_at": "2023-01-01T00:00:00",
            }
        ]
        save_tasks(tasks)

        # Eseguiamo la funzione da testare con un ID inesistente
        with patch("devnotes.tasks.console.print") as mock_print:
            mark_task_done("999")

        # Verifichiamo che sia stato mostrato un messaggio di errore
        mock_print.assert_called_with("[bold red]Task 999 non trovato.[bold red]")

        # Verifichiamo che il task esistente non sia stato modificato
        tasks = load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["status"], "todo")


class TestWorkflow(unittest.TestCase):
    """Test che verificano l'intero flusso di lavoro dell'applicazione"""

    def setUp(self):
        # Creiamo una directory temporanea per i test
        self.test_dir = tempfile.mkdtemp()
        # Salviamo la directory corrente
        self.original_dir = os.getcwd()
        # Ci spostiamo nella directory temporanea
        os.chdir(self.test_dir)
        # Patchamo la costante STORAGE_DIR per usare un percorso relativo
        self.storage_patcher = patch("devnotes.config.STORAGE_DIR", ".project")
        self.storage_patcher.start()

        # Creiamo un file Python di esempio per i test
        os.makedirs("src", exist_ok=True)
        with open(os.path.join("src", "example.py"), "w") as f:
            f.write(
                """
def hello():
    \"\"\"Say hello\"\"\"
    return "Hello, world!"

def goodbye():
    \"\"\"Say goodbye\"\"\"
    return "Goodbye, world!"
"""
            )

    def tearDown(self):
        # Ripristiniamo la directory originale
        os.chdir(self.original_dir)
        # Rimuoviamo la directory temporanea
        shutil.rmtree(self.test_dir)
        # Stoppiamo il patch
        self.storage_patcher.stop()

    @patch("devnotes.tasks.Prompt.ask")
    @patch("devnotes.tasks.prompt")
    @patch("devnotes.tasks.IntPrompt.ask")
    def test_complete_workflow(self, mock_int_prompt, mock_prompt, mock_ask):
        """Verifica il flusso: inizializzazione, aggiunta, modifica e completamento di task"""
        # Inizializziamo il progetto
        with patch("devnotes.cli.console.print"):
            init()

        # Verifichiamo che il progetto sia stato inizializzato correttamente
        self.assertTrue(os.path.exists(".project"))
        self.assertTrue(os.path.exists(os.path.join(".project", "tasks.yaml")))
        self.assertTrue(os.path.exists(os.path.join(".project", "settings.yaml")))

        # Configuriamo i mock per simulare l'aggiunta di un task
        mock_ask.side_effect = [
            "Implementare nuova funzionalità",  # Titolo
            "Aggiungere supporto per X",  # Descrizione
            "feature, enhancement",  # Tag
            "domani",  # Scadenza
            # Per la modifica
            "Implementare nuova funzionalità (urgente)",  # Titolo
            "Aggiungere supporto per X e Y",  # Descrizione
            "feature, enhancement, urgent",  # Tag
            "tra 3 giorni",  # Scadenza
        ]
        mock_prompt.side_effect = [
            "src/example.py",  # File
            "hello",  # Funzione
            "",  # Bloccato da
            # Per la modifica
            "001",  # ID del task da modificare
            "src/example.py",  # File
            "goodbye",  # Funzione
            "",  # Bloccato da
        ]
        mock_int_prompt.side_effect = [1, 2]  # Stato (todo, poi in_progress)

        # Aggiungiamo un task
        with patch("devnotes.tasks.console.print"), patch(
            "devnotes.tasks.scan_project_structure"
        ) as mock_scan:
            mock_scan.return_value = {
                "src/example.py": [("hello", "Say hello"), ("goodbye", "Say goodbye")]
            }
            add_task_interactive()

        # Verifichiamo che il task sia stato aggiunto
        tasks = load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Implementare nuova funzionalità")
        self.assertEqual(tasks[0]["status"], "todo")

        # Modifichiamo il task
        with patch("devnotes.tasks.console.print"), patch(
            "devnotes.tasks.scan_project_structure"
        ) as mock_scan:
            mock_scan.return_value = {
                "src/example.py": [("hello", "Say hello"), ("goodbye", "Say goodbye")]
            }
            edit_task()

        # Verifichiamo che il task sia stato modificato
        tasks = load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Implementare nuova funzionalità (urgente)")
        self.assertEqual(tasks[0]["status"], "in_progress")
        self.assertEqual(tasks[0]["symbol"], "goodbye")

        # Marchiamo il task come completato
        with patch("devnotes.tasks.console.print"):
            mark_task_done("001")

        # Verifichiamo che il task sia stato completato
        tasks = load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["status"], "done")


if __name__ == "__main__":
    unittest.main()
