from transformers import AutoModelForCausalLM, AutoTokenizer
import os

# Modell-ID von HuggingFace
model_id = "microsoft/Phi-3-mini-4k-instruct"
# Speicherort lokal
save_dir = "./models/Phi-3-mini-4k-instruct"

print(f"[INFO] 📥 Lade Modell {model_id} und speichere nach {save_dir}...")
os.makedirs(save_dir, exist_ok=True)

# Tokenizer laden & speichern
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
tokenizer.save_pretrained(save_dir)

# Modell laden & speichern (automatische FP16/BF16 je nach GPU)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True
)
model.save_pretrained(save_dir)

print("[INFO] ✅ Download abgeschlossen – Modell liegt jetzt lokal vor!")
