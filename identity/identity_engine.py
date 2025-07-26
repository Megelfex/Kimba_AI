import json

def load_identity(path):
    """
    EN: Loads Kimba's identity profile from a given JSON file.
    This file may contain traits, values, personality settings, or behavioral rules.

    DE: Lädt Kimbas Identitätsprofil aus einer angegebenen JSON-Datei.
    Diese Datei kann Eigenschaften, Werte, Verhaltensregeln oder Persönlichkeitsparameter enthalten.

    Args:
        path (str): Path to the identity JSON file.

    Returns:
        dict: Dictionary containing Kimba's identity configuration.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
