"""
Test per il modulo diagrams.py
"""

import os
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from devnotes.diagrams import generate_mermaid_diagram


class TestDiagrams(unittest.TestCase):
    def setUp(self):
        # Creiamo una directory temporanea per i test
        self.test_dir = tempfile.mkdtemp()
        # Salviamo la directory corrente
        self.original_dir = os.getcwd()
        # Ci spostiamo nella directory temporanea
        os.chdir(self.test_dir)
        # Creiamo la directory di storage
        os.makedirs(".project", exist_ok=True)
        
    def tearDown(self):
        # Ripristiniamo la directory originale
        os.chdir(self.original_dir)
        # Rimuoviamo la directory temporanea
        shutil.rmtree(self.test_dir)
    
    @patch('devnotes.diagrams.load_settings')
    def test_generate_mermaid_diagram(self, mock_load_settings):
        """Verifica che generate_mermaid_diagram generi correttamente il diagramma"""
        # Mock delle impostazioni
        mock_load_settings.return_value = {
            "diagram": {
                "output": "test_diagram.mmd",
                "style": "graph TD"
            }
        }
        
        # Creiamo alcuni task di esempio
        tasks = [
            {
                "id": "001",
                "title": "Task 1",
                "status": "todo"
            },
            {
                "id": "002",
                "title": "Task 2",
                "status": "in_progress",
                "blocked_by": "001"
            }
        ]
        
        # Eseguiamo la funzione da testare
        output_path = generate_mermaid_diagram(tasks)
        
        # Verifichiamo che il file sia stato creato
        self.assertTrue(os.path.exists(output_path))
        
        # Verifichiamo il contenuto del file
        with open(output_path, "r") as f:
            content = f.read()
            self.assertIn("graph TD", content)
            self.assertIn("task_001[Task 1]", content)
            self.assertIn("task_002[Task 2]", content)
            self.assertIn("task_001 --> task_002", content)


# Aggiungi altri test per le altre funzioni del modulo diagrams.py
# Ad esempio, potresti voler testare render_mermaid_diagram, generate_task_diagram, generate_call_graph_diagram
# Questi test richiederebbero un maggiore uso di mock, specialmente per subprocess.run


if __name__ == '__main__':
    unittest.main()