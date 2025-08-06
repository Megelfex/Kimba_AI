from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static, Select, Button
from textual.containers import Horizontal
from archive.llm_router import KimbaLLMRouter

class KimbaTerminalUI(App):
    CSS_PATH = "kimba_ui.css"

    def __init__(self):
        super().__init__()
        self.llm = KimbaLLMRouter()
        self.chat_history = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Kimba Terminal v1 - Dein Ghibli CMD+ChatGPT Hybrid", classes="title")
        yield Horizontal(
            Select(
                options=[(name, name) for name in self.llm.local_models.keys()],
                prompt="Wähle ein Modell"
            ),
            Button("API Modus umschalten", id="toggle_api"),
            Button("Bild generieren", id="gen_image"),
            Button("Code analysieren", id="analyze_code"),
        )
        yield Static("", id="chatbox")
        yield Input(placeholder="Schreibe hier...", id="user_input")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "toggle_api":
            state = self.llm.toggle_api()
            self.query_one("#chatbox", Static).update(
                f"🔄 API Modus: {'AN' if state else 'AUS'}"
            )
        elif event.button.id == "gen_image":
            self.query_one("#chatbox", Static).update("🎨 [Bildgenerierung gestartet]")
        elif event.button.id == "analyze_code":
            self.query_one("#chatbox", Static).update("🛠 [Codeanalyse gestartet]")

    def on_select_changed(self, event: Select.Changed):
        self.llm.set_model(event.value)
        self.query_one("#chatbox", Static).update(f"✅ Modell gesetzt: {event.value}")

    def on_input_submitted(self, event: Input.Submitted):
        user_text = event.value
        self.chat_history += f"\n🧑 Du: {user_text}"
        reply = self.llm.ask(user_text)
        self.chat_history += f"\n🐱 Kimba: {reply}"
        self.query_one("#chatbox", Static).update(self.chat_history)
        event.input.value = ""

if __name__ == "__main__":
    KimbaTerminalUI().run()
