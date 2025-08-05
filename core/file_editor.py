import os
import json
import shutil
from datetime import datetime

# Projektverzeichnis (eine Ebene über core/)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(os.path.dirname(__file__), "file_edit_log.json")
BACKUP_DIR = os.path.join(PROJECT_DIR, "_backups")

# --------------------------------------------------
# Hilfsfunktionen
# --------------------------------------------------

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

def _ensure_project_path(file_path):
    """Verhindert, dass versehentlich außerhalb des Projekts gearbeitet wird."""
    abs_path = os.path.abspath(file_path)
    if not abs_path.startswith(PROJECT_DIR):
        raise ValueError(f"🚫 Ungültiger Pfad außerhalb des Projekts: {file_path}")
    return abs_path

def _backup_file(file_path):
    """Erstellt eine Backup-Kopie der Datei."""
    if not os.path.exists(file_path):
        return None
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(
        BACKUP_DIR,
        f"{os.path.basename(file_path)}_{timestamp}.bak"
    )
    shutil.copy2(file_path, backup_path)
    return backup_path

# --------------------------------------------------
# Dateioperationen
# --------------------------------------------------

def create_file(file_path, content=""):
    """Erstellt eine neue Datei mit optionalem Inhalt."""
    abs_path = _ensure_project_path(file_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content)
    _log_action("create_file", abs_path, {"content": content})
    return f"📄 Datei erstellt: {abs_path}"

def append_to_file(file_path, content):
    """Hängt Text an eine bestehende Datei an."""
    abs_path = _ensure_project_path(file_path)
    if not os.path.exists(abs_path):
        return f"❌ Datei nicht gefunden: {abs_path}"
    _backup_file(abs_path)
    with open(abs_path, "a", encoding="utf-8") as f:
        f.write(content)
    _log_action("append_to_file", abs_path, {"content": content})
    return f"➕ Text angehängt an: {abs_path}"

def edit_file_line(file_path, line_number, new_content):
    """Bearbeitet eine bestimmte Zeile in einer Datei."""
    abs_path = _ensure_project_path(file_path)
    if not os.path.exists(abs_path):
        return f"❌ Datei nicht gefunden: {abs_path}"
    _backup_file(abs_path)

    with open(abs_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if line_number < 1 or line_number > len(lines):
        return f"❌ Ungültige Zeilennummer: {line_number} (Datei hat {len(lines)} Zeilen)"

    old_content = lines[line_number - 1].rstrip("\n")
    lines[line_number - 1] = new_content + "\n"

    with open(abs_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    _log_action("edit_file_line", abs_path, {
        "line_number": line_number,
        "old_content": old_content,
        "new_content": new_content
    })
    return f"✏️ Zeile {line_number} in {abs_path} geändert."

def replace_text(file_path, search_text, replace_text_str):
    """Ersetzt Text in einer Datei."""
    abs_path = _ensure_project_path(file_path)
    if not os.path.exists(abs_path):
        return f"❌ Datei nicht gefunden: {abs_path}"
    _backup_file(abs_path)

    with open(abs_path, "r", encoding="utf-8") as f:
        content = f.read()

    if search_text not in content:
        return f"ℹ️ Text nicht gefunden: '{search_text}'"

    new_content = content.replace(search_text, replace_text_str)

    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    _log_action("replace_text", abs_path, {
        "search_text": search_text,
        "replace_text": replace_text_str
    })
    return f"🔄 Text '{search_text}' durch '{replace_text_str}' ersetzt in {abs_path}"

def delete_file(file_path):
    """Löscht eine Datei (mit vorherigem Backup)."""
    abs_path = _ensure_project_path(file_path)
    if not os.path.exists(abs_path):
        return f"❌ Datei nicht gefunden: {abs_path}"
    backup_path = _backup_file(abs_path)
    os.remove(abs_path)
    _log_action("delete_file", abs_path, {"backup": backup_path})
    return f"🗑️ Datei gelöscht (Backup gespeichert unter {backup_path})"

def read_file(file_path):
    """Liest den Inhalt einer Datei."""
    abs_path = _ensure_project_path(file_path)
    if not os.path.exists(abs_path):
        return f"❌ Datei nicht gefunden: {abs_path}"
    with open(abs_path, "r", encoding="utf-8") as f:
        return f.read()

def get_edit_log():
    """Gibt das Änderungslog zurück."""
    return _load_log()
