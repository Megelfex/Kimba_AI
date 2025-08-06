import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QScrollArea
from PyQt6.QtCore import Qt
from datetime import datetime

# Pfad zum Projektstamm
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Core imports
from core.persona_manager import PersonaManager
from core.llm_router import KimbaLLMRouter
import core.longterm_memory as memory

# Dev tools
from tools.project_analyzer import analyze_report
from tools.proposal_handler import ProposalHandler
from tools.file_editor import read_file, create_file

# === Chat Bubble Widget ===
class ChatBubble(QWidget):
    def __init__(self, sender, text):
        super().__init__()
        layout = QHBoxLayout()
        label = QLabel(text)
        label.setWordWrap(True)

        bubble_color = '#1e1e1e'
        text_color = '#90ee90'

        label.setStyleSheet(f"""
            padding: 8px;
            border-radius: 6px;
            background-color: {bubble_color};
            color: {text_color};
            font-size: 14px;
        """)

        if sender in ["Iuno", "Augusta"]:
            layout.addWidget(label)
            layout.addStretch()
        else:
            layout.addStretch()
            layout.addWidget(label)
        self.setLayout(layout)

# === Main Window ===
class KimbaV2Chat(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kimba AI v2 – Chat & Dev Mode")
        self.resize(900, 650)

        # Core Systeme
        self.persona_manager = PersonaManager()
        self.llm = KimbaLLMRouter()

        # Nur Iuno laden
        self.persona_manager.load_persona("persona_iuno_local")
        self.active_persona = "Iuno"

        # GUI Layout
        self.chat_area_layout = QVBoxLayout()
        self.chat_area_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.chat_area_layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_widget)

        self.input_field = QTextEdit()
        self.input_field.setFixedHeight(50)
        self.input_field.setStyleSheet("""
            background-color: #1e1e1e;
            color: #90ee90;
            border: 1px solid #333;
            border-radius: 6px;
            padding: 6px;
            font-size: 14px;
        """)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_send)
        self.send_button.setStyleSheet("""
            background-color: #2e2e2e;
            color: #90ee90;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
        """)

        layout = QVBoxLayout()
        layout.addWidget(scroll)
        layout.addWidget(self.input_field)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

        self.setStyleSheet("background-color: #121212;")

        self.add_message("System", "Welcome to Kimba AI v2. Type !augusta to enter Dev Mode, or !iuno to switch back to Chat.")

    def add_message(self, sender, text):
        bubble = ChatBubble(sender, text)
        self.chat_area_layout.addWidget(bubble)

    def handle_send(self):
        user_text = self.input_field.toPlainText().strip()
        if not user_text:
            return
        self.input_field.clear()
        self.add_message("You", user_text)

        # Persona-Switching
        if user_text.lower() == "!augusta":
            self.persona_manager.load_persona("persona_augusta")
            self.active_persona = "Augusta"
            self.add_message("System", "Switched to Augusta (Dev Mode).")
            return
        elif user_text.lower() == "!iuno":
            self.active_persona = "Iuno"
            self.add_message("System", "Switched to Iuno (Chat Mode).")
            return

        # Speicheraktion (Memory speichern)
        memory.add_memory(
            content=user_text,
            mood="neutral",
            category="user_input",
            tags=[self.active_persona]
        )

        # Dev-Befehl verarbeiten
        if self.active_persona == "Augusta" and user_text.startswith("dev:"):
            self.handle_dev_command(user_text[4:].strip())
            return

        # Antwort generieren
        response = self.llm.ask_persona(self.active_persona, user_text)
        self.add_message(self.active_persona, response)

        # Antwort speichern
        memory.add_memory(
            content=response,
            mood="neutral",
            category="persona_response",
            tags=[self.active_persona]
        )

    def handle_dev_command(self, command):
        if command == "analyze_project":
            result = analyze_report()
            self.add_message("Augusta", result)
        elif command == "list_proposals":
            proposals = ProposalHandler()
            self.add_message("Augusta", "\n".join(proposals))
        elif command.startswith("read_file "):
            filepath = command.replace("read_file ", "").strip()
            try:
                content = read_file(filepath)
                self.add_message("Augusta", f"Contents of {filepath}:\n\n{content[:1000]}...")
            except Exception as e:
                self.add_message("Augusta", f"Error: {str(e)}")
        elif command.startswith("edit_file "):
            parts = command.split(" ", 2)
            if len(parts) < 3:
                self.add_message("Augusta", "Usage: dev:edit_file <path> <new_content>")
                return
            filepath, new_content = parts[1], parts[2]
            try:
                create_file(filepath, new_content)
                self.add_message("Augusta", f"✅ File {filepath} updated.")
            except Exception as e:
                self.add_message("Augusta", f"Error: {str(e)}")
        else:
            self.add_message("Augusta", f"Unknown dev command: {command}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KimbaV2Chat()
    window.show()
    sys.exit(app.exec())
