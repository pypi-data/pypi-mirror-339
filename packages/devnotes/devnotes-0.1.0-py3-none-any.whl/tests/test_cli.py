"""
Test per il modulo cli.py
"""

import unittest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from devnotes.cli import app_cli


class TestCli(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
    
    @patch('devnotes.cli.ensure_storage')
    def test_init_command(self, mock_ensure_storage):
        """Verifica che il comando init funzioni correttamente"""
        # Eseguiamo il comando
        result = self.runner.invoke(app_cli, ["init"])
        
        # Verifichiamo che il comando sia stato eseguito con successo
        self.assertEqual(result.exit_code, 0)
        
        # Verifichiamo che ensure_storage sia stato chiamato
        mock_ensure_storage.assert_called_once()
        
        # Verifichiamo che il messaggio di output sia corretto
        self.assertIn("Progetto inizializzato", result.stdout)
    
    @patch('devnotes.cli.update_settings')
    def test_update_command(self, mock_update_settings):
        """Verifica che il comando update funzioni correttamente"""
        # Eseguiamo il comando
        result = self.runner.invoke(app_cli, ["update"])
        
        # Verifichiamo che il comando sia stato eseguito con successo
        self.assertEqual(result.exit_code, 0)
        
        # Verifichiamo che update_settings sia stato chiamato
        mock_update_settings.assert_called_once()
    
    @patch('devnotes.cli.display_tasks')
    def test_task_list_command(self, mock_display_tasks):
        """Verifica che il comando task_list funzioni correttamente"""
        # Eseguiamo il comando
        result = self.runner.invoke(app_cli, ["task-list"])
        
        # Verifichiamo che il comando sia stato eseguito con successo
        self.assertEqual(result.exit_code, 0)
        
        # Verifichiamo che display_tasks sia stato chiamato
        mock_display_tasks.assert_called_once()
    
    @patch('devnotes.cli.mark_task_done')
    def test_task_done_command(self, mock_mark_task_done):
        """Verifica che il comando task_done funzioni correttamente"""
        # Eseguiamo il comando
        result = self.runner.invoke(app_cli, ["task-done", "001"])
        
        # Verifichiamo che il comando sia stato eseguito con successo
        self.assertEqual(result.exit_code, 0)
        
        # Verifichiamo che mark_task_done sia stato chiamato con l'ID corretto
        mock_mark_task_done.assert_called_once_with("001")


# Aggiungi altri test per gli altri comandi CLI
# Ad esempio, potresti voler testare task_add_interactive, task_edit, scan, diagram_generate, ecc.
# Questi test richiederebbero un maggiore uso di mock per simulare l'interazione con l'utente


if __name__ == '__main__':
    unittest.main()