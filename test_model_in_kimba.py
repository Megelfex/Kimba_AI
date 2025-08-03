from transformers import AutoModelForCausalLM, AutoTokenizer
import os

model_id = "Qwen/Qwen2.5-3B-Instruct"
save_dir = "./models/Qwen2.5-3B-Instruct-FP16"

print(f"[INFO] 📥 Lade Modell {model_id} (FP16) und speichere nach {save_dir}...")
os.makedirs(save_dir, exist_ok=True)

# Tokenizer laden & speichern
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
tokenizer.save_pretrained(save_dir)

# Modell (FP16) laden & speichern
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",       # FP16 oder BF16, je nach GPU
    device_map="auto",        # nutzt automatisch deine RX 6700 XT
    trust_remote_code=True
)
model.save_pretrained(save_dir)

print("[INFO] ✅ Download abgeschlossen – Modell liegt jetzt lokal vor!")
