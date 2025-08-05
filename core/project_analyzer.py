import json
import os

REPORT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "project_analysis.json"))

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
    print(analyze_report())
