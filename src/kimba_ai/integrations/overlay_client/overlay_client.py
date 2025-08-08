import sys
import os
import socket
import threading
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap

class CharacterOverlay(QMainWindow):
    def __init__(self, visuals_path, character="iuno", start_animation="idle", frame_delay=150, port=5001):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.visuals_path = visuals_path
        self.character = character
        self.current_animation = start_animation
        self.frame_delay = frame_delay

        self.animations = self._load_all_animations()
        if self.current_animation not in self.animations:
            raise ValueError(f"Animation '{self.current_animation}' nicht gefunden für {self.character}")

        self.frames = self.animations[self.current_animation]
        self.current_frame = 0
        self.label.setPixmap(self.frames[self.current_frame])
        self.resize(self.frames[0].size())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(self.frame_delay)

        self.old_pos = None

        # 🎯 Live-Kommunikation starten
        threading.Thread(target=self.listen_for_commands, args=(port,), daemon=True).start()

    def _load_all_animations(self):
        animations = {}
        for folder in os.listdir(self.visuals_path):
            if folder.startswith(self.character):
                anim_path = os.path.join(self.visuals_path, folder)
                if os.path.isdir(anim_path):
                    frames = []
                    for f in sorted(os.listdir(anim_path)):
                        if f.lower().endswith(".png"):
                            frames.append(QPixmap(os.path.join(anim_path, f)))
                    if frames:
                        anim_name = folder.split("_", 1)[-1]
                        animations[anim_name] = frames
        return animations

    def set_animation(self, animation_name):
        if animation_name in self.animations:
            self.current_animation = animation_name
            self.frames = self.animations[animation_name]
            self.current_frame = 0
            print(f"[{self.character}] Animation gewechselt zu: {animation_name}")
        else:
            print(f"[WARN] Animation '{animation_name}' nicht gefunden für {self.character}")

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.label.setPixmap(self.frames[self.current_frame])

    # Fenster verschiebbar machen
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = event.globalPosition() - self.old_pos
            self.move(self.x() + int(delta.x()), self.y() + int(delta.y()))
            self.old_pos = event.globalPosition()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = None

    def listen_for_commands(self, port):
        """Lauscht auf Animation-Befehle."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", port))
        server.listen(1)
        print(f"[{self.character}] Lausche auf Port {port} für Befehle...")

        while True:
            conn, _ = server.accept()
            data = conn.recv(1024).decode().strip()
            if data:
                self.set_animation(data)
            conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Bitte Charakter-Name angeben (iuno oder kimba)")
        sys.exit(1)

    character = sys.argv[1]
    port = 5001 if character == "iuno" else 5002

    app = QApplication(sys.argv)
    visuals_path = os.path.join(os.path.dirname(__file__), "visuals")
    overlay = CharacterOverlay(visuals_path, character=character, start_animation="idle", frame_delay=150, port=port)
    overlay.move(200 if character == "iuno" else 600, 500)
    overlay.show()
    sys.exit(app.exec())
