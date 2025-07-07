
# Kimba vX – Upgrade mit integrierter v5-Logik

Dies ist die weiterentwickelte Version von Kimba v5, erweitert um klare Modulstruktur, neue Tools und Soulmate-Logik.

## 📁 Hauptstruktur:
- `core/` – Denklogik und Langzeitgedächtnis
- `gui/` – Benutzeroberfläche mit Gradio
- `tools/` – Websuche, Sprachmodule, Bildgenerator
- `memory/` – Gesprächs- und Reflexionsspeicher
- `identity/` – Werte, Persönlichkeit, Ziele
- `config/` – Betriebsmodi, Einstellungen
- `data/` – Kreativdaten, Bildideen

## ✅ Integrierte Erweiterungen:
- Ollama-Unterstützung (lokales LLM)
- JSON-gestützte Identitätsstruktur
- Platzhalter für Bild- & Spracherweiterung
- Verbesserte Modularisierung

## 🛠 Nächster Schritt:
1. Virtuelle Umgebung einrichten:
   `python3 -m venv venv && source venv/bin/activate`
2. Abhängigkeiten installieren:
   `pip install -r requirements.txt`
3. Kimba starten:
   `python3 Kimba_AI_vX.py` oder über `gui/interface.py`
