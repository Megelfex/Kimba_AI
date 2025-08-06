import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QScrollArea, QFrame, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont

# Dummy chat data
chat_data = [
    {"persona": "Iuno", "text": "Hey there, how are you today?"},
    {"persona": "Kimba", "text": "Meeeow! I’m feeling playful!"},
    {"persona": "Iuno", "text": "Glad to hear that!"},
    {"persona": "Kimba", "text": "Do you have some treats for me?"},
]

# Persona styles
persona_styles = {
    "Iuno": {"color": "#e0f0ff", "avatar": "visual/avatar_iuno.png"},
    "Kimba": {"color": "#fff4e0", "avatar": "visual/avatar_kimba.png"}
}

# Dummy moods
moods = {
    "Iuno": "😊 Happy",
    "Kimba": "😺 Playful"
}

# Dummy tasks
tasks = [
    {"text": "Refactor long-term memory system", "priority": "🔴"},
    {"text": "Prepare image assets for Kimba", "priority": "🟠"},
    {"text": "Test new mood engine", "priority": "🟢"}
]


class ChatBubble(QWidget):
    def __init__(self, persona, text):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        color = persona_styles[persona]["color"]
        avatar_path = persona_styles[persona]["avatar"]

        # Avatar
        avatar_label = QLabel()
        pixmap = QPixmap(avatar_path).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        avatar_label.setPixmap(pixmap)

        # Bubble
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setStyleSheet(f"background-color: {color}; padding: 8px; border-radius: 8px;")
        bubble.setFont(QFont("Arial", 10))

        if persona == "Iuno":
            layout.addWidget(avatar_label)
            layout.addWidget(bubble)
            layout.addStretch()
        else:
            layout.addStretch()
            layout.addWidget(bubble)
            layout.addWidget(avatar_label)

        self.setLayout(layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kimba AI Chat – Prototype")
        self.resize(900, 600)

        main_layout = QHBoxLayout(self)

        # Chat Area
        chat_area = QVBoxLayout()
        chat_area.setSpacing(5)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for msg in chat_data:
            scroll_layout.addWidget(ChatBubble(msg["persona"], msg["text"]))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_widget)

        chat_area.addWidget(scroll)

        # Input Area
        input_layout = QHBoxLayout()
        self.input_field = QTextEdit()
        self.input_field.setFixedHeight(50)
        send_btn = QPushButton("Send")
        voice_btn = QPushButton("🎤")
        attach_btn = QPushButton("📎")
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_btn)
        input_layout.addWidget(voice_btn)
        input_layout.addWidget(attach_btn)

        chat_area.addLayout(input_layout)

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)

        mood_label = QLabel("<b>Current Mood</b>")
        sidebar.addWidget(mood_label)

        for persona, mood in moods.items():
            lbl = QLabel(f"{persona}: {mood}")
            sidebar.addWidget(lbl)

        sidebar.addSpacing(20)
        task_label = QLabel("<b>Active Tasks</b>")
        sidebar.addWidget(task_label)

        task_list = QListWidget()
        for task in tasks:
            item = QListWidgetItem(f"{task['priority']} {task['text']}")
            task_list.addItem(item)
        sidebar.addWidget(task_list)

        # Combine layouts
        main_layout.addLayout(chat_area, 3)
        sidebar_frame = QFrame()
        sidebar_frame.setLayout(sidebar)
        sidebar_frame.setFixedWidth(250)
        main_layout.addWidget(sidebar_frame)

        # Apply basic styling
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 11pt;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 5px 10px;
                border-radius: 5px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
