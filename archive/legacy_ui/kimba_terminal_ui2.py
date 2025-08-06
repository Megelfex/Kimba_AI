from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Button, Static, Select
from archive.llm_router import KimbaLLMRouter
from visual.themes import ThemeManager

class KimbaUI(App):
    CSS_PATH = "themes.css"
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.router = KimbaLLMRouter()
        self.messages = []
        self.current_purpose = "core"
        self.theme = ThemeManager("ghibli")

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Horizontal():
                yield Select(
                    options=[
                        ("Core Chat", "core"),
                        ("Creative Writing", "creative"),
                        ("Code Assistant", "code"),
                        ("Empathy Mode", "empathy"),
                        ("Multimodal / Bild", "multimodal"),
                        ("GPT-4 API", "gpt"),
                        ("Claude API", "claude")
                    ],
                    prompt="Select Model",
                    id="model_select"
                )
                yield Button("API Mode: OFF", id="api_toggle", variant="error")
                yield Button("Bildmodus", id="image_mode", variant="primary")
            yield Static("", id="chat_history", classes="chat-box")
            yield Input(placeholder="Schreib etwas für Kimba...", id="chat_input")
        yield Footer()

    def on_select_changed(self, event: Select.Changed) -> None:
        self.current_purpose = event.value
        if event.value in ["gpt", "claude"]:
            self.router.use_api = True
            self.router.api_choice = event.value
        else:
            self.router.use_api = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "api_toggle":
            self.router.use_api = not self.router.use_api
            event.button.label = f"API Mode: {'ON' if self.router.use_api else 'OFF'}"
            event.button.variant = "success" if self.router.use_api else "error"

        elif event.button.id == "image_mode":
            last_msg = self.messages[-1]["user"] if self.messages else "Bitte Prompt eingeben"
            result = self.router.generate_image(last_msg)
            self.query_one("#chat_history", Static).update(f"[Bild erstellt] {result}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_msg = event.value
        self.messages.append({"user": user_msg})
        self.query_one("#chat_history", Static).update(
            "\n".join([f"Du: {m['user']}\nKimba: {m.get('kimba','')}" for m in self.messages])
        )
        kimba_response = self.router.ask(user_msg, purpose=self.current_purpose)
        self.messages[-1]["kimba"] = kimba_response
        self.query_one("#chat_history", Static).update(
            "\n".join([f"Du: {m['user']}\nKimba: {m.get('kimba','')}" for m in self.messages])
        )
        event.input.value = ""

    class KimbaTerminalUI(App):
    CSS_PATH = "kimba_ui.css"

    def __init__(self):
        super().__init__()
        self.llm = KimbaLLMRouter()

        # Listen der Modelle
        self.local_llm_models = self.llm.list_llm_models()
        self.local_image_models = self.llm.list_image_models()

        self.selected_llm_model = None
        self.selected_image_model = None

    def compose(self) -> ComposeResult:
        yield Header()

        # LLM-Modell Auswahl
        yield Select(
            options=[(m, m) for m in self.local_llm_models],
            prompt="LLM Modell wählen",
            id="llm_model_select"
        )

        # Bildmodell Auswahl
        yield Select(
            options=[(m, m) for m in self.local_image_models],
            prompt="Bildmodell wählen",
            id="image_model_select"
        )

        yield Button("Bild generieren", id="gen_image")
        yield Static("", id="chatbox")
        yield Input(placeholder="Schreibe hier...", id="user_input")
        yield Footer()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "llm_model_select":
            self.selected_llm_model = event.value
            self.query_one("#chatbox", Static).update(f"LLM Modell gesetzt: {event.value}")
        elif event.select.id == "image_model_select":
            self.selected_image_model = event.value
            self.query_one("#chatbox", Static).update(f"Bildmodell gesetzt: {event.value}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "gen_image":
            if not self.selected_image_model:
                self.query_one("#chatbox", Static).update("⚠ Bitte ein Bildmodell auswählen!")
                return

            user_prompt = self.query_one("#user_input", Input).value
            if not user_prompt:
                self.query_one("#chatbox", Static).update("⚠ Bitte einen Prompt eingeben!")
                return

            result = self.llm.generate_image_comfyui(user_prompt, self.selected_image_model)
            self.query_one("#chatbox", Static).update(result)

        from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static, Select, Button
from archive.llm_router import KimbaLLMRouter

class KimbaTerminalUI(App):
    CSS_PATH = "kimba_ui.css"

    def __init__(self):
        super().__init__()
        self.llm = KimbaLLMRouter()
        self.local_llm_models = self.llm.list_llm_models()
        self.local_image_models = self.llm.list_image_models()
        self.selected_image_model = None

    def compose(self) -> ComposeResult:
        yield Header()

        yield Select(
            options=[(m, m) for m in self.local_llm_models],
            prompt="LLM Modell wählen",
            id="llm_model_select"
        )

        yield Select(
            options=[(m, m) for m in self.local_image_models],
            prompt="Bildmodell wählen",
            id="image_model_select"
        )

        yield Button("Bild generieren", id="gen_image")
        yield Static("", id="chatbox")
        yield Input(placeholder="Schreibe hier...", id="user_input")
        yield Footer()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "llm_model_select":
            result = self.llm.set_llm_model(event.value)
            self.query_one("#chatbox", Static).update(result)

        elif event.select.id == "image_model_select":
            self.selected_image_model = event.value
            self.query_one("#chatbox", Static).update(f"Bildmodell gesetzt: {event.value}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "gen_image":
            user_prompt = self.query_one("#user_input", Input).value
            if not user_prompt:
                self.query_one("#chatbox", Static).update("⚠ Bitte einen Prompt eingeben!")
                return
            result = self.llm.generate_image_comfyui(user_prompt, self.selected_image_model)
            self.query_one("#chatbox", Static).update(result)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        prompt = event.value
        reply = self.llm.ask_local(prompt)
        self.query_one("#chatbox", Static).update(f"Kimba: {reply}")
    
    

if __name__ == "__main__":
    KimbaUI().run()
