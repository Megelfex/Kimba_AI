import os
from llama_cpp import Llama

class KimbaLLMRouter:
    def __init__(self, use_api=False, api_choice="gpt"):
        """
        Kimba LLM Router
        - Lädt MythoMax Q4_K_M lokal mit stabilen Parametern
        - Optional GPT/Claude-Fallback
        """

        # API-Einstellungen
        self.use_api = use_api
        self.api_choice = api_choice
        self.openai_client = None
        self.claude_client = None

        # Hauptmodellpfad
        self.model_paths = {
            "core": "models/mythomax-l2-13b.Q4_K_M.gguf"
        }

        self.models = {}

        # API-Clients initialisieren (nur wenn aktiviert)
        if self.use_api:
            self._init_api_clients()

    def _init_api_clients(self):
        """Initialisiert API-Clients für GPT oder Claude."""
        if self.api_choice == "gpt":
            try:
                import openai
                self.openai_client = openai
                self.openai_client.api_key = os.getenv("OPENAI_API_KEY")
                print("[INFO] 🌐 GPT API-Client initialisiert.")
            except ImportError:
                print("[ERROR] OpenAI-Paket nicht installiert.")
        elif self.api_choice == "claude":
            try:
                import anthropic
                self.claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                print("[INFO] 🌐 Claude API-Client initialisiert.")
            except ImportError:
                print("[ERROR] Anthropic-Paket nicht installiert.")

    def load_model(self, purpose="core"):
        """Lädt das Hauptmodell mit stabilen Ladeparametern."""
        path = self.model_paths.get(purpose)
        if not path or not os.path.exists(path):
            print(f"[ERROR] ❌ Modellpfad existiert nicht: {path}")
            return None

        try:
            print(f"[INFO] 🧠 Lade Modell: {path}")
            self.models[path] = Llama(
                model_path=path,
                n_ctx=768,       # Kleiner Kontext → weniger RAM
                n_threads=4,     # Weniger Threads → stabiler
                n_gpu_layers=0   # Kein GPU-Offload → VRAM frei für ComfyUI
            )
            print("[INFO] ✅ Modell erfolgreich geladen (GPU-Offload: 20 Layers).")
            return self.models[path]
        except Exception as e:
            print(f"[ERROR] ❌ Fehler beim Laden des Modells: {e}")
            return None

    def ask(self, prompt, purpose="core", max_tokens=512):
        """Fragt das Modell oder API an."""
        if self.use_api:
            return self.ask_api(prompt, purpose)

        model = self.models.get(self.model_paths[purpose])
        if model is None:
            model = self.load_model(purpose)
            if model is None:
                # Fallback auf API, wenn verfügbar
                if self.openai_client or self.claude_client:
                    print("[WARN] ⚠ Lokales Modell konnte nicht geladen werden – API wird verwendet.")
                    return self.ask_api(prompt, purpose)
                return "[ERROR] Modell konnte nicht geladen werden."

        output = model(prompt, max_tokens=max_tokens)
        return output["choices"][0]["text"]

    def ask_api(self, prompt, purpose="core"):
        """Anfrage an GPT oder Claude API."""
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
            return "[ERROR] Kein API-Client aktiv."

    def list_llm_models(self):
        """Listet alle verfügbaren GGUF-Modelle."""
        models_dir = "models"
        all_models = []
        for root, dirs, files in os.walk(models_dir):
            for f in files:
                if f.endswith(".gguf"):
                    all_models.append(os.path.join(root, f))
        return all_models
