"""
Image Generator Module for Kimba (ComfyUI Workflow Integration)
===============================================================
DE: Nutzt die ComfyUI API, um Bilder über gespeicherte Workflows zu generieren.
EN: Uses the ComfyUI API to generate images via saved workflows.
"""

import requests
import logging
import json
import time
import os
from pathlib import Path

# ComfyUI Server Einstellungen
COMFYUI_HOST = "127.0.0.1"
COMFYUI_PORT = 8188
COMFYUI_URL = f"http://{COMFYUI_HOST}:{COMFYUI_PORT}"

# Speicherort für generierte Bilder
OUTPUT_DIR = "generated_images"

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def load_workflow(workflow_path: str) -> dict:
    """
    DE: Lädt einen gespeicherten Workflow aus einer JSON-Datei.
    EN: Loads a saved workflow from a JSON file.
    """
    with open(workflow_path, "r", encoding="utf-8") as f:
        return json.load(f)


def set_prompt_in_workflow(workflow_data: dict, prompt_text: str, model_name: str = None) -> dict:
    """
    DE: Ersetzt Prompt-Text (und optional Modellname) im Workflow.
    EN: Replaces prompt text (and optionally model name) in the workflow.
    """
    for node in workflow_data.get("nodes", []):
        # Prompt-Text ersetzen
        if "prompt" in node.get("inputs", {}):
            node["inputs"]["prompt"] = prompt_text
        # Modellname ersetzen
        if model_name and "ckpt_name" in node.get("inputs", {}):
            node["inputs"]["ckpt_name"] = f"{model_name}.safetensors"
    return workflow_data


def send_workflow_to_comfy(workflow_data: dict) -> str:
    """
    DE: Sendet den Workflow an ComfyUI und wartet auf das generierte Bild.
    EN: Sends the workflow to ComfyUI and waits for the generated image.
    """
    # 1. Workflow senden
    logging.info("📤 Sende Workflow an ComfyUI...")
    resp = requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": workflow_data})
    if resp.status_code != 200:
        return f"❌ Fehler beim Senden an ComfyUI: {resp.text}"

    prompt_id = resp.json().get("prompt_id")
    if not prompt_id:
        return "❌ Keine prompt_id erhalten."

    # 2. Auf Fertigstellung warten
    logging.info("⏳ Warte auf Bildgenerierung...")
    while True:
        hist = requests.get(f"{COMFYUI_URL}/history/{prompt_id}").json()
        if prompt_id in hist:
            output_data = hist[prompt_id]["outputs"]
            for node_id, node_output in output_data.items():
                if "images" in node_output:
                    img_info = node_output["images"][0]
                    img_filename = img_info["filename"]

                    # 3. Bild herunterladen
                    img_url = f"{COMFYUI_URL}/view?filename={img_filename}&subfolder={img_info['subfolder']}&type=output"
                    img_resp = requests.get(img_url)
                    os.makedirs(OUTPUT_DIR, exist_ok=True)
                    save_path = Path(OUTPUT_DIR) / f"{int(time.time())}_{img_filename}"
                    with open(save_path, "wb") as f:
                        f.write(img_resp.content)
                    logging.info(f"✅ Bild gespeichert: {save_path}")
                    return str(save_path)
        time.sleep(1)


def generate_image_with_comfy(prompt_text: str, model_name: str = None, workflow_path: str = "default_workflow.json") -> str:
    """
    DE: Generiert ein Bild über einen gespeicherten ComfyUI-Workflow.
    EN: Generates an image using a saved ComfyUI workflow.
    """
    try:
        # Workflow laden
        workflow_data = load_workflow(workflow_path)

        # Prompt + Modell einfügen
        workflow_data = set_prompt_in_workflow(workflow_data, prompt_text, model_name)

        # Workflow senden & Ergebnis holen
        result_path = send_workflow_to_comfy(workflow_data)
        return result_path
    except Exception as e:
        logging.error(f"❌ Fehler bei der Bildgenerierung: {e}")
        return f"❌ Fehler: {e}"
