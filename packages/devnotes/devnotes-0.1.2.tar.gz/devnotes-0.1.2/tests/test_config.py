"""
Test per il modulo config.py
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

import yaml

from devnotes.config import (
    ensure_storage,
    load_settings,
    load_tasks,
    save_tasks,
    update_settings,
)


class TestConfig(unittest.TestCase):
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

    def test_ensure_storage(self):
        """Verifica che ensure_storage crei la directory e i file necessari"""
        # Eseguiamo la funzione da testare
        ensure_storage()

        # Verifichiamo che la directory sia stata creata
        self.assertTrue(os.path.exists(".project"))

        # Verifichiamo che il file tasks.yaml sia stato creato
        self.assertTrue(os.path.exists(os.path.join(".project", "tasks.yaml")))

        # Verifichiamo che il file settings.yaml sia stato creato
        self.assertTrue(os.path.exists(os.path.join(".project", "settings.yaml")))

        # Verifichiamo il contenuto del file settings.yaml
        with open(os.path.join(".project", "settings.yaml"), "r") as f:
            settings = yaml.safe_load(f)
            self.assertIn("statuses", settings)
            self.assertIn("default_status", settings)
            self.assertIn("diagram", settings)
            self.assertIn("scan", settings)

    def test_update_settings(self):
        """Verifica che update_settings aggiorni correttamente le impostazioni"""
        # Creiamo un file settings.yaml con impostazioni parziali
        os.makedirs(".project", exist_ok=True)
        with open(os.path.join(".project", "settings.yaml"), "w") as f:
            yaml.safe_dump({"statuses": ["todo", "done"]}, f)

        # Eseguiamo la funzione da testare
        update_settings()

        # Verifichiamo che le impostazioni siano state aggiornate
        with open(os.path.join(".project", "settings.yaml"), "r") as f:
            settings = yaml.safe_load(f)
            self.assertIn("default_status", settings)
            self.assertIn("diagram", settings)
            self.assertIn("scan", settings)

    def test_load_tasks(self):
        """Verifica che load_tasks carichi correttamente i task"""
        # Creiamo un file tasks.yaml con alcuni task
        os.makedirs(".project", exist_ok=True)
        tasks = [
            {
                "id": "001",
                "title": "Test task",
                "status": "todo",
                "created_at": "2023-01-01T00:00:00",
            }
        ]
        with open(os.path.join(".project", "tasks.yaml"), "w") as f:
            yaml.safe_dump(tasks, f)

        # Eseguiamo la funzione da testare
        loaded_tasks = load_tasks()

        # Verifichiamo che i task siano stati caricati correttamente
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0]["id"], "001")
        self.assertEqual(loaded_tasks[0]["title"], "Test task")

    def test_save_tasks(self):
        """Verifica che save_tasks salvi correttamente i task"""
        # Creiamo la directory di storage
        os.makedirs(".project", exist_ok=True)

        # Creiamo alcuni task da salvare
        tasks = [
            {
                "id": "001",
                "title": "Test task",
                "status": "todo",
                "created_at": "2023-01-01T00:00:00",
            }
        ]

        # Eseguiamo la funzione da testare
        save_tasks(tasks)

        # Verifichiamo che il file sia stato creato
        self.assertTrue(os.path.exists(os.path.join(".project", "tasks.yaml")))

        # Verifichiamo che i task siano stati salvati correttamente
        with open(os.path.join(".project", "tasks.yaml"), "r") as f:
            loaded_tasks = yaml.safe_load(f)
            self.assertEqual(len(loaded_tasks), 1)
            self.assertEqual(loaded_tasks[0]["id"], "001")
            self.assertEqual(loaded_tasks[0]["title"], "Test task")

    def test_load_settings(self):
        """Verifica che load_settings carichi correttamente le impostazioni"""
        # Creiamo un file settings.yaml con alcune impostazioni
        os.makedirs(".project", exist_ok=True)
        settings = {
            "statuses": ["todo", "in_progress", "done"],
            "default_status": "todo",
        }
        with open(os.path.join(".project", "settings.yaml"), "w") as f:
            yaml.safe_dump(settings, f)

        # Eseguiamo la funzione da testare
        loaded_settings = load_settings()

        # Verifichiamo che le impostazioni siano state caricate correttamente
        self.assertEqual(loaded_settings["statuses"], ["todo", "in_progress", "done"])
        self.assertEqual(loaded_settings["default_status"], "todo")


if __name__ == "__main__":
    unittest.main()
