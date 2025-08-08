import os
import json
import time

# Projektbasis & Report-Datei
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Kimba_AI root
REPORT_FILE = os.path.join(PROJECT_DIR, "project_analysis.json")

# Ausschlusslisten
TRASH_EXTENSIONS = {".log", ".tmp", ".cache", ".pyc", ".pyo"}
TRASH_DIRS = {"__pycache__", ".pytest_cache", ".idea", ".vscode", "build", "dist", "archive", "models"}
IGNORED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".mp3", ".mp4", ".wav"}  # Binärdateien nicht lesen

# Alter in Sekunden (6 Monate)
OLD_FILE_THRESHOLD = 60 * 60 * 24 * 30 * 6

def scan_project():
    print(f"[INFO] 🔍 Scanne Projektordner: {PROJECT_DIR}")
    all_files = []
    project_text = ""

    # Alle Dateien sammeln
    for root, dirs, files in os.walk(PROJECT_DIR):
        dirs[:] = [d for d in dirs if d not in TRASH_DIRS]  # Ignorierte Ordner ausfiltern
        for f in files:
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, PROJECT_DIR)
            ext = os.path.splitext(f)[1].lower()

            try:
                size = os.path.getsize(path)
                mtime = os.path.getmtime(path)
            except OSError:
                continue

            file_info = {
                "path": rel_path,
                "size_bytes": size,
                "last_modified": time.ctime(mtime),
                "mtime": mtime,
                "ext": ext
            }

            all_files.append(file_info)

            # Textinhalt nur für relevante Dateien sammeln
            if ext not in IGNORED_EXTENSIONS and ext in {".py", ".txt", ".json", ".md"}:
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        project_text += content + "\n"

                        # Zusätzliche Infos
                        file_info["todo_count"] = content.count("TODO")
                        file_info["fixme_count"] = content.count("FIXME")
                        file_info["is_empty"] = len(content.strip()) == 0 or content.strip() == "pass"

                except Exception as e:
                    file_info["error"] = str(e)

    # Dateien in Kategorien einteilen
    sinnlos = []
    nicht_genutzt = []
    veraltet = []

    for file in all_files:
        filename = os.path.basename(file["path"])

        # Sinnlos-Kriterien
        if file["ext"] in TRASH_EXTENSIONS:
            sinnlos.append(file["path"])
            continue

        # Nicht genutzt
        if filename not in project_text:
            nicht_genutzt.append(file["path"])

        # Veraltet
        if (time.time() - file["mtime"]) > OLD_FILE_THRESHOLD and filename not in project_text:
            veraltet.append(file["path"])

    report = {
        "summary": {
            "total_files": len(all_files),
            "sinnlos_count": len(sinnlos),
            "nicht_genutzt_count": len(nicht_genutzt),
            "veraltet_count": len(veraltet)
        },
        "sinnlos": sorted(set(sinnlos)),
        "nicht_genutzt": sorted(set(nicht_genutzt)),
        "veraltet": sorted(set(veraltet)),
        "files": all_files
    }

    # Ergebnis speichern
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"[INFO] 📄 Analyse abgeschlossen – Report gespeichert unter {REPORT_FILE}")
    return report

if __name__ == "__main__":
    result = scan_project()
    print(json.dumps(result, indent=2, ensure_ascii=False))
