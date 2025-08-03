import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel
)
from PyQt6.QtCore import Qt
from datetime import datetime, timedelta
from core.llm_router import KimbaLLMRouter

# Avatar-Bilder
IUNO_AVATAR = "./assets/iuno_avatar.png"
USER_AVATAR = "./assets/user_avatar.png"

# Individuelle Reset-Tage (1 = 1. des Monats, 5 = 5. des Monats, etc.)
API_RESET_DAYS = {
    "HuggingFace": 5,
    "DeepInfra": 10,
    "OpenRouter": 1
}

class KimbaApp(QMainWindow):
    def __init__(self, router):
        super().__init__()
        self.setWindowTitle("Kimba AI - Iuno v1")
        self.setGeometry(200, 100, 900, 650)
        self.setStyleSheet("background-color: #121212; color: white; font-family: Arial;")

        self.router = router

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # ----- Info-Bar -----
        info_bar = QHBoxLayout()
        self.api_toggle = QPushButton("API Mode: AUTO")
        self.api_toggle.setEnabled(False)
        self.api_toggle.setStyleSheet("""
            QPushButton {
                background-color: #1f1f1f;
                color: white;
                padding: 5px 10px;
                border-radius: 6px;
            }
        """)
        info_bar.addWidget(self.api_toggle)

        self.token_label = QLabel()
        self.token_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.token_label.setStyleSheet("""
            background-color: #1f1f1f;
            color: white;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 12px;
        """)
        info_bar.addWidget(self.token_label)

        layout.addLayout(info_bar)

        # ----- Chatfenster -----
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            background-color: #1e1e1e;
            font-size: 14px;
            border: none;
        """)
        layout.addWidget(self.chat_display)

        # ----- Eingabezeile -----
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Schreibe hier an Iuno...")
        self.input_field.setStyleSheet("""
            background-color: #2b2b2b;
            color: white;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid #444;
        """)
        self.send_button = QPushButton("Senden")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4d79ff;
                color: white;
                padding: 8px 14px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3c5fd1;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        self.append_system_message("✅ Iuno geladen! API-Fallback aktiv.")
        self.update_token_display()

    def days_until_reset(self, reset_day: int) -> int:
        today = datetime.today()
        this_month_reset = datetime(today.year, today.month, reset_day)

        if today < this_month_reset:
            return (this_month_reset - today).days
        else:
            # Nächster Monat
            next_month = today.month + 1 if today.month < 12 else 1
            year = today.year if today.month < 12 else today.year + 1
            next_reset = datetime(year, next_month, reset_day)
            return (next_reset - today).days

    def update_token_display(self):
        usage_texts = []

        for api in self.router.api_chain:
            name = api["name"]
            used = self.router.api_usage.get(name, 0)
            limit = api["limit"]
            reset_day = API_RESET_DAYS.get(name, 1)
            days_left = self.days_until_reset(reset_day)

            percent = (used / limit) * 100 if limit > 0 else 0
            color = "green"
            if percent >= 80:
                color = "red"
            elif percent >= 50:
                color = "orange"

            usage_texts.append(
                f"<span style='color:{color}'>{name}: {used}/{limit} Tokens</span> "
                f"<span style='color:gray'>(Reset in {days_left} Tagen)</span>"
            )

        model_info = f"<span style='color:cyan;'>Modell: {self.router.hf_model_id}</span>"
        self.token_label.setText(" | ".join(usage_texts) + " | " + model_info)

    # -------- Chatblasen mit Avataren --------
    def append_user_message(self, text):
        bubble_html = f"""
        <div style="text-align: right; margin: 8px;">
            <span style="display: inline-flex; align-items: center; justify-content: flex-end;">
                <span style="
                    background-color: #ff4d4d;
                    color: white;
                    padding: 10px 14px;
                    border-radius: 15px;
                    max-width: 60%;
                    word-wrap: break-word;
                    margin-right: 8px;">
                    {text}
                </span>
                <img src="{USER_AVATAR}" width="36" height="36" style="border-radius: 50%;">
            </span>
        </div>
        """
        self.chat_display.append(bubble_html)

    def append_iuno_message(self, text):
        bubble_html = f"""
        <div style="text-align: left; margin: 8px;">
            <span style="display: inline-flex; align-items: center;">
                <img src="{IUNO_AVATAR}" width="36" height="36" style="border-radius: 50%; margin-right: 8px;">
                <span style="
                    background-color: #4d79ff;
                    color: white;
                    padding: 10px 14px;
                    border-radius: 15px;
                    max-width: 60%;
                    word-wrap: break-word;">
                    {text}
                </span>
            </span>
        </div>
        """
        self.chat_display.append(bubble_html)

    def append_system_message(self, text):
        self.chat_display.append(f"<p style='color:gray; font-size:12px;'><i>{text}</i></p>")

    # -------- Senden & Empfangen --------
    def send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return

        self.append_user_message(user_text)
        self.input_field.clear()

        try:
            response, source = self.router.ask(user_text, return_source=True)
        except Exception as e:
            response = f"[Fehler: {str(e)}]"
            source = "ERROR"

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
