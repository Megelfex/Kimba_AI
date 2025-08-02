import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QComboBox, QTextEdit, QLineEdit
)
from core.llm_router import KimbaLLMRouter


class KimbaApp(QMainWindow):
    def __init__(self, router):
        super().__init__()
        self.setWindowTitle("Kimba AI - Desktop App")
        self.setGeometry(200, 100, 800, 600)

        # Übergebenes LLM Router Objekt (Modell ist schon geladen)
        self.router = router
        self.current_purpose = "core"

        # GUI Elemente
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Modell-Auswahl
        model_layout = QHBoxLayout()
        self.model_select = QComboBox()
        self.model_select.addItems(["core"])
        model_layout.addWidget(self.model_select)

        self.api_toggle = QPushButton("API Mode: OFF")
        self.api_toggle.setCheckable(True)
        self.api_toggle.clicked.connect(self.toggle_api_mode)
        model_layout.addWidget(self.api_toggle)
        layout.addLayout(model_layout)

        # Chat Anzeige
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Eingabefeld + Senden
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.send_button = QPushButton("Senden")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        self.append_message("System", "✅ Modell geladen! Du kannst jetzt mit Kimba sprechen.")

    def toggle_api_mode(self):
        if self.api_toggle.isChecked():
            self.api_toggle.setText("API Mode: ON")
        else:
            self.api_toggle.setText("API Mode: OFF")

    def append_message(self, sender, text):
        self.chat_display.append(f"<b>{sender}:</b> {text}")

    def send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return

        self.append_message("You", user_text)
        self.input_field.clear()

        response = self.router.ask(user_text)
        self.append_message("Kimba", response)


if __name__ == "__main__":
    print("[INFO] 🧠 Lade Modell im Hauptthread...")
    router = KimbaLLMRouter()
    router.load_model()

    app = QApplication(sys.argv)
    window = KimbaApp(router)
    window.show()
    sys.exit(app.exec())
