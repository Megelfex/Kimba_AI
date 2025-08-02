"""
Kimba Desktop App - Vollintegration
===================================
- Startet ComfyUI automatisch, falls nicht aktiv
- Nutzt nur ein lokales Hauptmodell (LLM) + GPT/Claude-Fallback
- Erkennt automatisch Bildanfragen und wählt passendes Bildmodell
- Zeigt generierte Bilder direkt im Chat an
"""

import sys
import logging
import subprocess
import socket
import time
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QComboBox, QLabel
)

# Kimba Core
from core.llm_router import KimbaLLMRouter
from modules.image_generator import generate_image_with_comfy

# Logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# --- ComfyUI Auto-Start ---
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

import os

def find_comfyui_path():
    """
    Sucht den ComfyUI-Ordner automatisch:
    - Prüft zuerst im gleichen Verzeichnis wie Kimba
    - Falls nicht gefunden, versucht im übergeordneten Ordner
    """
    base_dir = Path(__file__).resolve().parent
    possible_paths = [
        base_dir / "ComfyUI",
        base_dir.parent / "ComfyUI"
    ]
    for path in possible_paths:
        if (path / "main.py").exists():
            return str(path)
    return None


def start_comfyui():
    comfy_path = find_comfyui_path()
    if not comfy_path:
        logging.error("❌ Konnte ComfyUI-Ordner nicht finden! Bitte prüfe, ob 'main.py' existiert.")
        return

    if not is_port_in_use(8188):
        logging.info(f"🚀 Starte ComfyUI aus: {comfy_path}")
        try:
            subprocess.Popen(
                ["python", "main.py"],
                cwd=comfy_path,
                shell=True
            )
            time.sleep(5)  # Warte, bis ComfyUI hochfährt
        except Exception as e:
            logging.error(f"❌ Fehler beim Start von ComfyUI: {e}")
    else:
        logging.info("✅ ComfyUI läuft bereits.")


class KimbaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kimba AI - Desktop App")
        self.setGeometry(200, 100, 800, 600)

        # ComfyUI starten
        start_comfyui()

        # Router für LLM & API
        self.router = KimbaLLMRouter()
        self.current_purpose = "core"

        # Modelle: Nur LLM + Bildmodelle aus ComfyUI
        self.llm_models = ["core", "gpt", "claude"]
        self.image_models = [m.stem for m in Path("ComfyUI/models/checkpoints").glob("*.safetensors")]

        self._build_ui()

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Modell-Auswahl Dropdown
        model_layout = QHBoxLayout()
        self.model_select = QComboBox()
        self.model_select.addItems(self.llm_models + self.image_models)
        self.model_select.currentTextChanged.connect(self.change_model)
        model_layout.addWidget(QLabel("Select Model:"))
        model_layout.addWidget(self.model_select)

        # API Toggle
        self.api_button = QPushButton("API Mode: OFF")
        self.api_button.setStyleSheet("background-color: red; color: white;")
        self.api_button.clicked.connect(self.toggle_api)
        model_layout.addWidget(self.api_button)
        layout.addLayout(model_layout)

        # Chat Anzeige
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Eingabezeile + Senden Button
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Schreibe hier an Kimba...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        send_button = QPushButton("Senden")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)
        layout.addLayout(input_layout)

    def change_model(self, model_name):
        self.current_purpose = model_name
        if model_name == "gpt":
            self.router.use_api = True
            self.router.api_choice = "gpt"
            self.router._init_api_clients()
        elif model_name == "claude":
            self.router.use_api = True
            self.router.api_choice = "claude"
            self.router._init_api_clients()
        else:
            self.router.use_api = False
        self.add_message("System", f"Modell gewechselt zu: {model_name}")

    def toggle_api(self):
        self.router.use_api = not self.router.use_api
        if self.router.use_api:
            self.api_button.setText("API Mode: ON")
            self.api_button.setStyleSheet("background-color: green; color: white;")
        else:
            self.api_button.setText("API Mode: OFF")
            self.api_button.setStyleSheet("background-color: red; color: white;")
        self.add_message("System", f"API-Modus ist jetzt {'aktiv' if self.router.use_api else 'inaktiv'}.")

    def send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return

        self.add_message("You", user_text)
        self.input_field.clear()

        # --- Auto-Erkennung für Bild-Generierung ---
        image_keywords = ["erstelle ein bild", "male", "zeichne", "generiere bild", "render", "create image", "draw", "generate picture"]

        style_to_model = {
            "ghibli": "ghibli-style",
            "anime": "anime-style",
            "realistisch": "realistic-style",
            "cyberpunk": "cyberpunk-style",
            "pixel": "pixel-art",
            "fantasy": "fantasy-style"
        }

        if any(kw in user_text.lower() for kw in image_keywords):
            selected_model = None
            for style, model_name in style_to_model.items():
                if style in user_text.lower() and model_name in self.image_models:
                    selected_model = model_name
                    break

            if not selected_model and self.image_models:
                selected_model = self.image_models[0]

            if selected_model:
                self.add_message("System", f"🎨 Erkenne Bildanfrage – benutze Modell: {selected_model}")
                result_path = generate_image_with_comfy(
                    user_text,
                    model_name=selected_model,
                    workflow_path="default_workflow.json"
                )
                self.add_image_message("Kimba", result_path)
                return
            else:
                self.add_message("System", "❌ Kein passendes Bildmodell gefunden.")
                return

        # --- Normales LLM/API-Handling ---
        response = self.router.ask(user_text, purpose=self.current_purpose)
        self.add_message("Kimba", response)

    def add_message(self, sender, text):
        self.chat_display.append(f"<b>{sender}:</b> {text}")
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )

    def add_image_message(self, sender, image_path):
        self.chat_display.append(f"<b>{sender}:</b>")
        self.chat_display.insertHtml(f'<br><img src="{image_path}" width="400"><br>')
        self.chat_display.append(f"📁 Gespeichert unter: {image_path}")
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KimbaApp()
    window.show()
    sys.exit(app.exec())
