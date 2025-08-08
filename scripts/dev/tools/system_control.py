import os
import subprocess
import pyautogui
import time

class KimbaSystem:
    """
    EN: Provides system-level functions for Kimba, such as launching apps,
    opening files, controlling the mouse, taking screenshots, and reading directories.

    DE: Stellt Systemfunktionen für Kimba bereit – z. B. App-Start, Dateizugriff,
    Maussteuerung, Screenshots und Verzeichnisanalyse.
    """

    def open_file(self, path):
        """
        EN: Opens a file with the default associated application.
        DE: Öffnet eine Datei mit der Standardanwendung des Systems.

        Args:
            path (str): Full path to the file.

        Returns:
            str: Success or error message.
        """
        try:
            os.startfile(path)
            return f"📂 Datei geöffnet: {path}"
        except Exception as e:
            return f"❌ Fehler beim Öffnen der Datei: {e}"

    def launch_app(self, app_name):
        """
        EN: Launches an application by name or path.
        DE: Startet eine Anwendung über ihren Namen oder Pfad.

        Args:
            app_name (str): Executable or path to the application.

        Returns:
            str: Success or error message.
        """
        try:
            subprocess.Popen(app_name)
            return f"🚀 Anwendung gestartet: {app_name}"
        except Exception as e:
            return f"❌ Fehler beim Starten der Anwendung: {e}"

    def move_mouse(self, x, y):
        """
        EN: Moves the mouse cursor smoothly to a given screen coordinate.
        DE: Bewegt den Mauszeiger sanft zu einer bestimmten Bildschirmposition.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            str: Confirmation message.
        """
        pyautogui.moveTo(x, y, duration=1)
        return f"🖱 Maus bewegt zu: ({x}, {y})"

    def click_mouse(self):
        """
        EN: Performs a left mouse click at the current position.
        DE: Führt einen Mausklick an der aktuellen Position aus.

        Returns:
            str: Confirmation message.
        """
        pyautogui.click()
        return "✅ Klick ausgeführt"

    def take_screenshot(self, filename="screenshot.png"):
        """
        EN: Captures a screenshot and saves it to a file.
        DE: Erstellt einen Screenshot und speichert ihn als Datei.

        Args:
            filename (str): File name for the screenshot.

        Returns:
            str: Confirmation message.
        """
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return f"📸 Screenshot gespeichert als: {filename}"

    def read_directory(self, path):
        """
        EN: Returns the list of files/folders in the given directory.
        DE: Gibt die Inhalte eines Verzeichnisses zurück.

        Args:
            path (str): Path to the directory.

        Returns:
            list[str] or str: List of items or error message.
        """
        try:
            return os.listdir(path)
        except Exception as e:
            return f"❌ Fehler beim Lesen des Verzeichnisses: {e}"
