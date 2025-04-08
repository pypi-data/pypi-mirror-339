"""
Test per l'estrazione di task dai commenti nel codice
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

import yaml

from devnotes.analyzer import extract_tasks_from_comments, scan_project_structure


class TestTaskExtraction(unittest.TestCase):
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
        
        # Creiamo la directory di storage
        os.makedirs(".project", exist_ok=True)
        
        # Creiamo un file Python di esempio con task nei commenti
        self.test_file = os.path.join(self.test_dir, "test_module.py")
        with open(self.test_file, "w") as f:
            f.write(
                """
# Un commento normale
# #TASK: Questo non è un task valido (ha uno spazio prima)

#TASK: Implementare la funzione di test
def test_function():
    \"\"\"Questa è una funzione di test\"\"\"
    #TASK(bug,high): Correggere il bug in questa funzione
    return "test"

class TestClass:
    \"\"\"Questa è una classe di test\"\"\"
    
    #TASK(feature)[due:2023-12-31][priority:high][status:in_progress]: Aggiungere nuova funzionalità
    # DESCRIPTION: Questa è una descrizione dettagliata del task
    # che continua su più righe
    def test_method(self):
        \"\"\"Questo è un metodo di test\"\"\"
        return "test method"
"""
            )
        
        # Creiamo un file tasks.yaml vuoto
        with open(os.path.join(".project", "tasks.yaml"), "w") as f:
            yaml.safe_dump([], f)

    def tearDown(self):
        # Ripristiniamo la directory originale
        os.chdir(self.original_dir)
        # Rimuoviamo la directory temporanea
        shutil.rmtree(self.test_dir)
        # Stoppiamo il patch
        self.storage_patcher.stop()

    def test_extract_tasks_from_comments(self):
        """Verifica che extract_tasks_from_comments estragga correttamente i task dai commenti"""
        # Eseguiamo la funzione da testare
        tasks = extract_tasks_from_comments(self.test_file)
        
        # Verifichiamo che siano stati estratti 3 task
        self.assertEqual(len(tasks), 3)
        
        # Verifichiamo che i titoli dei task siano corretti
        titles = [task["title"] for task in tasks]
        self.assertIn("Implementare la funzione di test", titles)
        self.assertIn("Correggere il bug in questa funzione", titles)
        self.assertIn("Aggiungere nuova funzionalità", titles)
        
        # Verifichiamo che i tag siano stati estratti correttamente
        task_with_tags = next(task for task in tasks if "bug" in task.get("tags", []))
        self.assertIn("high", task_with_tags["tags"])
        
        # Verifichiamo che il task nella classe abbia il tag "feature"
        task_with_feature = next(task for task in tasks if "feature" in task.get("tags", []))
        self.assertEqual(task_with_feature["title"], "Aggiungere nuova funzionalità")
        
    def test_extract_task_metadata(self):
        """Verifica che extract_tasks_from_comments estragga correttamente i metadati e la descrizione"""
        # Eseguiamo la funzione da testare
        tasks = extract_tasks_from_comments(self.test_file)
        
        # Troviamo il task con metadati
        task_with_metadata = next(task for task in tasks if "feature" in task.get("tags", []))
        
        # Verifichiamo i metadati
        self.assertEqual(task_with_metadata["due"], "2023-12-31")
        self.assertEqual(task_with_metadata["priority"], "high")
        self.assertEqual(task_with_metadata["status"], "in_progress")
        
        # Verifichiamo la descrizione
        self.assertIn("Questa è una descrizione dettagliata del task", task_with_metadata["description"])
        self.assertIn("che continua su più righe", task_with_metadata["description"])

    @patch("devnotes.analyzer.console.print")
    def test_scan_project_structure_task_extraction(self, mock_print):
        """Verifica che scan_project_structure estragga automaticamente i task"""
        # Eseguiamo la funzione da testare (ora l'estrazione dei task è abilitata per default)
        scan_project_structure()
        
        # Verifichiamo che il file tasks.yaml contenga i task estratti
        with open(os.path.join(".project", "tasks.yaml"), "r") as f:
            tasks = yaml.safe_load(f)
            
        # Verifichiamo che siano stati creati 3 task
        self.assertEqual(len(tasks), 3)
        
        # Verifichiamo che i titoli dei task siano corretti
        titles = [task["title"] for task in tasks]
        self.assertIn("Implementare la funzione di test", titles)
        self.assertIn("Correggere il bug in questa funzione", titles)
        self.assertIn("Aggiungere nuova funzionalità", titles)
        
        # Verifichiamo che i task abbiano gli ID corretti
        ids = [task["id"] for task in tasks]
        self.assertEqual(set(ids), {"001", "002", "003"})
        
        # Verifichiamo che i task abbiano gli stati corretti
        statuses = [task["status"] for task in tasks]
        self.assertEqual(set(statuses), {"todo", "in_progress"})
        
        # Verifichiamo che il task con tag "feature" abbia lo stato "in_progress"
        task_with_feature = next(task for task in tasks if "feature" in task.get("tags", []))
        self.assertEqual(task_with_feature["status"], "in_progress")


if __name__ == "__main__":
    unittest.main()