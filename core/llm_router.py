"""
Kimba LLM Router - Clean Fixed Version
======================================
DE: Verwaltet den Zugriff auf lokale und API-basierte Sprachmodelle.
    Standardmäßig werden lokale Modelle genutzt, API-Modelle nur bei Bedarf.

EN: Manages access to local and API-based language models.
    Local models are used by default, API models only when explicitly requested.
"""

import os
import logging
from pathlib import Path
from llama_cpp import Llama

# API-Clients nur importieren, wenn gebraucht / Only import API clients if needed
try:
    from openai import OpenAI
    import anthropic
except ImportError:
    OpenAI = None
    anthropic = None

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


class KimbaLLMRouter:
    """
    DE: Router für verschiedene LLM-Modelle (lokal oder API).
    EN: Router for various LLM models (local or API).
    """

    def __init__(self, use_api=False, api_choice="gpt"):
        # Modellpfade
        self.model_paths = {
            "core": "models/llm/general/openhermes-2.5-mistral-7b.Q5_K_M.gguf",
            "creative": "models/llm/creative/mythomax-l2-13b.Q5_K_M.gguf",
            "code": "models/llm/code/deepseek-coder-6.7b-base.Q5_K_M.gguf",
            "empathy": "models/llm/empathy/dolphin-2.7-mixtral-8x7b.Q5_K_M.gguf",
            "multimodal": "models/llm/multimodal/Q5_K_M-00001-of-00003.gguf"
        }

        self.models = {}
        self.use_api = use_api
        self.api_choice = api_choice

        # API-Clients nur erstellen, wenn nötig
        self.gpt_client = None
        self.claude_client = None

        if self.use_api:
            self._init_api_clients()

    def _init_api_clients(self):
        """
        DE: Initialisiert API-Clients nur, wenn API-Modus aktiv ist.
        EN: Initializes API clients only if API mode is active.
        """
        if self.api_choice == "gpt":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logging.warning("⚠ Kein OPENAI_API_KEY gefunden, wechsle zu lokalem Modus.")
                self.use_api = False
                return
            self.gpt_client = OpenAI(api_key=api_key)
            logging.info("✅ GPT API-Client initialisiert.")

        elif self.api_choice == "claude":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                logging.warning("⚠ Kein ANTHROPIC_API_KEY gefunden, wechsle zu lokalem Modus.")
                self.use_api = False
                return
            self.claude_client = anthropic.Anthropic(api_key=api_key)
            logging.info("✅ Claude API-Client initialisiert.")

    def load_model(self, purpose: str):
        path = self.model_paths.get(purpose, self.model_paths["core"])

    # Prüfen, ob Pfad existiert
        if not os.path.exists(path):
            logging.warning(f"⚠ Modell-Datei fehlt: {path}")
            return None

        try:
            if path not in self.models:
                logging.info(f"🧠 Lade Modell: {path}")
                self.models[path] = Llama(
                    model_path=path,
                    n_ctx=2048,
                    n_threads=6,
                    n_gpu_layers=0,  # GPU deaktiviert für Stabilität
                    verbose=False
            )
            return self.models[path]
        except Exception as e:
            logging.error(f"❌ Fehler beim Laden {path}: {e}")
            return None


    def ask(self, prompt: str, purpose: str = "core") -> str:
        """Stellt dem passenden Modell eine Frage / Sends a prompt to the appropriate model."""
        if self.use_api:
            return self.ask_api(prompt)

        model = self.load_model(purpose)
        if model is None:
            # Versuch API-Fallback
            if self.openai_client or self.claude_client:
                logging.warning("⚠ Lokales Modell fehlgeschlagen → API-Fallback aktiviert.")
                self.use_api = True
                return self.ask_api(prompt)
            else:
                return "❌ Konnte lokales Modell nicht laden und kein API-Key vorhanden."

        try:
            output = model(prompt, max_tokens=512)
            return output.get("choices", [{}])[0].get("text", "").strip()
        except Exception as e:
        logging.error(f"❌ Fehler bei der Textgenerierung: {e}")
        return "❌ Fehler bei der Textgenerierung."

    def ask_api(self, prompt: str) -> str:
        """
        DE: Nutzt API-Modelle (GPT oder Claude).
        EN: Uses API models (GPT or Claude).
        """
        if self.api_choice == "gpt" and self.gpt_client:
            response = self.gpt_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()

        elif self.api_choice == "claude" and self.claude_client:
            response = self.claude_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()

        else:
            logging.warning("⚠ API-Client nicht initialisiert, wechsle zu lokalem Modus.")
            self.use_api = False
            return self.ask(prompt)

    def list_llm_models(self):
        """
        DE: Gibt eine Liste der verfügbaren LLM-Modelle zurück.
        EN: Returns a list of available LLM models.
        """
        return list(self.model_paths.keys())

    def list_image_models(self):
        """
        DE: Gibt eine Liste der verfügbaren Bildmodelle zurück.
        EN: Returns a list of available image models.
        """
        return ["sd_xl_base_1.0", "sd_xl_refiner_1.0"]
