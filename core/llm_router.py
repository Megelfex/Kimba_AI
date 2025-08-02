import os
from llama_cpp import Llama

class KimbaLLMRouter:
    def __init__(self, use_api=False, api_choice=None):
        """
        Router für verschiedene LLMs (lokal oder API).
        DE: Steuert, ob lokale Modelle oder APIs wie GPT/Claude genutzt werden.
        """
        # API Settings
        self.use_api = use_api
        self.api_choice = api_choice
        self.openai_client = None
        self.claude_client = None

        # Modellpfade definieren
        self.model_paths = {
            "core": "models/llm/general/tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf",
            "creative": "models/llm/general/tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf",
            "code": "models/llm/general/tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf",
            "empathy": "models/llm/general/tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf",
            "multimodal": "models/llm/general/tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf"
        }

        self.models = {}

        # Falls API aktiv ist, initialisieren
        if self.use_api:
            self._init_api_clients()

    def _init_api_clients(self):
        """Initialisiert API-Clients für GPT oder Claude."""
        if self.api_choice == "gpt":
            try:
                import openai
                self.openai_client = openai
                self.openai_client.api_key = os.getenv("OPENAI_API_KEY")
                print("[INFO] GPT API-Client initialisiert.")
            except ImportError:
                print("[ERROR] openai-Paket nicht installiert.")
        elif self.api_choice == "claude":
            try:
                import anthropic
                self.claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                print("[INFO] Claude API-Client initialisiert.")
            except ImportError:
                print("[ERROR] anthropic-Paket nicht installiert.")

    def load_model(self, purpose):
        """Lädt ein Modell für den angegebenen Zweck."""
        if purpose not in self.model_paths:
            raise ValueError(f"[ERROR] Kein Modellpfad für Zweck '{purpose}' definiert.")

        path = self.model_paths[purpose]

        if not os.path.exists(path):
            print(f"[ERROR] Modellpfad existiert nicht: {path}")
            return None

        try:
            print(f"[INFO] 🧠 Lade Modell: {path}")
            self.models[path] = Llama(model_path=path, n_ctx=4096, n_threads=8)
            return self.models[path]
        except Exception as e:
            print(f"[ERROR] ❌ Fehler beim Laden {path}: {e}")
            return None

    def ask(self, prompt, purpose="core", max_tokens=512):
        """Fragt ein Modell oder API an."""
        # API-Modus
        if self.use_api:
            return self.ask_api(prompt, purpose)

        # Lokaler Modus
        model = self.models.get(self.model_paths[purpose])
        if model is None:
            model = self.load_model(purpose)
            if model is None:
                return "[ERROR] Modell konnte nicht geladen werden."

        output = model(prompt, max_tokens=max_tokens)
        return output["choices"][0]["text"]

    def ask_api(self, prompt, purpose="core"):
        """Stellt eine Anfrage an GPT oder Claude API."""
        if self.api_choice == "gpt" and self.openai_client:
            resp = self.openai_client.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512
            )
            return resp.choices[0].message["content"]

        elif self.api_choice == "claude" and self.claude_client:
            resp = self.claude_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.content[0].text

        else:
            return "[ERROR] Keine API-Client-Initialisierung gefunden."

    def list_llm_models(self):
        """Listet alle verfügbaren LLM-Modelle im Ordner models/llm."""
        models_dir = "models/llm"
        all_models = []
        for root, dirs, files in os.walk(models_dir):
            for f in files:
                if f.endswith(".gguf"):
                    all_models.append(os.path.join(root, f))
        return all_models

    def list_image_models(self):
        """Listet alle verfügbaren Bildmodelle im Ordner models/image."""
        models_dir = "models/image"
        all_models = []
        for root, dirs, files in os.walk(models_dir):
            for f in files:
                if f.endswith(".safetensors"):
                    all_models.append(os.path.join(root, f))
        return all_models
