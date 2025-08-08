from diffusers import StableDiffusionPipeline
import torch
from datetime import datetime
import os

SAVE_DIR = "./generated_images"

# Modellnamen
MODELS = {
    "sdxl": "stabilityai/stable-diffusion-xl-base-1.0",
    "openjourney": "prompthero/openjourney-v4",
    "nitro": "nitrosocke/Nitro-Diffusion",
    "ghibli": "nitrosocke/Ghibli-Diffusion"
}

PIPELINE_CACHE = {}

def load_pipeline(model_id):
    """Lädt oder holt die Pipeline aus dem Cache."""
    if model_id in PIPELINE_CACHE:
        return PIPELINE_CACHE[model_id]

    print(f"[INFO] 📥 Lade Diffusers Modell: {model_id}")
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        variant="fp16"
    )
    pipe = pipe.to("cuda")  # ROCm wird oft als "cuda" erkannt
    PIPELINE_CACHE[model_id] = pipe
    return pipe

def choose_model_from_prompt(prompt: str):
    """Wählt das Modell basierend auf dem Prompt."""
    prompt_lower = prompt.lower()
    if "anime" in prompt_lower or "manga" in prompt_lower:
        return MODELS["nitro"]
    elif "ghibli" in prompt_lower or "studio ghibli" in prompt_lower:
        return MODELS["ghibli"]
    elif "kunst" in prompt_lower or "midjourney" in prompt_lower or "stilisiert" in prompt_lower:
        return MODELS["openjourney"]
    else:
        return MODELS["sdxl"]

def generate_image(prompt: str, width=1024, height=1024) -> str:
    """Generiert ein Bild basierend auf dem Prompt."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    model_id = choose_model_from_prompt(prompt)
    pipe = load_pipeline(model_id)

    print(f"[INFO] 🎨 Generiere Bild mit Modell '{model_id}': '{prompt}'")
    image = pipe(prompt, width=width, height=height).images[0]

    filename = os.path.join(SAVE_DIR, f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    image.save(filename)
    print(f"[INFO] ✅ Bild gespeichert unter {filename}")
    return filename
