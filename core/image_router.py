import os
import json
import openai
from datetime import datetime
from diffusers import StableDiffusionPipeline
import torch

class KimbaImageRouter:
    def __init__(self):
        # API-Setup
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        openai.api_key = self.openai_api_key

        self.dalle_model = "dall-e-3"
        self.dalle_budget_usd = 20.0  # Monatsbudget in USD
        self.dalle_price_per_image = 0.04  # 1024x1024 Preis in USD

        # Stable Diffusion Setup (lokales Modell)
        self.local_model_dir = "./models/stable-diffusion-xl-base-1.0"
        self.local_pipeline = None

        # Usage-Tracking
        self.usage_file = "image_usage.json"
        self.load_usage()

    # ---------------- Usage Management ----------------
    def load_usage(self):
        if os.path.exists(self.usage_file):
            with open(self.usage_file, "r") as f:
                self.image_usage = json.load(f)
        else:
            self.image_usage = {"OpenAI_DALLE": 0.0, "month": datetime.now().month}
            self.save_usage()

        # Reset, wenn neuer Monat
        if self.image_usage["month"] != datetime.now().month:
            self.image_usage = {"OpenAI_DALLE": 0.0, "month": datetime.now().month}
            self.save_usage()

    def save_usage(self):
        with open(self.usage_file, "w") as f:
            json.dump(self.image_usage, f)

    def add_usage(self, cost):
        self.image_usage["OpenAI_DALLE"] += cost
        self.save_usage()

    def budget_exceeded(self):
        return self.image_usage["OpenAI_DALLE"] >= self.dalle_budget_usd

    # ---------------- API-Image Generation ----------------
    def generate_dalle(self, prompt, size="1024x1024"):
        if not self.openai_api_key:
            raise ValueError("Kein OpenAI API Key für DALL·E gesetzt.")

        if self.budget_exceeded():
            print("[INFO] 💰 DALL·E Budget erreicht – Fallback auf lokales Modell.")
            return None

        try:
            response = openai.Image.create(
                model=self.dalle_model,
                prompt=prompt,
                size=size
            )
            image_url = response['data'][0]['url']
            self.add_usage(self.dalle_price_per_image)
            print(f"[INFO] 🖼️ DALL·E Bild erstellt: {image_url}")
            return image_url
        except Exception as e:
            print(f"[ERROR] DALL·E API fehlgeschlagen: {e}")
            return None

    # ---------------- Lokale Image Generation ----------------
    def load_local_pipeline(self):
        if self.local_pipeline is None:
            print("[INFO] 🧠 Lade lokales Stable Diffusion Modell...")
            self.local_pipeline = StableDiffusionPipeline.from_pretrained(
                self.local_model_dir,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            self.local_pipeline = self.local_pipeline.to("cuda" if torch.cuda.is_available() else "cpu")

    def generate_local(self, prompt):
        self.load_local_pipeline()
        image = self.local_pipeline(prompt).images[0]
        output_path = f"output_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image.save(output_path)
        print(f"[INFO] 🖼️ Lokales Bild gespeichert unter: {output_path}")
        return output_path

    # ---------------- Haupt-Logik ----------------
    def generate_image(self, prompt, size="1024x1024"):
        # Erst DALL·E probieren
        url = self.generate_dalle(prompt, size)
        if url:
            return {"source": "DALL·E", "path_or_url": url}

        # Fallback auf lokales Modell
        local_path = self.generate_local(prompt)
        return {"source": "Local", "path_or_url": local_path}
