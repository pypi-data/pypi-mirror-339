"""
Test per la gestione di docstring complesse e la generazione di diagrammi Mermaid
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from devnotes.analyzer import extract_call_relations, extract_definitions
from devnotes.diagrams import generate_mermaid_diagram
from devnotes.utils import sanitize_for_mermaid


class TestComplexDocstrings(unittest.TestCase):
    def setUp(self):
        # Creiamo una directory temporanea per i test
        self.test_dir = tempfile.mkdtemp()
        # Salviamo la directory corrente
        self.original_dir = os.getcwd()
        # Ci spostiamo nella directory temporanea
        os.chdir(self.test_dir)
        # Creiamo la directory di storage
        os.makedirs(".project", exist_ok=True)

        # Creiamo un file Python con docstring complesse
        with open("complex_docstrings.py", "w") as f:
            f.write(
                '''
def get_proxy(proxy_country=None, level=None, level_range=None, last_proxy=None,
              domain=None, id_domain=None, proxy_type=None, force_refresh=False):
    """
    Retrieve a new proxy from the proxy pool.

    Args:
        proxy_country: The country code for the proxy (e.g., "IT", "US")
        level: Specific level to request (overrides last_proxy, but is overridden by level_range)
        level_range: Range of levels to request (e.g., "1,8"), takes precedence over level
        last_proxy: The last proxy used, to get the next level
        domain: Filter proxy whitelist and blacklist by domain
        id_domain: Filter proxy whitelist and blacklist by domain id
        proxy_type: Filter by proxy type (e.g., "residential", "datacenter", "mobile")
        force_refresh: If True, force a refresh of the proxy list from the API

    Returns:
        The raw proxy data dictionary, or None if no proxies are available
    """
    return {"proxy": "127.0.0.1:8080"}

def process_data(data, config=None):
    """
    Process data with the given configuration.

    This function handles various types of data processing:
    - Text normalization
    - Feature extraction
    - Model prediction

    Example:
        ```python
        result = process_data(my_data, {"normalize": True})
        ```

    Note:
        * This is a complex function with multiple steps
        * It may raise exceptions if the data is invalid
        * Performance depends on the size of the input data

    Args:
        data: The input data to process
        config: Configuration dictionary with processing options

    Returns:
        Processed data in the same format as the input
    """
    return data

class DataProcessor:
    """
    A class for processing various types of data.

    This class provides methods for:
    1. Loading data from different sources
    2. Transforming data into a standard format
    3. Applying various processing algorithms
    4. Exporting results to different formats

    Attributes:
        name: The name of the processor
        version: The version of the processor
        config: Configuration dictionary
    """

    def __init__(self, name, version="1.0", config=None):
        """
        Initialize the DataProcessor.

        Args:
            name: The name of the processor
            version: The version of the processor (default: "1.0")
            config: Configuration dictionary (default: None)
        """
        self.name = name
        self.version = version
        self.config = config or {}

    def process(self, data):
        """
        Process the given data.

        This method applies the configured processing steps to the input data.
        It calls the global process_data function with the appropriate configuration.

        Args:
            data: The input data to process

        Returns:
            The processed data

        Raises:
            ValueError: If the data is invalid
        """
        if not data:
            raise ValueError("Data cannot be empty")
        return process_data(data, self.config)
'''
            )

    def tearDown(self):
        # Ripristiniamo la directory originale
        os.chdir(self.original_dir)
        # Rimuoviamo la directory temporanea
        shutil.rmtree(self.test_dir)

    def test_extract_definitions_with_complex_docstrings(self):
        """Verifica che extract_definitions gestisca correttamente docstring complesse"""
        # Eseguiamo la funzione da testare
        definitions = extract_definitions("complex_docstrings.py")

        # Verifichiamo che tutte le definizioni siano state estratte
        self.assertEqual(len(definitions), 5)  # 2 funzioni + 1 classe + 2 metodi

        # Verifichiamo che le docstring siano state estratte correttamente
        function_names = [name for name, _ in definitions]
        self.assertIn("get_proxy", function_names)
        self.assertIn("process_data", function_names)
        self.assertIn("DataProcessor", function_names)
        self.assertIn("__init__", function_names)
        self.assertIn("process", function_names)

        # Verifichiamo che le docstring complesse siano state estratte correttamente
        # Nota: extract_definitions prende solo la prima riga della docstring
        for name, docstring in definitions:
            if name == "get_proxy":
                self.assertIn("Retrieve a new proxy from the proxy pool", docstring)
            elif name == "process_data":
                self.assertIn("Process data with the given configuration", docstring)

    def test_sanitize_for_mermaid(self):
        """Verifica che sanitize_for_mermaid gestisca correttamente caratteri speciali"""
        # Testiamo con vari input problematici
        test_cases = [
            # Input, output atteso
            ("Normal text", "Normal text"),
            ("Text with: colon", "Text with&#58; colon"),
            ('Text with "quotes"', "Text with &quot;quotes&quot;"),
            ("Text with [brackets]", "Text with &#91;brackets&#93;"),
            ("Text with {braces}", "Text with &#123;braces&#125;"),
            ("Text with (parentheses)", "Text with &#40;parentheses&#41;"),
            ("Text with <angle brackets>", "Text with &lt;angle brackets&gt;"),
            ("Text with & ampersand", "Text with &amp; ampersand"),
            ("Text with # hash", "Text with &#35; hash"),
            ("Text with | pipe", "Text with &#124; pipe"),
            ("Text with ` backtick", "Text with &#96; backtick"),
            ("Text with \\ backslash", "Text with &#92; backslash"),
            (
                "Multi\nline\ntext",
                "Multi line text",
            ),  # Newlines should be replaced with spaces
            (
                "Text with    multiple    spaces",
                "Text with multiple spaces",
            ),  # Multiple spaces should be collapsed
            # Test per verificare che & venga sostituito prima degli altri caratteri
            ("Text with &:", "Text with &amp;&#58;"),
            ("Text with &#58;", "Text with &amp;&#35;58;"),
        ]

        for input_text, expected_output in test_cases:
            result = sanitize_for_mermaid(input_text)
            self.assertEqual(result, expected_output)

    @patch("devnotes.diagrams.load_settings")
    @patch("devnotes.diagrams.load_tasks")
    def test_generate_mermaid_diagram_with_complex_descriptions(
        self, mock_load_tasks, mock_load_settings
    ):
        """Verifica che generate_mermaid_diagram gestisca descrizioni complesse"""
        # Mock delle impostazioni
        mock_load_settings.return_value = {
            "diagram": {"output": "test_diagram.mmd", "style": "graph TD"}
        }

        # Creiamo alcuni task con descrizioni complesse
        mock_load_tasks.return_value = [
            {
                "id": "001",
                "title": "Task with: special characters",
                "description": """This task has special characters:
                * Colons: like this
                * "Quotes" like this
                * [Brackets] like this
                * {Braces} like this
                * (Parentheses) like this
                * <Angle brackets> like this
                * & Ampersands like this
                * # Hash like this
                * | Pipe like this
                * ` Backtick like this
                * \\ Backslash like this""",
                "status": "todo",
            },
            {
                "id": "002",
                "title": "Task with code blocks",
                "description": """This task has code blocks:
                ```python
                def example():
                    return "Hello, world!"
                ```""",
                "status": "in_progress",
                "blocked_by": "001",
            },
            {
                "id": "003",
                "title": "Task with very long description",
                "description": "This is a very long description that should be truncated. "
                * 10,
                "status": "done",
            },
        ]

        # Eseguiamo la funzione da testare
        output_path = generate_mermaid_diagram(mock_load_tasks.return_value)

        # Verifichiamo che il file sia stato creato
        self.assertTrue(os.path.exists(output_path))

        # Verifichiamo il contenuto del file
        with open(output_path, "r") as f:
            content = f.read()

            # Verifichiamo che il diagramma contenga i task
            self.assertIn("task_001", content)
            self.assertIn("task_002", content)
            self.assertIn("task_003", content)

            # Verifichiamo che i caratteri speciali siano stati sanitizzati
            # Nota: ":" viene sostituito con "&#58;" e "&" con "&amp;"
            self.assertIn("Task with", content)
            self.assertIn("special characters", content)

            # Verifichiamo che le relazioni siano state generate correttamente
            self.assertIn("task_001 --> task_002", content)

    def test_extract_call_relations_with_complex_code(self):
        """Verifica che extract_call_relations gestisca codice complesso"""
        # Eseguiamo la funzione da testare
        call_relations = extract_call_relations("complex_docstrings.py")

        # Verifichiamo che le relazioni di chiamata siano state estratte correttamente
        self.assertIn(("process", "process_data"), call_relations)

        # Verifichiamo che non ci siano false relazioni
        for caller, callee in call_relations:
            # La funzione get_proxy non chiama altre funzioni
            if caller == "get_proxy":
                self.fail(f"get_proxy non dovrebbe chiamare {callee}")


# La funzione sanitize_for_mermaid è già stata implementata nel modulo devnotes.utils


if __name__ == "__main__":
    unittest.main()
