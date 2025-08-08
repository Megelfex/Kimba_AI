import sys
import threading
import subprocess
import socket
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime
from core.llm_router import KimbaLLMRouter
from modules.image_router import KimbaImageRouter
from modules import vision
from core.persona_manager import PersonaManager
from core.longterm_memory import add_memory
from core.memory_filter import is_relevant_message
from src.kimba_ai.services.startup_loop import start_all_background_services
from services.auto_overlay_mood import register_user_activity
from modules.live_vision import (
    start_live_vision_in_background,
    stop_live_vision,
    set_reaction_callback
)

# API Reset-Tage
API_RESET_DAYS = {
    "OpenAI GPT": 1,
    "HuggingFace": 5,
    "DeepInfra": 10,
    "OpenRouter": 1
}

def categorize_message(user_input: str):
    """Kategorisiert die Nachricht für Speicher- und Trigger-Logik."""
    text_lower = user_input.lower()
    if any(word in text_lower for word in ["mache", "baue", "erstelle", "füge hinzu", "implementiere"]):
        return "task", ["entwicklung"]
    if any(word in text_lower for word in ["ja", "okay", "mach das", "bestätige", "genehmige"]):
        return "decision", ["approval"]
    if any(word in text_lower for word in ["nein", "nicht machen", "abbrechen", "stop"]):
        return "decision", ["rejected"]
    return "general", ["notiz"]

class KimbaApp(QMainWindow):
    response_ready = pyqtSignal(str, str)
    system_message_ready = pyqtSignal(str)

    def __init__(self, router):
        super().__init__()
        self.setWindowTitle("Kimba AI - Iuno v1 + Kimba Katze")
        self.setGeometry(200, 100, 900, 650)
        self.setStyleSheet("background-color: #121212; color: white; font-family: Arial;")

        # 🔹 PersonaManager einbinden
        self.persona_manager = PersonaManager()
        self.router = router

        self.image_router = KimbaImageRouter()
        self.vision_handler = vision.KimbaVision(vision_api="gpt4o", api_key=None)

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

        # 🔹 Label für aktive Persona
        self.persona_label = QLabel(f"Aktive Persona: {self.persona_manager.get_active_prompt()[:30]}...")
        self.persona_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_bar.addWidget(self.persona_label)

        self.token_label = QLabel()
        self.token_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        info_bar.addWidget(self.token_label)
        layout.addLayout(info_bar)

        # Chatfenster
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Eingabe
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Schreibe hier an Iuno...")
        self.send_button = QPushButton("Senden")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        # Startmeldung
        self.append_system_message("✅ Iuno und Kimba Katze geladen!")
        self.update_token_display()

        # 🎯 Hintergrunddienste starten
        self.append_system_message("✅ Starte Hintergrunddienste...")
        start_all_background_services()

        # 🎯 Live-Vision Callback setzen
        set_reaction_callback(self.display_live_vision_reaction)

        # 🎯 Beide Overlays starten
        threading.Thread(target=self.start_overlay_client, args=("iuno",), daemon=True).start()
        threading.Thread(target=self.start_overlay_client, args=("kimba",), daemon=True).start()

    def start_overlay_client(self, character):
        """Startet einen Overlay-Client für einen bestimmten Charakter."""
        overlay_path = os.path.join(os.path.dirname(__file__), "..", "overlay_client", "overlay_client.py")
        if os.path.exists(overlay_path):
            subprocess.Popen([sys.executable, overlay_path, character])
        else:
            print(f"[WARN] Overlay-Client nicht gefunden unter: {overlay_path}")

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
        if self.vision_mode:
            start_live_vision_in_background()
        else:
            stop_live_vision()
        self.vision_toggle.setText("Vision-Modus: AN" if self.vision_mode else "Vision-Modus: AUS")

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
        for api, limit in {a["name"]: a["limit"] for a in self.router.api_chain}.items():
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

    def append_user_message(self, text):
        self.chat_display.append(f"<p style='color:#ff4d4d;'><b>Du:</b> {text}</p>")

    def append_iuno_message(self, text):
        self.chat_display.append(f"<p style='color:#4d79ff;'><b>Iuno:</b> {text}</p>")

    def append_system_message(self, text):
        self.chat_display.append(f"<p style='color:gray; font-size:12px;'><i>{text}</i></p>")

    def display_live_vision_reaction(self, text):
        """Zeigt Live-Vision-Reaktionen direkt im Chatfenster."""
        self.append_iuno_message(text)

    def send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return

        # 🔹 Persona-Wechsel per Chatbefehl
        if user_text.startswith("!persona "):
            persona_name = user_text.replace("!persona ", "").strip()
            try:
                msg = self.persona_manager.switch_persona(persona_name)
                self.persona_label.setText(f"Aktive Persona: {persona_name}")
                self.append_system_message(msg)
            except ValueError as e:
                self.append_system_message(str(e))
            self.input_field.clear()
            return

        # Nutzeraktivität registrieren (für Idle/Mood-System)
        register_user_activity()

        # Langzeitgedächtnis speichern
        if is_relevant_message(user_text):
            category, tags = categorize_message(user_text)
            add_memory(content=user_text, category=category, tags=tags)

        # Chat anzeigen
        self.append_user_message(user_text)
        self.input_field.clear()
        self.system_message_ready.emit("💭 Iuno denkt nach...")

        # Animationstrigger setzen
        self.trigger_animations(user_text)

        def worker():
            try:
                if self.api_mode == 0:
                    response, source = self.router.ask_local(user_text), "LOCAL"
                elif self.api_mode == 1:
                    response, source = self.router.ask(user_text, return_source=True)
                else:
                    response = self.router.ask_api(user_text)
                    source = "API"
            except Exception as e:
                response, source = f"[Fehler: {str(e)}]", "ERROR"
            self.response_ready.emit(response, source)

        threading.Thread(target=worker, daemon=True).start()

    def trigger_animations(self, user_text):
        """Einfache Regel-Engine für beide Charaktere."""
        text_lower = user_text.lower()

        # Iuno reagiert auf Gespräch
        if "hallo" in text_lower or "hi" in text_lower:
            self.set_character_mood("iuno", "happy")
        elif "traurig" in text_lower:
            self.set_character_mood("iuno", "sad")
        else:
            self.set_character_mood("iuno", "speak")

        # Kimba Katze reagiert unabhängig
        if "streichel" in text_lower:
            self.set_character_mood("kimba", "happy")
        elif "schlaf" in text_lower:
            self.set_character_mood("kimba", "sleep")
        elif "böse" in text_lower:
            self.set_character_mood("kimba", "angry")
        else:
            self.set_character_mood("kimba", "idle")

    def set_character_mood(self, character, animation):
        """Setzt Animation und speichert sie ins Gedächtnis."""
        self.send_overlay_command(character, animation)
        add_memory(
            content=f"{character} Animation geändert auf {animation}",
            mood=animation,
            category="mood",
            tags=[character]
        )

    def send_overlay_command(self, character, animation):
        """Schickt einen Animationswechsel an den Overlay-Client."""
        port = 5001 if character == "iuno" else 5002
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", port))
            s.sendall(animation.encode())
            s.close()
            print(f"[Overlay-Command] {character} → {animation}")
        except ConnectionRefusedError:
            print(f"[WARN] Kein Overlay für {character} aktiv.")

    def on_response_received(self, response, source):
        self.append_system_message(f"DEBUG: Antwortquelle: {source}")
        self.append_iuno_message(response)
        self.update_token_display()

if __name__ == "__main__":
    print("[INFO] 🧠 Lade Iuno und Kimba Katze...")
    router = KimbaLLMRouter(model_choice="Phi-3-mini-4k-instruct")
    app = QApplication(sys.argv)
    window = KimbaApp(router)
    window.show()
    sys.exit(app.exec())
