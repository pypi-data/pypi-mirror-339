"""
Test di debug per l'estrazione di task dai commenti
"""

import os
import tempfile

from devnotes.analyzer import extract_tasks_from_comments

def test_debug_extraction():
    """Test di debug per l'estrazione dei task dai commenti"""
    # Creiamo un file temporaneo con task nei commenti
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as f:
        f.write("""
# Un commento normale
# #TASK: Questo non è un task valido (ha uno spazio prima)

#TASK: Implementare la funzione di test
def test_function():
    \"\"\"Questa è una funzione di test\"\"\"
    #TASK(bug,high): Correggere il bug in questa funzione
    return "test"

class TestClass:
    \"\"\"Questa è una classe di test\"\"\"
    
    #TASK(feature): Aggiungere nuova funzionalità
    def test_method(self):
        \"\"\"Questo è un metodo di test\"\"\"
        return "test method"
""")
        temp_file = f.name

    try:
        # Eseguiamo la funzione da testare
        tasks = extract_tasks_from_comments(temp_file)
        
        # Stampiamo i risultati per debug
        print(f"Numero di task estratti: {len(tasks)}")
        for i, task in enumerate(tasks, 1):
            print(f"Task {i}:")
            print(f"  Titolo: {task['title']}")
            print(f"  File: {task['file']}")
            print(f"  Linea: {task['line']}")
            print(f"  Symbol: {task['symbol']}")
            print(f"  Tags: {task['tags']}")
            print()
    finally:
        # Pulizia
        os.unlink(temp_file)

if __name__ == "__main__":
    test_debug_extraction()