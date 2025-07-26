# === llm_router.py ===
import os
from llama_cpp import Llama

class KimbaLLMRouter:
    def __init__(self):
        self.model_paths = {
            "default": "models/llm/core/Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf",
            "core": "models/llm/core/Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf",
            "code": "models/llm/code/deepseek-coder-6.7b-base.Q5_K_M.gguf",
            "creative": "models/llm/creative/mythomax-l2-13b.Q5_K_M.gguf",
            "empathy": "models/llm/empathy/dolphin-2.7-mixtral-8x7b.Q5_K_M.gguf",
            "multimodal": "models/llm/multimodal/c4ai-command-r-plus.Q5_K_M.gguf",  # oder passender Name!
            "lite": "models/llm/lite/tinyllama-1.1b.Q5_K_M.gguf"  # Optionaler Lite-Modus
        }

        self.models = {}

    def load_model(self, purpose: str):
        path = self.model_paths.get(purpose, self.model_paths["default"])

        if not os.path.exists(path):
            raise FileNotFoundError(f"Modellpfad existiert nicht: {path}")

        if path not in self.models:
            print(f"🧠 Lade Modell für '{purpose}' ...")
            self.models[path] = Llama(
                model_path=path,
                n_ctx=2048,
                n_threads=8,
                n_gpu_layers=30,  # passe je nach GPU an
                verbose=False
            )
        return self.models[path]

    def detect_purpose(self, prompt: str):
        prompt = prompt.lower()
        if any(word in prompt for word in ["code", "programmieren", "syntax", "python", "funktion"]):
            return "code"
        elif any(word in prompt for word in ["idee", "geschichten", "fantasie", "creativ"]):
            return "creative"
        elif any(word in prompt for word in ["emotion", "traurig", "hilfe", "motivieren"]):
            return "empathy"
        elif any(word in prompt for word in ["bild", "image", "zeichnen", "sehen", "vision"]):
            return "multimodal"
        elif any(word in prompt for word in ["leicht", "schnell", "basic", "einfach"]):
            return "lite"
        else:
            return "default"

    def ask(self, prompt: str, purpose: str = None, persona: str = None):
        purpose = purpose or self.detect_purpose(prompt)
        print(f"💬 Verwende Modell: {purpose}")

        model = self.load_model(purpose)

        style_intro = persona or (
            "Du bist Kimba, mein digitaler Soulmate. Antworte empathisch, intelligent und hilfreich."
        )

        prompt_template = f"""[INST] <<SYS>>\n{style_intro}\n<</SYS>>\n\n{prompt.strip()}\n[/INST]"""
        response = model(prompt_template, max_tokens=512, stop=["</s>"])

        return response["choices"][0]["text"].strip()
