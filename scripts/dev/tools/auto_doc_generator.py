import os
import openai  # Optional: kompatibel mit llama-cpp Wrapper
from datetime import datetime

DOC_STYLE_HEADER = """
# =============================================
# ✨ Auto-Generated Docstrings (DE + EN)
# Datei: {filename}
# Erstellt: {timestamp}
# =============================================
"""

def get_python_files(directory):
    """
    🔍 Scans a directory for .py files recursively.

    Args:
        directory (str): Path to base directory.

    Returns:
        list[str]: List of full paths to Python files.
    """
    py_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                py_files.append(os.path.join(root, file))
    return py_files

def generate_docstring(code, model="gpt-4"):
    """
    📄 Calls the LLM to generate bilingual docstrings for the given code.

    Args:
        code (str): Python code without docstrings.
        model (str): Model name (OpenAI or local API).

    Returns:
        str: Code with inserted docstrings (top + function).
    """
    prompt = f"""
You are an expert software documenter.
Read the following Python code and add professional, concise docstrings in **English and German** for all functions and classes.

Rules:
- Include short one-liner docstring at the top of each function (EN+DE)
- Don't modify logic or add new functions
- Format should follow the style: triple quotes with both languages
- Add a header comment to the top with file name and timestamp

Code:
{code}
    """

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return response.choices[0].message.content.strip()

def document_all(directory=".", dry_run=False):
    """
    📚 Processes all .py files in a directory and rewrites them with bilingual docstrings.

    Args:
        directory (str): Path to scan.
        dry_run (bool): If True, doesn't overwrite files.
    """
    files = get_python_files(directory)
    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            raw_code = f.read()

        documented_code = generate_docstring(raw_code)
        if not dry_run:
            with open(path, "w", encoding="utf-8") as f:
                f.write(documented_code)
            print(f"✅ Dokumentiert: {path}")
        else:
            print(f"[TEST] Würde dokumentieren: {path}")

# ▶️ Beispielstart
if __name__ == "__main__":
    document_all("modules", dry_run=False)
