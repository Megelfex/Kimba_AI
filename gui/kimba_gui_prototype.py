import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QScrollArea, QListWidget,
    QComboBox, QCheckBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QSplitter, QSizePolicy
from core.persona_manager import PersonaManager
from core.llm_router import KimbaLLMRouter
import core.longterm_memory as memory
import tiktoken

# === Persona Mapping ===
persona_map = {
    "Augusta": "persona_augusta",
    "Bella": "persona_bella",
    "Carlotta": "persona_carlotta",
    "Frieren": "persona_frieren",
    "Iuno (API)": "persona_iuno_api",
    "Iuno (Local)": "persona_iuno_local",
    "Kimba (Cat)": "persona_kimba_cat",
    "Lucy": "persona_lucy",
    "Luna": "persona_luna",
    "Mikasa": "persona_mikasa",
    "Milly": "persona_milly",
    "Nami": "persona_nami",
    "Phrolova": "persona_phrolova",
    "Shorekeeper": "persona_shorekeeper"
}

# === Chat Bubble ===
class ChatBubble(QWidget):
    def __init__(self, sender, text):
        super().__init__()
        layout = QHBoxLayout()
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet(f"""
            padding: 8px;
            border-radius: 6px;
            background-color: {'#1e1e1e' if sender != 'You' else '#2a2a2a'};
            color: #90ee90;
            font-size: 14px;
        """)
        if sender == "You":
            layout.addStretch()
            layout.addWidget(label)
        else:
            layout.addWidget(label)
            layout.addStretch()
        self.setLayout(layout)

# === Main App ===
class KimbaV3App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kimba Augusta – Dev Companion")
        self.resize(1100, 750)

        self.persona_manager = PersonaManager()
        self.llm = KimbaLLMRouter(self.persona_manager)

        # Set default persona
        self.active_persona = "Augusta"
        self.persona_manager.load_persona(persona_map[self.active_persona])

        # Layouts
        main_layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        center_panel = QVBoxLayout()
        right_panel = QVBoxLayout()

        # === LEFT PANEL ===
        
        # Neuer Datei-Explorer
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(os.getcwd()))
        self.tree.setColumnHidden(1, True)  # Größe ausblenden
        self.tree.setColumnHidden(2, True)  # Typ ausblenden
        self.tree.setColumnHidden(3, True)  # Datum ausblenden
        self.tree.clicked.connect(self.load_tree_file_preview)

        open_btn = QPushButton("Datei öffnen")
        open_btn.clicked.connect(self.open_file_dialog)

        self.preview = QLabel("Dateivorschau ...")
        self.preview.setStyleSheet("color: #90ee90")

        left_panel.addWidget(QLabel("📁 Projektdateien"))
        left_panel.addWidget(self.tree)  # oder wie dein QTreeView aktuell heißt
        left_panel.addWidget(open_btn)
        left_panel.addWidget(QLabel("📝 Vorschau"))
        left_panel.addWidget(self.preview)

        # === CENTER PANEL ===
        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.chat_area)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_widget)

        self.input_field = QTextEdit()
        self.input_field.setFixedHeight(50)

        send_btn = QPushButton("Senden")
        send_btn.clicked.connect(self.handle_send)

        analyze_btn = QPushButton("🔍 Datei analysieren")
        analyze_btn.clicked.connect(self.analyze_current_file)

        image_btn = QPushButton("🧠 DALL·E Bild erstellen")
        image_btn.clicked.connect(self.create_dalle_image)

        center_panel.addWidget(QLabel("💬 Chat mit Augusta"))
        center_panel.addWidget(scroll)
        center_panel.addWidget(self.input_field)
        center_panel.addWidget(send_btn)
        center_panel.addWidget(analyze_btn)
        center_panel.addWidget(image_btn)

        # === RIGHT PANEL ===
        self.persona_dropdown = QComboBox()
        self.persona_dropdown.addItems(persona_map.keys())
        self.persona_dropdown.setCurrentText("Augusta")
        self.persona_dropdown.currentTextChanged.connect(self.switch_persona)

        self.token_label = QLabel("Tokens verwendet: 0")

        right_panel.addWidget(QLabel("👤 Persona"))
        right_panel.addWidget(self.persona_dropdown)
        right_panel.addWidget(QLabel("⚙️ Modi"))
        right_panel.addWidget(QCheckBox("AutoSave"))
        right_panel.addWidget(QCheckBox("Debug Mode"))
        right_panel.addWidget(QCheckBox("CodeAssist"))
        right_panel.addWidget(QCheckBox("Explain Mode"))
        right_panel.addWidget(self.token_label)

        # === Final Layout ===
        # Vorschau-Komponenten
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setStyleSheet("color: #90ee90; background-color: #1e1e1e;")
        self.preview_image = QLabel()
        self.preview_image.setScaledContents(True)

        self.preview_text.hide()
        self.preview_image.hide()

        self.close_preview_btn = QPushButton("🗙 Vorschau schließen")
        self.close_preview_btn.clicked.connect(self.clear_preview)
        self.close_preview_btn.hide()

        # In Vorschau-Sektion einsetzen
        left_panel.addWidget(QLabel("📝 Vorschau"))
        left_panel.addWidget(self.preview_text)
        left_panel.addWidget(self.preview_image)
        left_panel.addWidget(self.close_preview_btn)


        # Panels als Widgets verpacken
        left_panel_widget = QWidget()
        left_panel_widget.setLayout(left_panel)
        left_panel_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        center_panel_widget = QWidget()
        center_panel_widget.setLayout(center_panel)
        center_panel_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        right_panel_widget = QWidget()
        right_panel_widget.setLayout(right_panel)
        right_panel_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        # QSplitter erzeugen
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setStyleSheet("QSplitter::handle { background-color: #333; }")

        # Widgets einfügen
        main_splitter.addWidget(left_panel_widget)
        main_splitter.addWidget(center_panel_widget)
        main_splitter.addWidget(right_panel_widget)

        # Startgrößen setzen (z. B. 200 / 600 / 200 px)
        main_splitter.setSizes([250, 850, 300])

        # In Hauptlayout einbetten
        main_layout = QHBoxLayout()
        main_layout.addWidget(main_splitter)
        self.setLayout(main_layout)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #121212; color: #90ee90;")
        self.current_file_path = None

    def populate_file_list(self):
        self.file_list.clear()
        for item in os.listdir("."):
            if os.path.isfile(item):
                self.file_list.addItem(item)

    def add_message(self, sender, text):
        bubble = ChatBubble(sender, text)
        self.chat_area.addWidget(bubble)

    def handle_send(self):
        user_text = self.input_field.toPlainText().strip()
        if not user_text:
            return
        self.input_field.clear()
        self.add_message("You", user_text)

        memory.add_memory(user_text, mood="neutral", category="user_input", tags=[self.active_persona])
        response = self.llm.ask_persona(self.active_persona, user_text)
        self.add_message(self.active_persona, response)
        memory.add_memory(response, mood="neutral", category="persona_response", tags=[self.active_persona])

        # Token-Zählung
        enc = tiktoken.encoding_for_model("gpt-4")
        total_tokens = len(enc.encode(user_text)) + len(enc.encode(response))
        self.token_label.setText(f"Tokens verwendet: {total_tokens}")

    def switch_persona(self, persona_label):
        if persona_label in persona_map:
            self.persona_manager.load_persona(persona_map[persona_label])
            self.active_persona = persona_label

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Datei öffnen", ".", "Alle Dateien (*.*)")
        if file_path:
            self.current_file_path = file_path
            self.load_file_preview_from_path(file_path)

    def load_file_preview(self, item):
        file_path = os.path.join(".", item.text())
        if os.path.isfile(file_path):
            self.current_file_path = file_path
            self.load_file_preview_from_path(file_path)

    def load_file_preview_from_path(self, file_path):
        try:
            self.clear_preview()
            if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")):
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    self.preview_image.setPixmap(pixmap.scaledToWidth(200))
                    self.preview_image.show()
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    preview_text = content[:2000] + "\n..." if len(content) > 2000 else content
                    self.preview_text.setText(preview_text)
                    self.preview_text.show()

            self.close_preview_btn.show()
        except Exception as e:
            self.preview_text.setText(f"❌ Vorschau nicht möglich: {str(e)}")
            self.preview_text.show()
            self.close_preview_btn.show()

    def analyze_current_file(self):
        if self.current_file_path and os.path.isfile(self.current_file_path):
            try:
                with open(self.current_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                prompt = f"Bitte analysiere folgenden Code auf Fehler, Struktur, Qualität und Verbesserungsvorschläge:\n\n{content}"
                response = self.llm.ask_persona(self.active_persona, prompt)
                self.add_message(self.active_persona, f"📊 Analyse von {os.path.basename(self.current_file_path)}:\n\n{response}")
            except Exception as e:
                self.add_message("System", f"❌ Analysefehler: {str(e)}")

    def create_dalle_image(self):
        prompt = self.input_field.toPlainText().strip()
        if not prompt:
            return self.add_message("System", "Bitte eine Bildbeschreibung eingeben.")

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
        }
        json_data = {
            "prompt": prompt,
            "n": 1,
            "size": "512x512"
        }
        try:
            r = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=json_data)
            if r.status_code == 200:
                img_url = r.json()['data'][0]['url']
                self.add_message(self.active_persona, f"🖼️ DALL·E Bild erstellt: {img_url}")
            else:
                self.add_message("System", f"❌ Fehler bei DALL·E: {r.text}")
        except Exception as e:
            self.add_message("System", f"❌ DALL·E Anfragefehler: {str(e)}")

    def load_tree_file_preview(self, index):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            self.current_file_path = file_path
            self.load_file_preview_from_path(file_path)

    def clear_preview(self):
            self.preview_text.clear()
            self.preview_image.clear()
            self.preview_text.hide()
            self.preview_image.hide()
            self.close_preview_btn.hide()

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KimbaV3App()
    window.show()
    sys.exit(app.exec())
