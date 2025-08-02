"""
Kimba Terminal UI - Hauptkommunikationszentrum
==============================================
DE: Dies ist die zentrale Benutzeroberfläche für Kimba, in der alle Interaktionen
    stattfinden – Chat, Befehle, Datei- und Bildoperationen.
    Sie unterstützt Modellwahl über Dropdown und erkennt spezielle Befehle automatisch.

EN: This is the main communication hub for Kimba, where all interactions happen –
    chat, commands, file and image operations.
    It supports model selection via dropdown and automatically detects special commands.
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static, Select, Button
from textual.containers import Horizontal
import logging
import os

# Import Kimba Core Modules
from core.llm_router import KimbaLLMRouter
from core.kimba_core import run_file_organizer, kimba_say

# Logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


class KimbaTerminalUI(App):
    """
    DE: Hauptklasse der Textual-UI für Kimba.
    EN: Main class of Kimba's Textual UI.
    """

    CSS_PATH = "kimba_ui.css"
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.router = KimbaLLMRouter()  # Standard: lokaler Modus
        self.messages = []  # Chatverlauf
        self.current_purpose = "core"

    def compose(self) -> ComposeResult:
        """DE: Definiert das Layout. EN: Defines the layout."""
        yield Header()

        # Dropdowns und Buttons
        with Horizontal():
            yield Select(
                options=[
                    ("Core Chat", "core"),
                    ("Creative Writing", "creative"),
                    ("Code Assistant", "code"),
                    ("Empathy Mode", "empathy"),
                    ("Multimodal", "multimodal"),
                    ("GPT-4 API", "gpt"),
                    ("Claude API", "claude")
                ],
                prompt="Select Model",
                id="model_select"
            )
            yield Button("API Mode: OFF", id="api_toggle", variant="error")

        # Chatbereich
        yield Static("", id="chat_history", classes="chat-box")

        # Eingabezeile
        yield Input(placeholder="Schreibe hier an Kimba / Type here to Kimba", id="chat_input")

        yield Footer()

    def on_select_changed(self, event: Select.Changed) -> None:
        """DE: Modellwechsel. EN: Model change."""
        self.current_purpose = event.value
        if event.value in ["gpt", "claude"]:
            self.router.use_api = True
            self.router.api_choice = event.value
            self.router._init_api_clients()
        else:
            self.router.use_api = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """DE: API-Toggle. EN: API toggle."""
        if event.button.id == "api_toggle":
            self.router.use_api = not self.router.use_api
            event.button.label = f"API Mode: {'ON' if self.router.use_api else 'OFF'}"
            event.button.variant = "success" if self.router.use_api else "error"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """DE: Eingabe verarbeiten. EN: Process input."""
        user_msg = event.value.strip()
        if not user_msg:
            return

        # Usernachricht speichern
        self.messages.append({"user": user_msg})
        self.update_chat()

        # Spezielle Befehle erkennen
        if "prüfe plugins" in user_msg.lower() or "check plugins" in user_msg.lower():
            result = self.check_plugins_folder()
            self.add_kimba_response(result)
        else:
            # Normale KI-Antwort holen
            kimba_response = self.router.ask(user_msg, purpose=self.current_purpose)
            self.add_kimba_response(kimba_response)

        # Eingabe zurücksetzen
        event.input.value = ""

    def check_plugins_folder(self) -> str:
        """
        DE: Prüft den plugins-Ordner und gibt Status zurück.
        EN: Checks the plugins folder and returns the status.
        """
        folder_path = os.path.join(os.getcwd(), "plugins")
        if not os.path.exists(folder_path):
            return "Der Plugins-Ordner existiert nicht."
        contents = os.listdir(folder_path)
        if not contents:
            return "Der Plugins-Ordner ist leer. Soll ich dir ein Plugin vorschlagen?"
        return f"Ich habe {len(contents)} Plugin(s) gefunden: {', '.join(contents)}"

    def add_kimba_response(self, text: str):
        """DE: Fügt Kimbas Antwort zum Chat hinzu. EN: Adds Kimba's response to the chat."""
        self.messages[-1]["kimba"] = text
        self.update_chat()

    def update_chat(self):
        """DE: Aktualisiert den Chatverlauf. EN: Updates the chat history."""
        chat_text = "\n".join(
            [f"You: {m['user']}\nKimba: {m.get('kimba','')}" for m in self.messages]
        )
        self.query_one("#chat_history", Static).update(chat_text)


if __name__ == "__main__":
    KimbaTerminalUI().run()
