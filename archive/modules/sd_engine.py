# modules/image_generation/sd_engine.py
# This module allows Kimba to generate images using a local Stable Diffusion backend (Automatic1111 via API)

import requests
import os

# Define the URL to the AUTOMATIC1111 Web UI API
API_URL = os.getenv("SD_API_URL", "http://127.0.0.1:7860")

def get_model_by_purpose(purpose: str) -> str:
    # Einfach anpassen nach deinem Modellnamen im ComfyUI/models/checkpoints
    model_map = {
        "realistic": "realisticVisionV5.safetensors",
        "anime": "anythingV5.safetensors",
        "inpainting": "inpaintDiffusion.safetensors",
        "art": "dreamshaper.safetensors",
        "default": "realisticVisionV5.safetensors"
    }
    return model_map.get(purpose.lower(), model_map["default"])




def generate_image(prompt: str, steps: int = 30, cfg_scale: float = 7.0, sampler_name: str = "Euler a", seed: int = -1, width: int = 512, height: int = 512, model: str = "Realistic Vision V6.0") -> str:
    """
    Sends a request to the AUTOMATIC1111 API to generate an image.

    Returns the path to the saved image or raises an exception.

    """
    model = get_model_by_purpose(purpose)  # 'purpose' musst du von Kimba übergeben lassen



    payload = {
        "prompt": prompt,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "sampler_name": sampler_name,
        "seed": seed,
        "width": width,
        "height": height,
        "override_settings": {
            "sd_model_checkpoint": model
        }
    }

    try:
        response = requests.post(f"{API_URL}/sdapi/v1/txt2img", json=payload)
        response.raise_for_status()
        result = response.json()

        # Save base64 image to file
        image_data = result["images"][0]
        image_bytes = bytes(image_data, encoding='utf-8')
        file_path = f"outputs/generated_kimba_{seed if seed != -1 else 'random'}.png"
        with open(file_path, "wb") as f:
            f.write(requests.utils.unquote_to_bytes(image_data))

        return file_path
    except Exception as e:
        raise RuntimeError(f"Fehler beim Generieren des Bildes: {str(e)}")
