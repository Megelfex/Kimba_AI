import os
import requests
from llama_cpp import Llama
from openai import OpenAI
import anthropic
import os
import requests
from pathlib import Path
import json

class KimbaLLMRouter:
    def __init__(self, use_api=False, api_choice="gpt"):
        # Pfade zu deinen Kernmodellen
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

        # API-Clients vorbereiten
        self.gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def load_model(self, purpose: str):
        path = self.model_paths.get(purpose, self.model_paths["core"])
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
        if path not in self.models:
            print(f"🧠 Loading model for '{purpose}'...")
            self.models[path] = Llama(
                model_path=path,
                n_ctx=4096,
                n_threads=8,
                n_gpu_layers=35,
                verbose=False
            )
        return self.models[path]

    def ask_local(self, prompt: str, purpose: str):
        model = self.load_model(purpose)
        response = model(
            f"[INST] {prompt} [/INST]",
            max_tokens=512,
            stop=["</s>"]
        )
        return response["choices"][0]["text"].strip()

    def ask_gpt(self, prompt: str):
        completion = self.gpt_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

    def ask_claude(self, prompt: str):
        response = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def ask(self, prompt: str, purpose="core"):
        if self.use_api:
            if self.api_choice == "gpt":
                return self.ask_gpt(prompt)
            elif self.api_choice == "claude":
                return self.ask_claude(prompt)
        return self.ask_local(prompt, purpose)

    # === Bildgenerierung mit ComfyUI ===
    def generate_image(self, prompt: str, output_path="output.png"):
        print("🎨 Generating image via ComfyUI...")
        payload = {
            "prompt": prompt,
            "parameters": {"steps": 30, "width": 512, "height": 512}
        }
        try:
            r = requests.post("http://127.0.0.1:8188/prompt", json=payload)
            if r.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(r.content)
                return f"Image saved to {output_path}"
            else:
                return f"ComfyUI error: {r.text}"
        except Exception as e:
            return f"ComfyUI connection failed: {e}"
        
    def __init__(self, use_api=False, api_choice="gpt"):
        self.use_api = use_api
        self.api_choice = api_choice

        # ComfyUI API URL
        self.comfyui_url = "http://127.0.0.1:8188"

        # LLM-Modelldir (gguf)
        self.llm_base_path = Path("models")

        # ComfyUI Checkpoints Pfad (safetensors)
        self.image_models_path = Path("tools/comfyui/models/checkpoints")

    # -------------------
    # LLM MODEL LISTING
    # -------------------
    def list_llm_models(self):
        """Listet alle GGUF-Dateien in den Models-Unterordnern."""
        llm_models = []
        for root, dirs, files in os.walk(self.llm_base_path):
            for file in files:
                if file.endswith(".gguf"):
                    rel_path = os.path.relpath(os.path.join(root, file), self.llm_base_path)
                    llm_models.append(rel_path)
        return llm_models

    # -------------------
    # IMAGE MODEL LISTING
    # -------------------
    def list_image_models(self):
        """Listet alle .safetensors im ComfyUI-Ordner."""
        return [f.name for f in self.image_models_path.glob("*.safetensors")]

    # -------------------
    # COMFYUI IMAGE GENERATION
    # -------------------
    def generate_image_comfyui(self, prompt, model_name, output_path="output.png"):
        """Sendet Prompt an ComfyUI und speichert Bild."""
        workflow = {
            "prompt": prompt,
            "model": model_name,
            "steps": 30,
            "width": 512,
            "height": 512
        }

        try:
            r = requests.post(f"{self.comfyui_url}/prompt", json=workflow)
            r.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(r.content)

            return f"Bild gespeichert unter {output_path}"
        except Exception as e:
            return f"[ComfyUI Fehler] {str(e)}"
        
    import os
from pathlib import Path
import requests
from llama_cpp import Llama

class KimbaLLMRouter:
    def __init__(self, use_api=False, api_choice="gpt"):
        self.use_api = use_api
        self.api_choice = api_choice
        self.llm_base_path = Path("models")
        self.image_models_path = Path("tools/comfyui/models/checkpoints")
        self.models = {}
        self.current_model_path = None
        self.llm_instance = None

    # -------------------
    # LIST LOCAL LLM MODELS
    # -------------------
    def list_llm_models(self):
        llm_models = []
        for root, dirs, files in os.walk(self.llm_base_path):
            for file in files:
                if file.endswith(".gguf"):
                    rel_path = os.path.relpath(os.path.join(root, file), self.llm_base_path)
                    llm_models.append(rel_path)
        return llm_models

    # -------------------
    # LIST IMAGE MODELS
    # -------------------
    def list_image_models(self):
        return [f.name for f in self.image_models_path.glob("*.safetensors")]

    # -------------------
    # SET LLM MODEL LIVE
    # -------------------
    def set_llm_model(self, model_name):
        """Wechselt das aktive LLM-Modell sofort"""
        model_path = self.llm_base_path / model_name
        if not model_path.exists():
            return f"⚠ Modell nicht gefunden: {model_name}"

        self.current_model_path = str(model_path)
        self.llm_instance = Llama(
            model_path=str(model_path),
            n_ctx=4096,
            n_threads=8,
            n_batch=512,
            verbose=False
        )
        return f"✅ LLM gewechselt zu: {model_name}"

    # -------------------
    # ASK USING CURRENT MODEL
    # -------------------
    def ask_local(self, prompt):
        if not self.llm_instance:
            return "⚠ Kein Modell geladen. Bitte zuerst im Dropdown auswählen."

        output = self.llm_instance(
            f"[INST] {prompt} [/INST]",
            max_tokens=512,
            stop=["</s>"]
        )
        return output["choices"][0]["text"].strip()

    # -------------------
    # COMFYUI IMAGE GENERATION
    # -------------------
    def generate_image_comfyui(self, prompt, model_name, output_path="output.png"):
        workflow = {
            "prompt": prompt,
            "model": model_name,
            "steps": 30,
            "width": 512,
            "height": 512
        }
        try:
            r = requests.post("http://127.0.0.1:8188/prompt", json=workflow)
            r.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(r.content)
            return f"Bild gespeichert unter {output_path}"
        except Exception as e:
            return f"[ComfyUI Fehler] {str(e)}"
    

        
