"""
Test per il modulo analyzer.py
"""

import os
import shutil
import tempfile
import unittest

from devnotes.analyzer import (
    extract_call_relations,
    extract_defined_names,
    extract_definitions,
)


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        # Creiamo una directory temporanea per i test
        self.test_dir = tempfile.mkdtemp()
        # Salviamo la directory corrente
        self.original_dir = os.getcwd()
        # Ci spostiamo nella directory temporanea
        os.chdir(self.test_dir)

        # Creiamo un file Python di esempio per i test
        self.test_file = os.path.join(self.test_dir, "test_module.py")
        with open(self.test_file, "w") as f:
            f.write(
                """
def function1():
    \"\"\"This is function1\"\"\"
    return function2()

def function2():
    \"\"\"This is function2\"\"\"
    return "Hello"

class TestClass:
    \"\"\"This is a test class\"\"\"

    def method1(self):
        \"\"\"This is method1\"\"\"
        return function1()

    def method2(self):
        \"\"\"This is method2\"\"\"
        return self.method1()
"""
            )

    def tearDown(self):
        # Ripristiniamo la directory originale
        os.chdir(self.original_dir)
        # Rimuoviamo la directory temporanea
        shutil.rmtree(self.test_dir)

    def test_extract_definitions(self):
        """Verifica che extract_definitions estragga correttamente le definizioni"""
        # Eseguiamo la funzione da testare
        definitions = extract_definitions(self.test_file)

        # Verifichiamo che tutte le definizioni siano state estratte
        self.assertEqual(len(definitions), 5)

        # Verifichiamo che le definizioni contengano i nomi corretti
        names = [name for name, _ in definitions]
        self.assertIn("function1", names)
        self.assertIn("function2", names)
        self.assertIn("TestClass", names)
        self.assertIn("method1", names)
        self.assertIn("method2", names)

        # Verifichiamo che le definizioni contengano le docstring corrette
        docs = {name: doc for name, doc in definitions}
        self.assertEqual(docs["function1"], "This is function1")
        self.assertEqual(docs["function2"], "This is function2")
        self.assertEqual(docs["TestClass"], "This is a test class")
        self.assertEqual(docs["method1"], "This is method1")
        self.assertEqual(docs["method2"], "This is method2")

    def test_extract_defined_names(self):
        """Verifica che extract_defined_names estragga i nomi delle funzioni"""
        # Eseguiamo la funzione da testare
        names = extract_defined_names(self.test_file)

        # Verifichiamo che tutti i nomi siano stati estratti
        self.assertEqual(len(names), 4)

        # Verifichiamo che i nomi siano corretti
        self.assertIn("function1", names)
        self.assertIn("function2", names)
        self.assertIn("method1", names)
        self.assertIn("method2", names)

    def test_extract_call_relations(self):
        """Verifica che extract_call_relations estragga le relazioni di chiamata"""
        # Definiamo le funzioni conosciute
        defined_funcs = {"function1", "function2", "method1", "method2"}

        # Eseguiamo la funzione da testare
        calls = extract_call_relations(self.test_file, defined_funcs)

        # Verifichiamo che tutte le chiamate siano state estratte
        # Nota: le chiamate ai metodi di classe non vengono rilevate in questo test semplificato
        self.assertIn(("function1", "function2"), calls)
        self.assertIn(("method1", "function1"), calls)


# Aggiungi altri test per le altre funzioni del modulo analyzer.py
# Ad esempio, potresti voler testare scan_project_structure, generate_call_graph, generate_hierarchical_mermaid
# Questi test richiederebbero un maggiore uso di mock e file temporanei


if __name__ == "__main__":
    unittest.main()
