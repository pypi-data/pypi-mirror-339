"""
Test di integrazione per l'interfaccia a riga di comando
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

import yaml
from typer.testing import CliRunner

from devnotes.cli import app_cli


class TestCliIntegration(unittest.TestCase):
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
        # Creiamo un runner per i comandi CLI
        self.runner = CliRunner()

    def tearDown(self):
        # Ripristiniamo la directory originale
        os.chdir(self.original_dir)
        # Rimuoviamo la directory temporanea
        shutil.rmtree(self.test_dir)
        # Stoppiamo il patch
        self.storage_patcher.stop()

    def test_cli_init_and_task_done(self):
        """Verifica che i comandi CLI init e task-done funzionino correttamente insieme"""
        # Eseguiamo il comando init
        result = self.runner.invoke(app_cli, ["init"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Progetto inizializzato", result.stdout)

        # Verifichiamo che la directory di storage sia stata creata
        self.assertTrue(os.path.exists(".project"))

        # Creiamo manualmente un task per testare il comando task-done
        os.makedirs(".project", exist_ok=True)
        with open(os.path.join(".project", "tasks.yaml"), "w") as f:
            yaml.safe_dump(
                [
                    {
                        "id": "001",
                        "title": "Task di test",
                        "status": "todo",
                        "created_at": "2023-01-01T00:00:00",
                    }
                ],
                f,
            )

        # Eseguiamo il comando task-done
        result = self.runner.invoke(app_cli, ["task-done", "001"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Task 001 completato", result.stdout)

        # Verifichiamo che il task sia stato marcato come completato
        with open(os.path.join(".project", "tasks.yaml"), "r") as f:
            tasks = yaml.safe_load(f)
            self.assertEqual(tasks[0]["status"], "done")

    def test_cli_task_list(self):
        """Verifica che il comando CLI task-list funzioni correttamente"""
        # Inizializziamo il progetto
        self.runner.invoke(app_cli, ["init"])

        # Creiamo manualmente alcuni task
        os.makedirs(".project", exist_ok=True)
        with open(os.path.join(".project", "tasks.yaml"), "w") as f:
            yaml.safe_dump(
                [
                    {
                        "id": "001",
                        "title": "Task 1",
                        "status": "todo",
                        "created_at": "2023-01-01T00:00:00",
                    },
                    {
                        "id": "002",
                        "title": "Task 2",
                        "status": "in_progress",
                        "created_at": "2023-01-02T00:00:00",
                    },
                ],
                f,
            )

        # Eseguiamo il comando task-list
        result = self.runner.invoke(app_cli, ["task-list"])
        self.assertEqual(result.exit_code, 0)

        # Verifichiamo che l'output contenga i task
        self.assertIn("Task 1", result.stdout)
        self.assertIn("Task 2", result.stdout)
        self.assertIn("todo", result.stdout)
        # La tabella Rich potrebbe troncare "in_progress" a "in_pro..."
        self.assertTrue("in_pro" in result.stdout or "in_progress" in result.stdout)

    @patch("devnotes.cli.scan_project_structure")
    def test_cli_scan(self, mock_scan):
        """Verifica che il comando CLI scan funzioni correttamente"""
        # Configuriamo il mock per scan_project_structure
        mock_scan.return_value = {
            "file1.py": [("func1", "Function 1"), ("func2", "Function 2")],
            "file2.py": [("class1", "Class 1")],
        }

        # Inizializziamo il progetto
        self.runner.invoke(app_cli, ["init"])

        # Eseguiamo il comando scan
        result = self.runner.invoke(app_cli, ["scan"])
        self.assertEqual(result.exit_code, 0)

        # Verifichiamo che l'output contenga le informazioni sui file e le funzioni
        self.assertIn("file1.py", result.stdout)
        self.assertIn("file2.py", result.stdout)
        self.assertIn("func1", result.stdout)
        self.assertIn("func2", result.stdout)
        self.assertIn("class1", result.stdout)

    @patch("devnotes.cli.generate_task_diagram")
    def test_cli_diagram_tasks(self, mock_generate):
        """Verifica che il comando CLI diagram tasks funzioni correttamente"""
        # Configuriamo il mock per generate_task_diagram
        mock_generate.return_value = ".project/test_diagram.mmd"

        # Inizializziamo il progetto
        self.runner.invoke(app_cli, ["init"])

        # Eseguiamo il comando diagram tasks
        result = self.runner.invoke(app_cli, ["diagram", "tasks"])
        self.assertEqual(result.exit_code, 0)

        # Verifichiamo che l'output contenga il percorso del diagramma generato
        self.assertIn("Diagramma dei task generato", result.stdout)
        self.assertIn("test_diagram.mmd", result.stdout)

    @patch("devnotes.cli.generate_call_graph_diagram")
    def test_cli_diagram_callgraph(self, mock_generate):
        """Verifica che il comando CLI diagram callgraph funzioni correttamente"""
        # Inizializziamo il progetto
        self.runner.invoke(app_cli, ["init"])

        # Eseguiamo il comando diagram callgraph
        result = self.runner.invoke(app_cli, ["diagram", "callgraph"])
        self.assertEqual(result.exit_code, 0)

        # Verifichiamo che l'output contenga il percorso del diagramma generato
        self.assertIn("Call graph generato", result.stdout)
        self.assertIn("call_graph.mmd", result.stdout)

        # Verifichiamo che generate_call_graph_diagram sia stato chiamato
        mock_generate.assert_called_once()

    @patch("devnotes.cli.generate_hierarchy_diagram")
    def test_cli_diagram_hierarchy(self, mock_generate):
        """Verifica che il comando CLI diagram hierarchy funzioni correttamente"""
        # Inizializziamo il progetto
        self.runner.invoke(app_cli, ["init"])

        # Eseguiamo il comando diagram hierarchy
        result = self.runner.invoke(app_cli, ["diagram", "hierarchy"])
        self.assertEqual(result.exit_code, 0)

        # Verifichiamo che l'output contenga il percorso del diagramma generato
        self.assertIn("Diagramma gerarchico generato", result.stdout)
        self.assertIn("structure_graph.mmd", result.stdout)

        # Verifichiamo che generate_hierarchy_diagram sia stato chiamato
        mock_generate.assert_called_once()

    @patch("devnotes.cli.render_mermaid_diagram")
    def test_cli_diagram_with_render(self, mock_render):
        """Verifica che il comando CLI diagram con --render funzioni correttamente"""
        # Configuriamo il mock per render_mermaid_diagram
        mock_render.return_value = True

        # Inizializziamo il progetto
        self.runner.invoke(app_cli, ["init"])

        # Eseguiamo il comando diagram tasks con --render
        result = self.runner.invoke(app_cli, ["diagram", "tasks", "--render"])
        self.assertEqual(result.exit_code, 0)

        # Verifichiamo che render_mermaid_diagram sia stato chiamato
        mock_render.assert_called_once()

    @patch("devnotes.cli.render_mermaid_diagram")
    def test_cli_render(self, mock_render):
        """Verifica che il comando CLI render funzioni correttamente"""
        # Configuriamo il mock per render_mermaid_diagram
        mock_render.return_value = True

        # Inizializziamo il progetto
        self.runner.invoke(app_cli, ["init"])

        # Creiamo un file mermaid di esempio
        os.makedirs(".project", exist_ok=True)
        with open(os.path.join(".project", "test.mmd"), "w") as f:
            f.write("graph TD\n    A-->B")

        # Eseguiamo il comando render
        result = self.runner.invoke(app_cli, ["render", "--path", ".project/test.mmd"])
        self.assertEqual(result.exit_code, 0)

        # Verifichiamo che render_mermaid_diagram sia stato chiamato con i parametri corretti
        mock_render.assert_called_once_with(".project/test.mmd", True)


if __name__ == "__main__":
    unittest.main()
