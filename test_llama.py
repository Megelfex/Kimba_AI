from llama_cpp import Llama

print("[INFO] 🚀 Lade TinyLlama Testmodell...")

try:
    llm = Llama(
        model_path="models/TinyLlama-1.1B-Chat-v1.0.Q5_K_M.gguf",  # Pfad anpassen falls nötig
        n_ctx=512,         # kleiner Kontext → weniger RAM
        n_threads=2,       # minimale CPU-Last
        n_gpu_layers=0     # kein GPU-Offload
    )

    print("[INFO] ✅ Modell erfolgreich geladen. Testeingabe wird gesendet...")
    output = llm("Hello TinyLlama!", max_tokens=20)
    print("[OUTPUT]", output)

except Exception as e:
    print("[ERROR] ❌ Modell konnte nicht geladen werden:", e)
