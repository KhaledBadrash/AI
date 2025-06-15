# utils/validation.py

def validate_program(name: str, hardcoded: dict) -> bool:
    """
    Prüft, ob der gegebene Studiengang in den hart codierten Programmen enthalten ist.
    """
    return name in hardcoded

def validate_id(matrikelnummer: str) -> bool:
    """
    Einfache Prüfung der Matrikelnummer: nur Ziffern, Länge 5–12.
    """
    return matrikelnummer.isdigit() and 5 <= len(matrikelnummer) <= 12
