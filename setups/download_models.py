import os
import subprocess
from pathlib import Path

TARGET_DIR = Path("C:/Users/elex/Documents/GitHub/Kimba_AI/models")

models = {
    "llm": {
        "core": ("TheBloke/Llama-3.1-8B-Instruct-GGUF", "llama3.1-8b-instruct.Q4_K_M.gguf"),
        "creative": ("TheBloke/MythoMax-L2-13B-GGUF", "mythomax-l2-13b.Q4_K_M.gguf"),
        "empathy": ("TheBloke/dolphin-2.9-mixtral-8x7b-GGUF", "dolphin-2.9-mixtral-8x7b.Q4_K_M.gguf"),
        "code": ("deepseek-ai/deepseek-coder-6.7b-base-GGUF", "deepseek-coder.Q4_K_M.gguf"),
        "multimodal": ("TheBloke/Command-R-Plus-GGUF", "command-r-plus.Q4_K_M.gguf"),
        "lite": ("TheBloke/Mistral-7B-Instruct-v0.2-GGUF", "mistral-7b-instruct-v0.2.Q4_K_M.gguf")
    },
    "sd": {
        "realistic": ("SG161222/Realistic_Vision_V6.0", "realisticVisionV60B1_v20.safetensors"),
        "dream": ("Lykon/DreamShaper", "dreamshaper_8.safetensors"),
        "juggernaut": ("XpucT/Juggernaut-XL-v8", "juggernautXL_v8.safetensors"),
        "flux": ("ItsJayQz/Flux1-Dev", "flux1-dev.safetensors"),
        "sd3": ("stabilityai/stable-diffusion-3-medium", "sd3_medium.ckpt")
    }
}

for category, entries in models.items():
    for subfolder, (repo, filename) in entries.items():
        dest_path = TARGET_DIR / category / subfolder
        dest_path.mkdir(parents=True, exist_ok=True)
        print(f"📥 Downloading {filename} into {dest_path}")
        subprocess.run([
            "huggingface-cli", "download", repo,
            "--include", filename,
            "--local-dir", str(dest_path)
        ])
