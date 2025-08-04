import sys
import threading
import json
import os
import subprocess
import shutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel,
    QDialog, QListWidget, QFileDialog, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime
from core.llm_router import KimbaLLMRouter
from core.image_router import KimbaImageRouter
from core import project_manager, file_editor, vision  # Vision importieren

# Avatar-Bilder
IUNO_AVATAR = "./assets/iuno_avatar.png"
USER_AVATAR = "./assets/user_avatar.png"

API_RESET_DAYS = {
    "HuggingFace": 5,
    "DeepInfra": 10,
    "OpenRouter": 1,
    "OpenAI GPT": 1
}

class KimbaApp(QMainWindow):
    response_ready = pyqtSignal(str, str)
    system_message_ready = pyqtSignal(str)

    def __init__(self, router):
        super().__init__()
        self.setWindowTitle("Kimba AI - Iuno v1")
        self.setGeometry(200, 100, 900, 650)
        self.setStyleSheet("background-color: #121212; color: white; font-family: Arial;")

        self.router = router
        self.image_router = KimbaImageRouter()
        self.vision_handler = vision.KimbaVision(vision_api="gpt4o", api_key=os.getenv("OPENAI_API_KEY"))
        self.api_mode = 1
        self.image_mode = False
        self.vision_mode = False

        self.response_ready.connect(self.on_response_received)
        self.system_message_ready.connect(self.append_system_message)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Info-Bar
        info_bar = QHBoxLayout()
        self.api_toggle = QPushButton(self.get_api_mode_label())
        self.api_toggle.clicked.connect(self.toggle_api_mode)
        info_bar.addWidget(self.api_toggle)

        self.image_toggle = QPushButton("Bildmodus: AUS")
        self.image_toggle.clicked.connect(self.toggle_image_mode)
        info_bar.addWidget(self.image_toggle)

        self.vision_toggle = QPushButton("Vision-Modus: AUS")
        self.vision_toggle.clicked.connect(self.toggle_vision_mode)
        info_bar.addWidget(self.vision_toggle)

        self.token_label = QLabel()
        self.token_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        info_bar.addWidget(self.token_label)

        layout.addLayout(info_bar)

        # Chatfenster
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Eingabefeld
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Schreibe hier an Iuno...")
        self.send_button = QPushButton("Senden")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        self.append_system_message("✅ Iuno geladen!")
        self.update_token_display()

    # =====================
    #    MODUS TOGGLES
    # =====================
    def get_api_mode_label(self):
        return f"API Mode: {['Nur Lokal', 'Lokal + API', 'Nur API'][self.api_mode]}"

    def toggle_api_mode(self):
        self.api_mode = (self.api_mode + 1) % 3
        self.api_toggle.setText(self.get_api_mode_label())

    def toggle_image_mode(self):
        self.image_mode = not self.image_mode
        self.image_toggle.setText("Bildmodus: AN" if self.image_mode else "Bildmodus: AUS")

    def toggle_vision_mode(self):
        self.vision_mode = not self.vision_mode
        self.vision_toggle.setText("Vision-Modus: AN" if self.vision_mode else "Vision-Modus: AUS")

    # =====================
    #    TOKEN-ANZEIGE
    # =====================
    def days_until_reset(self, reset_day: int) -> int:
        today = datetime.today()
        this_month_reset = datetime(today.year, today.month, reset_day)
        if today < this_month_reset:
            return (this_month_reset - today).days
        else:
            next_month = today.month + 1 if today.month < 12 else 1
            year = today.year if today.month < 12 else today.year + 1
            next_reset = datetime(year, next_month, reset_day)
            return (next_reset - today).days

    def update_token_display(self):
        usage_texts = []
        for api, limit in {**{a["name"]: a["limit"] for a in self.router.api_chain}, "OpenAI GPT": 50_000}.items():
            used = self.router.api_usage.get(api, 0)
            reset_day = API_RESET_DAYS.get(api, 1)
            days_left = self.days_until_reset(reset_day)
            percent = (used / limit) * 100 if limit > 0 else 0
            color = "green" if percent < 50 else "orange" if percent < 80 else "red"
            usage_texts.append(
                f"<span style='color:{color}'>{api}: {used}/{limit} Tokens</span> "
                f"<span style='color:gray'>(Reset in {days_left} Tagen)</span>"
            )
        self.token_label.setText(" | ".join(usage_texts))

    # =====================
    #    CHAT-FUNKTIONEN
    # =====================
    def append_user_message(self, text):
        self.chat_display.append(f"<p style='color:#ff4d4d;'><b>Du:</b> {text}</p>")

    def append_iuno_message(self, text):
        self.chat_display.append(f"<p style='color:#4d79ff;'><b>Iuno:</b> {text}</p>")

    def append_system_message(self, text):
        self.chat_display.append(f"<p style='color:gray; font-size:12px;'><i>{text}</i></p>")

    # =====================
    #    VISION HANDLER
    # =====================
    def handle_vision_request(self):
        self.append_system_message("📸 Erfasse aktuellen Bildschirm...")
        screenshot_path = self.vision_handler.capture_screenshot()
        self.append_system_message(f"Screenshot gespeichert: {screenshot_path}")
        self.append_system_message("🔍 Sende Bild an Vision-Modell...")
        desc = self.vision_handler.describe_screenshot(screenshot_path)
        self.append_iuno_message(desc)

    # =====================
    #    DATEI-BEFEHLE
    # =====================
    def handle_file_command(self, user_text):
        parts = user_text.split()
        cmd = parts[0].lower()

        try:
            if cmd == "erstelle" and parts[1] == "datei":
                path = parts[2]
                content = " ".join(parts[4:]) if "inhalt" in parts else ""
                result = file_editor.create_file(path, content)
                self.append_system_message(result)

            elif cmd == "ändere" and parts[1] == "zeile":
                line_num = int(parts[2])
                path = parts[4]
                new_content = " ".join(parts[6:])
                result = file_editor.edit_file_line(path, line_num, new_content)
                self.append_system_message(result)

            elif cmd == "ersetze":
                path = parts[2]
                search_text = parts[4].strip('"')
                replace_text_str = parts[6].strip('"')
                result = file_editor.replace_text(path, search_text, replace_text_str)
                self.append_system_message(result)

            elif cmd == "zeige" and parts[1] == "datei":
                path = parts[2]
                content = file_editor.read_file(path)
                self.append_iuno_message(f"<pre>{content}</pre>")

            elif cmd == "zeige" and parts[1] == "änderungen":
                log = file_editor.get_edit_log()
                self.append_iuno_message(json.dumps(log, indent=2, ensure_ascii=False))

            else:
                self.append_system_message("❌ Unbekannter Datei-Befehl.")

        except Exception as e:
            self.append_system_message(f"❌ Fehler bei Dateibefehl: {str(e)}")

    # =====================
    #    NACHRICHT SENDEN
    # =====================
    def send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return
        self.append_user_message(user_text)
        self.input_field.clear()

        # Vision-Befehl
        if "analysiere meinen bildschirm" in user_text.lower():
            self.handle_vision_request()
            return

        # Projektanalyse
        if "analysiere meinen projektordner" in user_text.lower():
            self.handle_project_analysis()
            return

        # Datei-Befehle
        if any(user_text.lower().startswith(cmd) for cmd in ["erstelle datei", "ändere zeile", "ersetze", "zeige datei", "zeige änderungen"]):
            self.handle_file_command(user_text)
            return

        # Bildmodus
        if self.image_mode or any(k in user_text.lower() for k in ["erstelle ein bild", "generiere ein bild", "zeige mir ein bild", "mache ein bild"]):
            self.handle_image_request(user_text)
            return

        # Standard LLM Anfrage
        self.system_message_ready.emit("💭 Iuno denkt nach...")

        def worker():
            try:
                if self.api_mode == 0:
                    response, source = self.router.ask_local(user_text), "LOCAL"
                elif self.api_mode == 1:
                    response, source = self.router.ask(user_text, return_source=True)
                else:
                    response, source = self.router.ask_api(user_text), "API"
            except Exception as e:
                response, source = f"[Fehler: {str(e)}]", "ERROR"
            self.response_ready.emit(response, source)

        threading.Thread(target=worker, daemon=True).start()

    def on_response_received(self, response, source):
        self.append_system_message(f"DEBUG: Antwortquelle: {source}")
        self.append_iuno_message(response)
        self.update_token_display()


if __name__ == "__main__":
    print("[INFO] 🧠 Lade Iuno...")
    router = KimbaLLMRouter(model_choice="qwen-3b-fp16")
    router.load_model()
    app = QApplication(sys.argv)
    window = KimbaApp(router)
    window.show()
    sys.exit(app.exec())
