import os
import json
import time

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Kimba_AI root
REPORT_FILE = os.path.join(PROJECT_DIR, "project_analysis.json")

# Dateiendungen, die wir als "sinnlos" betrachten
TRASH_EXTENSIONS = {".log", ".tmp", ".cache", ".pyc", ".pyo"}
TRASH_DIRS = {"__pycache__", ".pytest_cache", ".idea", ".vscode", "build", "dist"}

# Alter in Sekunden (6 Monate)
OLD_FILE_THRESHOLD = 60 * 60 * 24 * 30 * 6

def scan_project():
    print(f"[INFO] 🔍 Scanne Projektordner: {PROJECT_DIR}")
    file_data = []
    all_files = []

    # Alle Dateien sammeln
    for root, dirs, files in os.walk(PROJECT_DIR):
        for f in files:
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, PROJECT_DIR)
            size = os.path.getsize(path)
            mtime = os.path.getmtime(path)
            ext = os.path.splitext(f)[1].lower()
            all_files.append({
                "path": rel_path,
                "size": size,
                "mtime": mtime,
                "ext": ext
            })

    # Dateien in Kategorien einteilen
    sinnlos = []
    nicht_genutzt = []
    veraltet = []

    # Für Nicht-genutzt: Referenzen im gesamten Projekttext suchen
    project_text = ""
    for file in all_files:
        try:
            if file["ext"] in {".py", ".txt", ".json", ".md"}:
                with open(os.path.join(PROJECT_DIR, file["path"]), "r", encoding="utf-8", errors="ignore") as f:
                    project_text += f.read() + "\n"
        except:
            pass

    for file in all_files:
        # Sinnlos-Kriterien
        if file["ext"] in TRASH_EXTENSIONS or any(d in file["path"] for d in TRASH_DIRS):
            sinnlos.append(file["path"])
            continue

        # Nicht genutzt
        filename = os.path.basename(file["path"])
        if filename not in project_text:
            nicht_genutzt.append(file["path"])

        # Veraltet
        if (time.time() - file["mtime"]) > OLD_FILE_THRESHOLD and filename not in project_text:
            veraltet.append(file["path"])

    report = {
        "sinnlos": sorted(set(sinnlos)),
        "nicht_genutzt": sorted(set(nicht_genutzt)),
        "veraltet": sorted(set(veraltet))
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"[INFO] 📄 Analyse abgeschlossen. Report gespeichert unter {REPORT_FILE}")
    return report

if __name__ == "__main__":
    result = scan_project()
    print(json.dumps(result, indent=2, ensure_ascii=False))
