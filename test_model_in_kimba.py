from transformers import AutoModelForCausalLM, AutoTokenizer
import os

model_id = "mistralai/Mistral-7B-Instruct-v0.2"
save_dir = "./models/Mistral-7B-Instruct"

print(f"[INFO] 📥 Lade Modell {model_id} von Hugging Face und speichere nach {save_dir}...")
os.makedirs(save_dir, exist_ok=True)

tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.save_pretrained(save_dir)

model = AutoModelForCausalLM.from_pretrained(model_id)
model.save_pretrained(save_dir)

print("[INFO] ✅ Download abgeschlossen. Modell liegt jetzt lokal vor!")
