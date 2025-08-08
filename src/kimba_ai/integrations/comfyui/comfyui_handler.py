import requests
import time
import os
from pathlib import Path
from datetime import datetime

# ComfyUI Server-URL
COMFYUI_API_URL = "http://127.0.0.1:8188"
COMFYUI_OUTPUT_DIR = Path("./ComfyUI/output")
GENERATED_PATH = Path("./generated_images")

def generate_image_with_comfy(prompt: str) -> str:
    """Schickt Prompt an ComfyUI, wartet auf Ergebnis und gibt Bildpfad zurück."""
    print(f"[INFO] 🎨 Sende Prompt an ComfyUI: {prompt}")
    GENERATED_PATH.mkdir(exist_ok=True)

    # API Payload (abhängig von deinem Workflow)
    # Hier Beispiel für einen einfachen Text-to-Image-Workflow
    payload = {
        "prompt": {
            "1": {  # Node-ID in deinem Workflow
                "inputs": {
                    "text": prompt
                },
                "class_type": "CLIPTextEncode"
            }
        }
    }

    # Prompt an ComfyUI senden
    response = requests.post(f"{COMFYUI_API_URL}/prompt", json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"[ERROR] ComfyUI-API-Fehler: {response.text}")

    # Job-ID extrahieren
    job_id = response.json()["prompt_id"]
    print(f"[INFO] 🏭 Job-ID: {job_id}")

    # Auf Bild warten (Polling)
    print("[INFO] ⏳ Warte auf Bild...")
    image_path = None
    start_time = time.time()

    while time.time() - start_time < 60:  # max. 60 Sek. warten
        time.sleep(2)
        if COMFYUI_OUTPUT_DIR.exists():
            images = sorted(COMFYUI_OUTPUT_DIR.glob("*.png"), key=os.path.getmtime, reverse=True)
            if images:
                latest_image = images[0]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                final_path = GENERATED_PATH / f"image_{timestamp}.png"
                latest_image.replace(final_path)
                image_path = str(final_path)
                break

    if not image_path:
        raise RuntimeError("[ERROR] Kein Bild gefunden.")

    print(f"[INFO] ✅ Bild gespeichert unter: {image_path}")
    return image_path
