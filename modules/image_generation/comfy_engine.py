import requests
import os
import base64


from modules.image_generation import sd_engine, comfy_engine

def kimba_generate_image(prompt, purpose):
    model = get_model_by_purpose(purpose)
    
    if comfy_engine.is_comfyui_running():
        return comfy_engine.generate_image(prompt, model=model)
    else:
        return sd_engine.generate_image(prompt, purpose=purpose)
    

# ComfyUI API-URL – Port 8188 ist Standard für DirectML builds


COMFY_URL = os.getenv("COMFY_API_URL", "http://127.0.0.1:8188")

def is_comfyui_running():
    try:
        res = requests.get(f"{COMFY_URL}/system_stats")
        return res.status_code == 200
    except:
        return False

def generate_image(prompt, steps=30, sampler="euler", model="realisticVisionV5.safetensors"):
    payload = {
        "prompt": {
            "2": {
                "inputs": {
                    "ckpt_name": model,
                    "positive": f"{prompt}",
                    "negative": "",
                    "steps": steps,
                    "sampler_name": sampler,
                    "cfg": 7,
                    "seed": -1,
                    "denoise": 1.0,
                    "width": 512,
                    "height": 512,
                }
            }
        }
    }

    try:
        response = requests.post(f"{COMFY_URL}/prompt", json=payload)
        response.raise_for_status()
        prompt_id = response.json().get("prompt_id")

        # Jetzt Polling der Ergebnisse
        while True:
            result = requests.get(f"{COMFY_URL}/history/{prompt_id}")
            data = result.json()
            if prompt_id in data and "outputs" in data[prompt_id]:
                images = data[prompt_id]["outputs"]
                for node_id, node_output in images.items():
                    for img in node_output.get("images", []):
                        image_name = img["filename"]
                        image_url = f"{COMFY_URL}/view?filename={image_name}&type=output"
                        return image_url
    except Exception as e:
        raise RuntimeError(f"ComfyUI-Bildgenerierung fehlgeschlagen: {str(e)}")
