"""
Test per il modulo tasks.py
"""

import unittest
from datetime import datetime, timedelta

from devnotes.tasks import parse_due_date


class TestTasks(unittest.TestCase):
    def test_parse_due_date_empty(self):
        """Verifica che parse_due_date restituisca None per input vuoti"""
        self.assertIsNone(parse_due_date(""))
        self.assertIsNone(parse_due_date("none"))
        self.assertIsNone(parse_due_date("None"))

    def test_parse_due_date_domani(self):
        """Verifica che parse_due_date gestisca correttamente 'domani'"""
        # Otteniamo la data di domani
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")

        # Testiamo la funzione
        result = parse_due_date("domani")

        # Verifichiamo che il risultato contenga la data di domani
        self.assertIsNotNone(result)
        self.assertTrue(tomorrow_str in result)

    def test_parse_due_date_tra_giorni(self):
        """Verifica che parse_due_date gestisca correttamente 'tra X giorni'"""
        # Otteniamo la data tra 5 giorni
        future_date = datetime.now() + timedelta(days=5)
        future_date_str = future_date.strftime("%Y-%m-%d")

        # Testiamo la funzione
        result = parse_due_date("tra 5 giorni")

        # Verifichiamo che il risultato contenga la data futura
        self.assertIsNotNone(result)
        self.assertTrue(future_date_str in result)

    def test_parse_due_date_iso(self):
        """Verifica che parse_due_date gestisca correttamente date in formato ISO"""
        # Data in formato ISO
        iso_date = "2025-12-31T23:59:59"

        # Testiamo la funzione
        result = parse_due_date(iso_date)

        # Verifichiamo che il risultato sia uguale all'input
        self.assertEqual(result, iso_date)

    def test_parse_due_date_human_readable(self):
        """Verifica che parse_due_date gestisca date in formato leggibile"""
        # Data in formato leggibile
        human_date = "31 dicembre 2025"

        # Testiamo la funzione
        result = parse_due_date(human_date)

        # Verifichiamo che il risultato contenga l'anno corretto
        self.assertIsNotNone(result)
        self.assertTrue("2025" in result)

    def test_parse_due_date_invalid(self):
        """Verifica che parse_due_date gestisca correttamente input non validi"""
        # Input non valido
        invalid_date = "questa non è una data"

        # Testiamo la funzione
        result = parse_due_date(invalid_date)

        # Verifichiamo che il risultato sia None
        self.assertIsNone(result)


# Aggiungi altri test per le altre funzioni del modulo tasks.py
# Ad esempio, potresti voler testare display_tasks, add_task_interactive,
# edit_task, mark_task_done
# Questi test richiederebbero un maggiore uso di mock per simulare
# l'interazione con l'utente


if __name__ == "__main__":
    unittest.main()
