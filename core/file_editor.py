import os
import json
from datetime import datetime

# Logdatei für Änderungen
LOG_FILE = os.path.join(os.path.dirname(__file__), "file_edit_log.json")

def _load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save_log(log_data):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

def _log_action(action_type, file_path, details):
    log_data = _load_log()
    log_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action_type,
        "file": file_path,
        "details": details
    }
    log_data.append(log_entry)
    _save_log(log_data)

def create_file(file_path, content=""):
    """Erstellt eine neue Datei mit optionalem Inhalt."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    _log_action("create_file", file_path, {"content": content})
    return f"📄 Datei erstellt: {file_path}"

def edit_file_line(file_path, line_number, new_content):
    """Bearbeitet eine bestimmte Zeile in einer Datei."""
    if not os.path.exists(file_path):
        return f"❌ Datei nicht gefunden: {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if line_number < 1 or line_number > len(lines):
        return f"❌ Ungültige Zeilennummer: {line_number} (Datei hat {len(lines)} Zeilen)"

    old_content = lines[line_number - 1].rstrip("\n")
    lines[line_number - 1] = new_content + "\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    _log_action("edit_file_line", file_path, {
        "line_number": line_number,
        "old_content": old_content,
        "new_content": new_content
    })

    return f"✏️ Zeile {line_number} in {file_path} geändert."

def replace_text(file_path, search_text, replace_text_str):
    """Ersetzt Text in einer Datei."""
    if not os.path.exists(file_path):
        return f"❌ Datei nicht gefunden: {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if search_text not in content:
        return f"ℹ️ Text nicht gefunden: '{search_text}'"

    new_content = content.replace(search_text, replace_text_str)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    _log_action("replace_text", file_path, {
        "search_text": search_text,
        "replace_text": replace_text_str
    })

    return f"🔄 Text '{search_text}' durch '{replace_text_str}' ersetzt in {file_path}"

def read_file(file_path):
    """Liest den Inhalt einer Datei."""
    if not os.path.exists(file_path):
        return f"❌ Datei nicht gefunden: {file_path}"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def get_edit_log():
    """Gibt das Änderungslog zurück."""
    return _load_log()
