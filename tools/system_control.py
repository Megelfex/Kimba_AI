
import os
import subprocess
import pyautogui
import time

class KimbaSystem:
    def open_file(self, path):
        try:
            os.startfile(path)
            return f"📂 Datei geöffnet: {path}"
        except Exception as e:
            return f"❌ Fehler beim Öffnen der Datei: {e}"

    def launch_app(self, app_name):
        try:
            subprocess.Popen(app_name)
            return f"🚀 Anwendung gestartet: {app_name}"
        except Exception as e:
            return f"❌ Fehler beim Starten der Anwendung: {e}"

    def move_mouse(self, x, y):
        pyautogui.moveTo(x, y, duration=1)
        return f"🖱 Maus bewegt zu: ({x}, {y})"

    def click_mouse(self):
        pyautogui.click()
        return "✅ Klick ausgeführt"

    def take_screenshot(self, filename="screenshot.png"):
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return f"📸 Screenshot gespeichert als: {filename}"

    def read_directory(self, path):
        try:
            return os.listdir(path)
        except Exception as e:
            return f"❌ Fehler beim Lesen des Verzeichnisses: {e}"
