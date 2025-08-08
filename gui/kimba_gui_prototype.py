import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QScrollArea, QComboBox, QCheckBox,
    QTreeView, QSplitter, QSizePolicy
)
from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QPixmap, QFileSystemModel

# Core
from core.persona_manager import PersonaManager
from core.llm_router import KimbaLLMRouter

# Memory system
from memory.memory_manager import MemoryManager


# Persona map (UI label -> module name)
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
    "Shorekeeper": "persona_shorekeeper",
}


# === Simple chat bubble ===
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


class KimbaV3App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kimba Augusta – Dev Companion")
        self.resize(1200, 750)

        # Core systems
        self.persona_manager = PersonaManager()
        self.memory_manager = MemoryManager()
        self.llm = KimbaLLMRouter(persona_manager=self.persona_manager, memory_manager=self.memory_manager)

        # Default persona
        self.active_persona = "Augusta"
        self.persona_manager.load_persona(persona_map[self.active_persona])

        # ---------- LEFT: file explorer (tree) + preview in a vertical splitter ----------
        self.fs_model = QFileSystemModel()
        self.fs_model.setRootPath(QDir.currentPath())
        self.fs_model.setFilter(
            QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot
        )

        self.file_tree = QTreeView()
        self.file_tree.setModel(self.fs_model)
        self.file_tree.setRootIndex(self.fs_model.index(QDir.currentPath()))
        self.file_tree.setColumnWidth(0, 280)
        self.file_tree.doubleClicked.connect(self.on_tree_double_clicked)
        self.file_tree.setHeaderHidden(False)

        self.preview = QLabel("📝 Vorschau …")
        self.preview.setStyleSheet("color: #90ee90;")
        self.preview.setMinimumHeight(160)
        self.preview.setWordWrap(True)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # A vertical splitter for tree (top) + preview (bottom)
        self.left_splitter = QSplitter(Qt.Orientation.Vertical)
        self.left_splitter.setHandleWidth(6)
        self.left_splitter.addWidget(self.file_tree)
        self.left_splitter.addWidget(self.preview)
        self.left_splitter.setChildrenCollapsible(False)
        self.left_splitter.setSizes([520, 220])  # tree taller than preview by default
        self.left_splitter.setMinimumWidth(260)

        # ---------- CENTER: Chat ----------
        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.chat_area)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_widget)

        self.input_field = QTextEdit()
        self.input_field.setFixedHeight(64)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.handle_send)

        analyze_btn = QPushButton("🔍 Analyse aktuelle Datei")
        analyze_btn.clicked.connect(self.analyze_current_file)

        center_panel = QVBoxLayout()
        self.chat_title = QLabel(f"💬 Chat mit {self.active_persona}")
        center_panel.addWidget(self.chat_title)
        center_panel.addWidget(scroll)

        input_row = QHBoxLayout()
        input_row.addWidget(self.input_field)
        center_panel.addLayout(input_row)

        action_row = QHBoxLayout()
        action_row.addWidget(send_btn)
        action_row.addWidget(analyze_btn)
        center_panel.addLayout(action_row)

        center_container = QWidget()
        center_container.setLayout(center_panel)
        center_container.setMinimumWidth(500)
        center_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # ---------- RIGHT: Persona & modes ----------
        self.persona_dropdown = QComboBox()
        self.persona_dropdown.addItems(persona_map.keys())
        self.persona_dropdown.setCurrentText(self.active_persona)
        self.persona_dropdown.currentTextChanged.connect(self.switch_persona)

        self.chk_autosave = QCheckBox("AutoSave memory")
        self.chk_autosave.setChecked(True)
        self.chk_debug = QCheckBox("Debug Mode")
        self.chk_codeassist = QCheckBox("CodeAssist")
        self.chk_explain = QCheckBox("Explain Mode")
        self.token_label = QLabel("Tokens verwendet: 0")

        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("👤 Persona"))
        right_panel.addWidget(self.persona_dropdown)
        right_panel.addWidget(QLabel("⚙️ Modi"))
        right_panel.addWidget(self.chk_autosave)
        right_panel.addWidget(self.chk_debug)
        right_panel.addWidget(self.chk_codeassist)
        right_panel.addWidget(self.chk_explain)
        right_panel.addStretch()
        right_panel.addWidget(self.token_label)

        right_container = QWidget()
        right_container.setLayout(right_panel)
        right_container.setMinimumWidth(240)
        right_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        # ---------- OUTER splitter: left (vertical splitter) | center | right ----------
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(6)
        splitter.addWidget(self.left_splitter)    # left: tree + preview
        splitter.addWidget(center_container)      # center: chat
        splitter.addWidget(right_container)       # right: controls

        # don’t allow panes to collapse to 0
        for i in range(3):
            splitter.setCollapsible(i, False)

        # stretch factors: center gets most space
        splitter.setStretchFactor(0, 3)  # left
        splitter.setStretchFactor(1, 8)  # center (big)
        splitter.setStretchFactor(2, 3)  # right
        splitter.setSizes([320, 820, 280])  # starting widths

        outer = QHBoxLayout()
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(splitter)
        self.setLayout(outer)
        self.setStyleSheet("background-color: #121212; color: #90ee90;")

        self.current_file_path = None

        # Greeting
        self.add_message("System", "Memory is active. Everything you and Augusta say is saved & searchable.")

    # ----- helpers -----
    def add_message(self, sender, text):
        bubble = ChatBubble(sender, text)
        self.chat_area.addWidget(bubble)

    def on_tree_double_clicked(self, index):
        path = self.fs_model.filePath(index)
        if os.path.isdir(path):
            return
        self.current_file_path = path
        self.load_file_preview_from_path(path)

    def load_file_preview_from_path(self, file_path):
        try:
            # Images
            if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")):
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    self.preview.setPixmap(
                        pixmap.scaledToWidth(360, Qt.TransformationMode.SmoothTransformation)
                    )
                    return
            # Text
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.preview.setPixmap(QPixmap())  # reset if last was image
                self.preview.setText(content[:2500] + ("..." if len(content) > 2500 else ""))
        except Exception as e:
            self.preview.setPixmap(QPixmap())
            self.preview.setText(f"❌ Vorschau nicht möglich: {str(e)}")

    # ----- core actions -----
    def switch_persona(self, persona_label):
        if persona_label in persona_map:
            module_name = persona_map[persona_label]
            self.persona_manager.load_persona(module_name)
            self.active_persona = persona_label
            self.chat_title.setText(f"💬 Chat mit {self.active_persona}")

    def handle_send(self):
        user_text = self.input_field.toPlainText().strip()
        if not user_text:
            return
        self.input_field.clear()
        self.add_message("You", user_text)

        # 1) Save user message (session + optional LT)
        self.memory_manager.remember(
            speaker="user",
            text=user_text,
            category="user_input",
            tags=[self.active_persona],
            importance=0
        )

        # 2) Recall relevant memories
        memory_hits = []
        try:
            hits = self.memory_manager.recall(user_text, limit=3)
            for sim, mem in hits:
                txt = mem.get("text", "")
                cat = mem.get("category", "general")
                prj = mem.get("project") or ""
                memory_hits.append(f"- {txt} ({cat}{', ' + prj if prj else ''}; rel: {sim:.2f})")
        except Exception as e:
            memory_hits.append(f"[Memory recall error: {e}]")

        # 3) Build augmented prompt
        augmented = user_text
        if memory_hits:
            augmented = "[Memories]\n" + "\n".join(memory_hits) + f"\n\n[User]\n{user_text}"

        # 4) Ask the active persona
        response = self.llm.ask_persona(self.active_persona, augmented)
        self.add_message(self.active_persona, response)

        # 5) Save persona reply
        self.memory_manager.remember(
            speaker="persona",
            text=response,
            category="persona_response",
            tags=[self.active_persona],
            importance=0
        )

    def analyze_current_file(self):
        if self.current_file_path and os.path.isfile(self.current_file_path):
            try:
                with open(self.current_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                prompt = (
                    "Bitte analysiere den folgenden Code/Texte auf Fehler, "
                    "Verbesserungen und Clean-Code-Punkte:\n\n" + content
                )

                # Recall for analysis request too
                memory_hits = []
                try:
                    hits = self.memory_manager.recall(prompt, limit=3)
                    for sim, mem in hits:
                        memory_hits.append(f"- {mem.get('text','')} (rel: {sim:.2f})")
                except Exception:
                    pass

                augmented = prompt if not memory_hits else "[Memories]\n" + "\n".join(memory_hits) + "\n\n" + prompt
                response = self.llm.ask_persona(self.active_persona, augmented)
                self.add_message(self.active_persona, f"📊 Analyse von {os.path.basename(self.current_file_path)}:\n\n{response}")

                # Save analysis request + result (mark a bit more important)
                self.memory_manager.remember("user", f"[analyse:{os.path.basename(self.current_file_path)}]",
                                             category="analysis", tags=[self.active_persona], importance=1)
                self.memory_manager.remember("persona", response,
                                             category="analysis_result", tags=[self.active_persona], importance=1)

            except Exception as e:
                self.add_message("System", f"❌ Fehler bei Analyse: {str(e)}")
        else:
            self.add_message("System", "⚠️ Keine Datei zum Analysieren geöffnet.")

    def closeEvent(self, event):
        try:
            self.memory_manager.session_memory.save_to_json()
        finally:
            super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KimbaV3App()
    window.show()
    sys.exit(app.exec())
