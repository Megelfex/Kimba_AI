import json
import os
import time

# Speicherort für Analyse-Ergebnisse
REPORT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "project_analysis.json"))

def scan_project(root_path=None):
    """
    Durchsucht den Projektordner und erstellt einen Analyse-Report.
    Erkennt:
      - unnötige Dateien (Backup, Temp, Cache)
      - ungenutzte Dateien (keine Referenz im Code)
      - veraltete Dateien (älter als 1 Jahr)
    """
    if root_path is None:
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    sinnlos_ext = [".tmp", ".log", ".bak", ".old"]
    sinnlos_namen = ["__pycache__", ".DS_Store", "Thumbs.db"]

    all_files = []
    sinnlos = []
    nicht_genutzt = []
    veraltet = []

    # 1. Alle Dateien sammeln
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Cache-Ordner überspringen
        dirnames[:] = [d for d in dirnames if d not in ["__pycache__", ".git", ".venv"]]
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, root_path)
            ext = os.path.splitext(filename)[1].lower()

            file_info = {
                "path": rel_path,
                "size": os.path.getsize(file_path),
                "mtime": os.path.getmtime(file_path)
            }
            all_files.append(file_info)

            # 2. Sinnlose Dateien erkennen
            if ext in sinnlos_ext or filename in sinnlos_namen:
                sinnlos.append(rel_path)

            # 3. Veraltete Dateien (älter als 365 Tage)
            if time.time() - file_info["mtime"] > 365 * 24 * 60 * 60:
                veraltet.append(rel_path)

    # 4. Referenzen prüfen – sehr simple Variante:
    #    Wenn eine .py-Datei nicht in irgendeinem anderen File importiert wird → "nicht genutzt"
    py_files = [f["path"] for f in all_files if f["path"].endswith(".py")]
    file_contents = {}
    for f in py_files:
        try:
            with open(os.path.join(root_path, f), "r", encoding="utf-8") as src:
                file_contents[f] = src.read()
        except Exception:
            file_contents[f] = ""

    for f in py_files:
        basename = os.path.splitext(os.path.basename(f))[0]
        used = False
        for other_f, content in file_contents.items():
            if f != other_f and (f"import {basename}" in content or f"from {basename}" in content):
                used = True
                break
        if not used:
            nicht_genutzt.append(f)

    # 5. Zusammenfassung speichern
    report_data = {
        "summary": {
            "total_files": len(all_files),
            "total_py_files": len(py_files),
        },
        "files": all_files,
        "sinnlos": sinnlos,
        "nicht_genutzt": nicht_genutzt,
        "veraltet": veraltet
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    return f"✅ Projektanalyse abgeschlossen. {len(all_files)} Dateien gescannt."

def analyze_report():
    if not os.path.exists(REPORT_FILE):
        return "⚠️ Kein Analyse-Report gefunden. Bitte zuerst 'scan_project()' ausführen."

    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary = data.get("summary", {})
    sinnlos = data.get("sinnlos", [])
    nicht_genutzt = data.get("nicht_genutzt", [])
    veraltet = data.get("veraltet", [])
    files = data.get("files", [])

    # 1. Grundlegende Beobachtungen
    observations = [
        f"📊 Projektübersicht: {summary.get('total_files', 0)} Dateien gescannt.",
        f"🗑️ {len(sinnlos)} potenziell unnötige Dateien.",
        f"📂 {len(nicht_genutzt)} ungenutzte Dateien.",
        f"⏳ {len(veraltet)} veraltete Dateien."
    ]

    # 2. Beispiele nennen
    if sinnlos:
        observations.append(f"🗑️ Beispiele unnötiger Dateien: {', '.join(sinnlos[:3])}...")
    if nicht_genutzt:
        observations.append(f"📂 Beispiele ungenutzter Dateien: {', '.join(nicht_genutzt[:3])}...")
    if veraltet:
        observations.append(f"⏳ Beispiele veralteter Dateien: {', '.join(veraltet[:3])}...")

    # 3. Spezifische Feature-Lücken finden
    missing_features = []
    filenames = [os.path.basename(f["path"]).lower() for f in files]

    if not any("cat" in name or "kimba" in name for name in filenames):
        missing_features.append("🐾 Keine visuelle Katze Kimba gefunden.")

    if not any("iuno" in name for name in filenames):
        missing_features.append("🌙 Keine Chibi-Iuno-Assets oder Code gefunden.")

    if not any("overlay" in name or "desktop" in name for name in filenames):
        missing_features.append("🖼️ Kein Desktop-Overlay-Client gefunden.")

    if missing_features:
        observations.append("🚧 Fehlende Kernfunktionen:")
        observations.extend(missing_features)

    # 4. Priorisierungsvorschläge
    priorities = []
    if missing_features:
        priorities.extend(missing_features)
    if veraltet:
        priorities.append("🔄 Alte, ungenutzte Dateien aufräumen.")
    if sinnlos:
        priorities.append("🧹 Sinnlose Dateien entfernen oder archivieren.")

    # Format für KI-Dialog
    persona_message = "Hier ist, was ich über unser Projekt herausgefunden habe:\n" + "\n".join(observations)
    if priorities:
        persona_message += "\n\n✨ Vorschläge, was wir als Nächstes tun könnten:\n" + "\n".join(f"- {p}" for p in priorities)

    return persona_message

if __name__ == "__main__":
    # Falls direkt ausgeführt → zuerst scannen, dann berichten
    print(scan_project())
    print(analyze_report())
