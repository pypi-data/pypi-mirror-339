"""
Test di integrazione per il modulo di analisi del codice
"""

import os
import unittest
import tempfile
import shutil
import yaml
from unittest.mock import patch

from devnotes.analyzer import (
    scan_project_structure, generate_call_graph,
    generate_hierarchical_mermaid, extract_structure_hierarchy
)
from devnotes.config import STORAGE_DIR


class TestAnalyzerIntegration(unittest.TestCase):
    def setUp(self):
        # Creiamo una directory temporanea per i test
        self.test_dir = tempfile.mkdtemp()
        # Salviamo la directory corrente
        self.original_dir = os.getcwd()
        # Ci spostiamo nella directory temporanea
        os.chdir(self.test_dir)
        # Patchamo la costante STORAGE_DIR per usare un percorso relativo
        self.storage_patcher = patch('devnotes.config.STORAGE_DIR', '.project')
        self.storage_patcher.start()
        
        # Creiamo una struttura di file Python di esempio
        os.makedirs("src", exist_ok=True)
        os.makedirs(".project", exist_ok=True)
        
        # File con funzioni che si chiamano tra loro
        with open(os.path.join("src", "module1.py"), "w") as f:
            f.write("""
def function1():
    \"\"\"This is function1\"\"\"
    return function2()

def function2():
    \"\"\"This is function2\"\"\"
    return "Hello"
""")
        
        # File con una classe e metodi
        with open(os.path.join("src", "module2.py"), "w") as f:
            f.write("""
class TestClass:
    \"\"\"This is a test class\"\"\"
    
    def method1(self):
        \"\"\"This is method1\"\"\"
        from src.module1 import function1
        return function1()
    
    def method2(self):
        \"\"\"This is method2\"\"\"
        return self.method1()
""")
        
    def tearDown(self):
        # Ripristiniamo la directory originale
        os.chdir(self.original_dir)
        # Rimuoviamo la directory temporanea
        shutil.rmtree(self.test_dir)
        # Stoppiamo il patch
        self.storage_patcher.stop()
    
    def test_scan_project_structure(self):
        """Verifica che scan_project_structure analizzi correttamente la struttura del progetto"""
        # Eseguiamo la funzione da testare
        with patch('devnotes.analyzer.console.print'):
            structure = scan_project_structure()
        
        # Verifichiamo che la struttura contenga i file corretti
        self.assertIn("src/module1.py", structure)
        self.assertIn("src/module2.py", structure)
        
        # Verifichiamo che le definizioni siano state estratte correttamente
        module1_defs = structure["src/module1.py"]
        self.assertEqual(len(module1_defs), 2)
        self.assertIn(("function1", "This is function1"), module1_defs)
        self.assertIn(("function2", "This is function2"), module1_defs)
        
        module2_defs = structure["src/module2.py"]
        self.assertEqual(len(module2_defs), 3)
        self.assertIn(("TestClass", "This is a test class"), module2_defs)
        self.assertIn(("method1", "This is method1"), module2_defs)
        self.assertIn(("method2", "This is method2"), module2_defs)
        
        # Verifichiamo che i file YAML siano stati creati
        self.assertTrue(os.path.exists(os.path.join(".project", "structure.yaml")))
        self.assertTrue(os.path.exists(os.path.join(".project", "calls.yaml")))
        
        # Verifichiamo il contenuto del file structure.yaml
        with open(os.path.join(".project", "structure.yaml"), "r") as f:
            saved_structure = yaml.safe_load(f)

            # YAML converte le tuple in liste, quindi dobbiamo confrontare i valori in modo diverso
            self.assertEqual(set(saved_structure.keys()), set(structure.keys()))

            for file_path, defs in structure.items():
                saved_defs = saved_structure[file_path]
                self.assertEqual(len(saved_defs), len(defs))

                # Convertiamo le tuple in liste per il confronto
                defs_as_lists = [list(d) for d in defs]
                for def_item in defs_as_lists:
                    self.assertIn(def_item, saved_defs)
    
    def test_generate_call_graph(self):
        """Verifica che generate_call_graph generi correttamente il grafo delle chiamate"""
        # Eseguiamo la funzione da testare
        with patch('devnotes.analyzer.console.print'):
            generate_call_graph()
        
        # Verifichiamo che il file del grafo sia stato creato
        self.assertTrue(os.path.exists(os.path.join(".project", "call_graph.mmd")))
        
        # Verifichiamo il contenuto del file
        with open(os.path.join(".project", "call_graph.mmd"), "r") as f:
            content = f.read()
            self.assertIn("graph TD", content)
            # Verifichiamo che contenga le funzioni
            self.assertIn("function1", content)
            self.assertIn("function2", content)
    
    def test_extract_structure_hierarchy(self):
        """Verifica che extract_structure_hierarchy estragga correttamente la gerarchia strutturale"""
        # Eseguiamo la funzione da testare
        hierarchy = extract_structure_hierarchy(os.path.join("src", "module2.py"))
        
        # Verifichiamo che la gerarchia contenga le definizioni corrette
        self.assertEqual(len(hierarchy), 3)
        
        # Verifichiamo che la classe sia stata estratta correttamente
        class_item = next((item for item in hierarchy if item[0] == "class"), None)
        self.assertIsNotNone(class_item)
        self.assertEqual(class_item[1], "TestClass")
        self.assertEqual(class_item[2], "This is a test class")
        
        # Verifichiamo che i metodi siano stati estratti correttamente
        method_items = [item for item in hierarchy if item[0] == "method"]
        self.assertEqual(len(method_items), 2)
        
        method_names = [item[1] for item in method_items]
        self.assertIn("method1", method_names)
        self.assertIn("method2", method_names)
        
        # Verifichiamo che i metodi siano associati alla classe corretta
        for method_item in method_items:
            self.assertEqual(method_item[3], "TestClass")
    
    def test_generate_hierarchical_mermaid(self):
        """Verifica che generate_hierarchical_mermaid generi correttamente il diagramma gerarchico"""
        # Eseguiamo la funzione da testare
        with patch('devnotes.analyzer.console.print'):
            generate_hierarchical_mermaid()
        
        # Verifichiamo che il file del diagramma sia stato creato
        self.assertTrue(os.path.exists(os.path.join(".project", "structure_graph.mmd")))
        
        # Verifichiamo il contenuto del file
        with open(os.path.join(".project", "structure_graph.mmd"), "r") as f:
            content = f.read()
            self.assertIn("graph TD", content)
            # Verifichiamo che contenga le classi e i metodi
            self.assertIn("TestClass", content)
            self.assertIn("method1", content)
            self.assertIn("method2", content)
            # Verifichiamo che contenga le funzioni
            self.assertIn("function1", content)
            self.assertIn("function2", content)


if __name__ == '__main__':
    unittest.main()