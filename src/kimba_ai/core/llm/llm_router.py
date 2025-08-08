# core/llm_router.py
import os, requests
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.kimba_ai.core.personas.persona_manager import PersonaManager

load_dotenv()

class KimbaLLMRouter:
    def __init__(self, persona_manager=None, memory_manager=None, model_choice="Phi-3-mini-4k-instruct"):
        self.persona_manager = persona_manager or PersonaManager()
        self.memory_manager = memory_manager    # ✅ neu

        self.active_persona = "Iuno"
        self.model_map = {
            "Phi-3-mini-4k-instruct": {
                "local_dir": "./models/Phi-3-mini-4k-instruct",
                "hf_id": "microsoft/Phi-3-mini-4k-instruct"
            }
        }
        self.local_dir = self.model_map[model_choice]["local_dir"]
        self.hf_model_id = self.model_map[model_choice]["hf_id"]
        self.local_model = None
        self.tokenizer = None

        self.api_chain = [
            {"name":"OpenAI GPT","url":"https://api.openai.com/v1/chat/completions","token":os.getenv("OPENAI_API_KEY"),"model":"gpt-4o-mini","limit":50_000},
            {"name":"DeepInfra","url":"https://api.deepinfra.com/v1/openai/chat/completions","token":os.getenv("DEEPINFRA_API_KEY"),"model":"mistralai/Mistral-7B-Instruct-v0.3","limit":500_000},
            {"name":"OpenRouter","url":"https://openrouter.ai/api/v1/chat/completions","token":os.getenv("OPENROUTER_API_KEY"),"model":"mistralai/mixtral-8x7b-instruct","limit":2_000_000},
            {"name":"HuggingFace","url":"https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3","token":os.getenv("HUGGINGFACE_API_KEY"),"model":None,"limit":1_000_000},
        ]
        self.api_usage = {api["name"]: 0 for api in self.api_chain}

    def set_active_persona(self, name: str):
        self.persona_manager.set_active_persona(name)
        self.active_persona = name

    def load_model(self):
        print(f"[INFO] 📥 Lade lokales Modell: {self.local_dir}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.local_dir, trust_remote_code=True)
        self.local_model = AutoModelForCausalLM.from_pretrained(
            self.local_dir, torch_dtype="auto", device_map="auto", trust_remote_code=True
        )

    def _augment_with_memories(self, user_text: str) -> str:
        """Fügt Top-Recall dem Prompt hinzu (falls MemoryManager vorhanden)."""
        if not self.memory_manager:
            return user_text
        try:
            hits = self.memory_manager.recall(user_text, limit=3)  # [(sim, mem), ...]
            if not hits:
                return user_text
            lines = []
            for sim, mem in hits:
                txt = mem.get("text", "")
                cat = mem.get("category", "general")
                prj = mem.get("project") or ""
                lines.append(f"- {txt} ({cat}{', ' + prj if prj else ''}; rel: {sim:.2f})")
            return "[Memories]\n" + "\n".join(lines) + f"\n\n[User]\n{user_text}"
        except Exception as e:
            return f"[Memories]\n- (recall error: {e})\n\n[User]\n{user_text}"

    def ask_local(self, prompt, max_tokens=512):
        persona_prompt = self.persona_manager.get_active_prompt()
        full_prompt = f"{persona_prompt}\n{prompt}"
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.local_model.device)
        outputs = self.local_model.generate(**inputs, max_new_tokens=max_tokens, do_sample=True, temperature=0.7)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def ask_api(self, prompt, max_tokens=512):
        persona_prompt = self.persona_manager.get_active_prompt()
        api_prompt = f"{persona_prompt}\n{prompt}"
        for api in self.api_chain:
            if not api["token"]:
                continue
            headers = {"Authorization": f"Bearer {api['token']}"}
            if api["name"] == "HuggingFace":
                payload = {"inputs": api_prompt, "parameters": {"max_new_tokens": max_tokens}}
            else:
                payload = {"model": api["model"], "messages":[
                    {"role":"system","content": persona_prompt},
                    {"role":"user","content": prompt}
                ], "max_tokens": max_tokens}
            try:
                r = requests.post(api["url"], headers=headers, json=payload, timeout=60)
                if r.status_code == 200:
                    self.api_usage[api["name"]] += len(prompt.split()) + max_tokens
                    data = r.json()
                    return data[0]["generated_text"] if api["name"]=="HuggingFace" else data["choices"][0]["message"]["content"]
                else:
                    print(f"[WARN] API {api['name']} Fehler: {r.status_code}")
            except Exception as e:
                print(f"[WARN] API {api['name']} Exception: {e}")
        return None

    def ask(self, prompt, return_source=False):
        prompt = self._augment_with_memories(prompt)  # ✅
        api_response = self.ask_api(prompt)
        if api_response:
            return (api_response, "API") if return_source else api_response
        print("[INFO] 🌙 Alle APIs fehlgeschlagen – wechsle zu lokalem Modell...")
        if self.local_model is None:
            self.load_model()
        local_response = self.ask_local(prompt)
        return (local_response, "LOCAL") if return_source else local_response

    def ask_persona(self, persona_name, prompt, return_source=False):
        self.set_active_persona(persona_name)
        prompt = self._augment_with_memories(prompt)  # ✅
        api_response = self.ask_api(prompt)
        if api_response:
            return (api_response, "API") if return_source else api_response
        print("[INFO] 🌙 Alle APIs fehlgeschlagen – wechsle zu lokalem Modell...")
        if self.local_model is None:
            self.load_model()
        local_response = self.ask_local(prompt)
        return (local_response, "LOCAL") if return_source else local_response
