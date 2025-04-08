"""
Modulo di utilità condivise tra i vari moduli
"""


def sanitize_for_mermaid(text):
    """
    Sanitizza il testo per l'uso in diagrammi Mermaid.

    Args:
        text: Il testo da sanitizzare

    Returns:
        Il testo sanitizzato
    """
    if not text:
        return ""

    # Utilizziamo un approccio diverso per evitare problemi con le entità HTML
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        if char == "&":
            result.append("&amp;")
        elif char == ":":
            result.append("&#58;")
        elif char == '"':
            result.append("&quot;")
        elif char == "[":
            result.append("&#91;")
        elif char == "]":
            result.append("&#93;")
        elif char == "{":
            result.append("&#123;")
        elif char == "}":
            result.append("&#125;")
        elif char == "(":
            result.append("&#40;")
        elif char == ")":
            result.append("&#41;")
        elif char == "<":
            result.append("&lt;")
        elif char == ">":
            result.append("&gt;")
        elif char == "#":
            result.append("&#35;")
        elif char == "|":
            result.append("&#124;")
        elif char == "`":
            result.append("&#96;")
        elif char == "\\":
            result.append("&#92;")
        elif char == "\n":
            result.append(" ")
        else:
            result.append(char)
        i += 1

    text = "".join(result)

    # Riduci gli spazi multipli a uno solo
    while "  " in text:
        text = text.replace("  ", " ")

    return text
