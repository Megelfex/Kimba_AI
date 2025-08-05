import os
import requests
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
from core.longterm_memory import semantic_search
from core.persona_manager import PersonaManager

# Lade .env Datei
load_dotenv()

class KimbaLLMRouter:
    def __init__(self, model_choice="Phi-3-mini-4k-instruct"):
        # Persona Manager initialisieren
        self.persona_manager = PersonaManager()

        # Lokale Modell-Infos
        self.model_map = {
            "Phi-3-mini-4k-instruct": {
                "local_dir": "./models/Phi-3-mini-4k-instruct",
                "hf_id": "microsoft/Phi-3-mini-4k-instruct"
            }
        }
        self.local_dir = self.model_map[model_choice]["local_dir"]
        self.hf_model_id = self.model_map[model_choice]["hf_id"]

        # API-Kette mit Token aus .env
        self.api_chain = [
            {
                "name": "OpenAI GPT",
                "url": "https://api.openai.com/v1/chat/completions",
                "token": os.getenv("OPENAI_API_KEY"),
                "model": "gpt-4o-mini",
                "limit": 50_000
            },
            {
                "name": "DeepInfra",
                "url": "https://api.deepinfra.com/v1/openai/chat/completions",
                "token": os.getenv("DEEPINFRA_API_KEY"),
                "model": "mistralai/Mistral-7B-Instruct-v0.3",
                "limit": 500_000
            },
            {
                "name": "OpenRouter",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "token": os.getenv("OPENROUTER_API_KEY"),
                "model": "mistralai/mixtral-8x7b-instruct",
                "limit": 2_000_000
            },
            {
                "name": "HuggingFace",
                "url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
                "token": os.getenv("HUGGINGFACE_API_KEY"),
                "model": None,
                "limit": 1_000_000
            }
        ]

        self.api_usage = {api["name"]: 0 for api in self.api_chain}
        self.local_model = None
        self.tokenizer = None

    # ---------------------------------------------------
    # Lokales Modell laden
    # ---------------------------------------------------
    def load_model(self):
        print(f"[INFO] 📥 Lade lokales Modell: {self.local_dir}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.local_dir, trust_remote_code=True)
        self.local_model = AutoModelForCausalLM.from_pretrained(
            self.local_dir,
            torch_dtype="auto",
            device_map="auto",
            trust_remote_code=True
        )

    # ---------------------------------------------------
    # Lokale Anfrage
    # ---------------------------------------------------
    def ask_local(self, prompt, max_tokens=512):
        persona_prompt = self.persona_manager.get_active_prompt()
        full_prompt = persona_prompt + "\n" + prompt
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.local_model.device)
        outputs = self.local_model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.7
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    # ---------------------------------------------------
    # API-Anfrage
    # ---------------------------------------------------
    def ask_api(self, prompt, max_tokens=512):
        persona_prompt = self.persona_manager.get_active_prompt()
        api_prompt = persona_prompt + "\n" + prompt

        for api in self.api_chain:
            if not api["token"]:
                continue

            headers = {"Authorization": f"Bearer {api['token']}"}
            if api["name"] == "HuggingFace":
                payload = {"inputs": api_prompt, "parameters": {"max_new_tokens": max_tokens}}
            else:
                payload = {
                    "model": api["model"],
                    "messages": [
                        {"role": "system", "content": persona_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": max_tokens
                }

            try:
                r = requests.post(api["url"], headers=headers, json=payload, timeout=60)
                if r.status_code == 200:
                    self.api_usage[api["name"]] += len(prompt.split()) + max_tokens
                    data = r.json()
                    if api["name"] == "HuggingFace":
                        return data[0]["generated_text"]
                    else:
                        return data["choices"][0]["message"]["content"]
                else:
                    print(f"[WARN] API {api['name']} Fehler: {r.status_code}")
            except Exception as e:
                print(f"[WARN] API {api['name']} Exception: {e}")
        return None

    # ---------------------------------------------------
    # API-First mit Local-Fallback + Erinnerungskontext
    # ---------------------------------------------------
    def ask(self, prompt, return_source=False):
        # 🔍 Semantische Suche für Erinnerungen
        memory_hits = []
        results = semantic_search(prompt, limit=3)
        for sim, _, ts, content, mood, category, tags in results:
            memory_hits.append(f"- {content} ({category}, Relevanz: {sim:.2f})")

        if memory_hits:
            prompt = f"[Erinnerungen]\n" + "\n".join(memory_hits) + f"\n\n[Nutzer]\n{prompt}"

        # 1️⃣ API-First
        api_response = self.ask_api(prompt)
        if api_response:
            return (api_response, "API") if return_source else api_response

        # 2️⃣ Lokales Modell als Fallback
        print("[INFO] 🌙 Alle APIs fehlgeschlagen – wechsle zu lokalem Modell...")
        if self.local_model is None:
            self.load_model()
        local_response = self.ask_local(prompt)
        return (local_response, "LOCAL") if return_source else local_response
