"""
🧪 auto_tester.py
EN: Automated testing for generated Kimba modules. Validates syntax, structure, docstrings.
DE: Automatisiertes Testen generierter Kimba-Module – prüft Syntax, Struktur, Docstrings.
"""

import ast
import os

def test_module(path):
    """
    Testet ein einzelnes Python-Modul auf grundlegende Eigenschaften.
    """
    results = {"syntax_ok": False, "has_docstrings": False, "functions_found": 0}
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)
        results["syntax_ok"] = True
        results["functions_found"] = len([n for n in tree.body if isinstance(n, ast.FunctionDef)])
        results["has_docstrings"] = any(ast.get_docstring(n) for n in tree.body if isinstance(n, ast.FunctionDef))

    except Exception as e:
        results["error"] = str(e)

    return results

def test_all(folder="proposals/generated_modules"):
    """
    Testet alle Module im Ordner und zeigt Ergebnisse.
    """
    print("🧪 Testlauf für neue Module ...")
    for file in os.listdir(folder):
        if file.endswith(".py"):
            path = os.path.join(folder, file)
            res = test_module(path)
            print(f"🔍 {file}: {res}")

if __name__ == "__main__":
    test_all()
