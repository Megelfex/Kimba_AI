"""
Kimba LLM Router (Optimiert)
============================
DE: Verwaltet die Verbindung zu lokalen LLMs und optional GPT/Claude API.
    Optimiert für nur ein Hauptmodell im RAM + automatischer API-Fallback.
EN: Manages connection to local LLMs and optional GPT/Claude API.
    Optimized for single main model in RAM + automatic API fallback.
"""

import os
import logging
from llama_cpp import Llama
import openai
import anthropic


class KimbaLLMRouter:
    def __init__(self):
        # Pfad zu deinem Hauptmodell
        MAIN_MODEL_PATH = "models/llm/general/openhermes-2.5-mistral-7b.Q4_K_M.gguf"

        # Alle Rollen mappen auf das gleiche Modell
        self.model_paths = {
            "core": MAIN_MODEL_PATH,
            "creative": MAIN_MODEL_PATH,
            "code": MAIN_MODEL_PATH,
            "empathy": MAIN_MODEL_PATH,
            "multimodal": MAIN_MODEL_PATH,
            "gpt": None,      # API only
            "claude": None    # API only
        }

        self.models = {}
        self.use_api = False
        self.api_choice = "gpt"

        # API-Keys laden
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        self.openai_client = None
        self.claude_client = None

        self._init_api_clients()

    def _init_api_clients(self):
        """Initialisiert API-Clients, falls Keys vorhanden sind."""
        if self.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
            logging.info("✅ OpenAI API-Client initialisiert.")
        else:
            logging.warning("⚠ Kein OPENAI_API_KEY gefunden, GPT API deaktiviert.")

        if self.anthropic_api_key:
            self.claude_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            logging.info("✅ Anthropic API-Client initialisiert.")
        else:
            logging.warning("⚠ Kein ANTHROPIC_API_KEY gefunden, Claude API deaktiviert.")

    def load_model(self, purpose: str):
        """Lädt das Hauptmodell, falls noch nicht im Speicher."""
        path = self.model_paths.get(purpose, self.model_paths["core"])

        if not os.path.exists(path):
            logging.error(f"❌ Modell-Datei nicht gefunden: {path}")
            return None

        if "main" in self.models:
            return self.models["main"]

        try:
            logging.info(f"🧠 Lade Hauptmodell: {path}")
            self.models["main"] = Llama(
                model_path=path,
                n_ctx=2048,
                n_threads=6,
                n_gpu_layers=0,  # GPU-Layer auf 0 für maximale Stabilität
                verbose=False
            )
            return self.models["main"]
        except Exception as e:
            logging.error(f"❌ Fehler beim Laden des Modells {path}: {e}")
            return None

    def ask(self, prompt: str, purpose: str = "core") -> str:
        """
        DE: Stellt dem passenden Modell eine Frage.
        EN: Sends a prompt to the appropriate model.
        """
        if self.use_api:
            return self.ask_api(prompt)

        model = self.load_model(purpose)
        if model is None:
            if self.openai_client or self.claude_client:
                logging.warning("⚠ Lokales Modell fehlgeschlagen → API-Fallback.")
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
        """Nutzt GPT oder Claude API."""
        try:
            if self.api_choice == "gpt" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=512
                )
                return response.choices[0].message["content"].strip()

            elif self.api_choice == "claude" and self.claude_client:
                response = self.claude_client.messages.create(
                    model="claude-2",
                    max_tokens=512,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()

            return "❌ API-Modell nicht verfügbar oder API-Key fehlt."
        except Exception as e:
            logging.error(f"❌ Fehler bei API-Anfrage: {e}")
            return "❌ Fehler bei API-Anfrage."
