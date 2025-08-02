import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class KimbaLLMRouter:
    def __init__(self, model_choice="tinyllama"):
        """
        model_choice:
        - "tinyllama"  → TinyLlama-1.1B-Chat-v1.0 (klein, schnell)
        - "nous-hermes" → Nous-Hermes-2-Mistral-7B-DPO (stärker, langsamer)
        """
        self.model_map = {
            "tinyllama": {
                "local_dir": "./models/TinyLlama",
                "hf_id": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
            },
            "nous-hermes": {
                "local_dir": "./models/Nous-Hermes-2-Mistral-7B-DPO",
                "hf_id": "NousResearch/Nous-Hermes-2-Mistral-7B-DPO"
            }
        }

        if model_choice not in self.model_map:
            raise ValueError(f"Ungültige Auswahl: {model_choice}")

        self.local_dir = self.model_map[model_choice]["local_dir"]
        self.hf_model_id = self.model_map[model_choice]["hf_id"]

        self.tokenizer = None
        self.model = None

    def is_model_complete(self):
        """Prüft, ob das Modellverzeichnis vollständig ist."""
        required_files = ["config.json", "tokenizer.json", "pytorch_model.bin"]
        return all(os.path.exists(os.path.join(self.local_dir, f)) for f in required_files)

    def load_model(self):
        """Lädt Modell lokal oder lädt es herunter, falls es fehlt."""
        if self.model is not None:
            return self.model

        if self.is_model_complete():
            print(f"[INFO] 🧠 Lade Modell lokal aus {self.local_dir}")
            model_path = self.local_dir
        else:
            print(f"[INFO] 📥 Lade Modell von Hugging Face: {self.hf_model_id}")
            os.makedirs(self.local_dir, exist_ok=True)
            model_path = self.hf_model_id

        self.tokenizer = AutoTokenizer.from_pretrained(model_path, cache_dir=self.local_dir)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            cache_dir=self.local_dir,
            torch_dtype=torch.float32,  # CPU-kompatibel
            device_map="auto"
        )

        if not self.is_model_complete():
            print(f"[INFO] 💾 Speichere Modell nach {self.local_dir}...")
            self.tokenizer.save_pretrained(self.local_dir)
            self.model.save_pretrained(self.local_dir)

        print("[INFO] ✅ Modell erfolgreich geladen!")
        return self.model

    def ask(self, prompt: str, max_tokens: int = 256) -> str:
        """Sendet eine Anfrage an das Modell."""
        if self.model is None:
            self.load_model()

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
