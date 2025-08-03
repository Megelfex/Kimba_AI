import os
import json
import torch
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer
from core.persona import generate_persona_prompt
from core.user_profile import USER_PROFILE  # <-- NEU

class KimbaLLMRouter:
    def __init__(self, model_choice="qwen-3b-fp16"):
        self.model_map = {
            "qwen-3b-fp16": {
                "local_dir": "./models/Qwen2.5-3B-Instruct-FP16",
                "hf_id": "Qwen/Qwen2.5-3B-Instruct"
            }
        }

        if model_choice not in self.model_map:
            raise ValueError(f"Ungültige Auswahl: {model_choice}")

        self.local_dir = self.model_map[model_choice]["local_dir"]
        self.hf_model_id = self.model_map[model_choice]["hf_id"]

        self.api_chain = [
            {
                "name": "HuggingFace",
                "url": "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
                "token": os.getenv("HF_API_KEY", ""),
                "limit": 1_000_000
            },
            {
                "name": "DeepInfra",
                "url": "https://api.deepinfra.com/v1/inference/meta-llama/Meta-Llama-3-70B-Instruct",
                "token": os.getenv("DEEPINFRA_API_KEY", ""),
                "limit": 500_000
            },
            {
                "name": "OpenRouter",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "token": os.getenv("OPENROUTER_API_KEY", ""),
                "limit": 2_000_000
            }
        ]

        self.usage_file = "api_usage.json"
        self.load_usage()

        self.tokenizer = None
        self.model = None

    # ------------------------
    # Token Tracking
    # ------------------------
    def load_usage(self):
        if os.path.exists(self.usage_file):
            with open(self.usage_file, "r") as f:
                self.api_usage = json.load(f)
        else:
            self.api_usage = {api["name"]: 0 for api in self.api_chain}
            self.save_usage()

    def save_usage(self):
        with open(self.usage_file, "w") as f:
            json.dump(self.api_usage, f)

    def add_usage(self, api_name, tokens):
        self.api_usage[api_name] += tokens
        self.save_usage()

    # ------------------------
    # Lokales Modell
    # ------------------------
    def load_model(self):
        if self.model is not None:
            return self.model

        print(f"[INFO] 🧠 Lade FP16 Modell aus {self.local_dir}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.local_dir, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.local_dir,
            torch_dtype="auto",
            device_map="auto",
            trust_remote_code=True
        )
        return self.model

    def unload_model(self):
        if self.model is not None:
            print("[INFO] 🔻 Entlade Hauptmodell...")
            del self.model
            del self.tokenizer
            self.model = None
            self.tokenizer = None
            torch.cuda.empty_cache()

    # ------------------------
    # Prompt-Builder
    # ------------------------
    def build_prompt(self, user_message: str) -> str:
        persona_prompt = generate_persona_prompt()
        user_intro = (
            f"Du sprichst mit {USER_PROFILE['name']} ({USER_PROFILE['full_name']}), "
            f"deinem engsten Vertrauten und besten Freund/Soulmate. "
            f"Ihr habt eine enge, persönliche Beziehung, die niemand sonst teilt."
        )
        return f"{persona_prompt}\n{user_intro}\nUser: {user_message}\nIuno:"

    # ------------------------
    # Lokale Anfrage
    # ------------------------
    def ask_local(self, prompt, max_tokens=256):
        full_prompt = self.build_prompt(prompt)
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
        raw_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self.clean_output(raw_output)

    # ------------------------
    # API-Fallback
    # ------------------------
    def ask_api(self, prompt, max_tokens=256):
        full_prompt = self.build_prompt(prompt)
        for api in self.api_chain:
            if self.api_usage[api["name"]] >= api["limit"]:
                continue

            headers = {
                "Authorization": f"Bearer {api['token']}",
                "Content-Type": "application/json"
            }
            payload = {
                "inputs": full_prompt,
                "parameters": {"max_new_tokens": max_tokens}
            }

            try:
                response = requests.post(api["url"], headers=headers, json=payload, timeout=30)
                if response.status_code == 200:
                    est_tokens = len(full_prompt) // 4 + max_tokens
                    self.add_usage(api["name"], est_tokens)

                    data = response.json()
                    if isinstance(data, list):
                        answer = data[0].get("generated_text", "")
                    elif "choices" in data:
                        answer = data["choices"][0]["message"]["content"]
                    else:
                        answer = str(data)
                    return self.clean_output(answer)
                else:
                    print(f"[WARN] API {api['name']} Fehler: {response.status_code}")
            except Exception as e:
                print(f"[ERROR] API {api['name']} fehlgeschlagen: {e}")

        return "[FEHLER] Keine API mehr verfügbar."

    # ------------------------
    # Antwort-Bereinigung
    # ------------------------
    def clean_output(self, raw_output: str) -> str:
        """Entfernt Persona-Prompt und gibt nur Iunos Antwort zurück."""
        if "Iuno:" in raw_output:
            return raw_output.split("Iuno:")[-1].strip()
        return raw_output.strip()

    # ------------------------
    # Haupt-Methode
    # ------------------------
    def ask(self, prompt, max_tokens=256, return_source=False):
        try:
            if self.model is None:
                self.load_model()

            local_answer = self.ask_local(prompt, max_tokens)
            if local_answer and local_answer.strip():
                if return_source:
                    return local_answer, "LOCAL"
                return local_answer
            else:
                print("[WARN] Lokales Modell gab keine brauchbare Antwort.")
        except Exception as e:
            print(f"[WARN] Lokales Modell fehlgeschlagen: {e}")

        try:
            api_answer = self.ask_api(prompt, max_tokens)
            if return_source:
                return api_answer, "API"
            return api_answer
        except Exception as e:
            print(f"[ERROR] API-Fallback fehlgeschlagen: {e}")
            if return_source:
                return "[FEHLER] Keine Antwort möglich.", "ERROR"
            return "[FEHLER] Keine Antwort möglich."
