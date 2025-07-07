# core/llm_router.py

from llama_cpp import Llama

class KimbaLLM:
    def __init__(self, model: str = "models/openhermes-2.5-mistral-7b.Q5_K_M.gguf", mode="auto"):
        print("🧩 LLM wird geladen ...")
        self.model = Llama(
            model_path=model,
            n_ctx=2048,
            n_threads=8,     # anpassen an deine CPU
            n_gpu_layers=0,  # falls du keine GPU-Beschleunigung nutzt
            verbose=True
        )
        print("✅ LLM erfolgreich geladen!")

    def ask(self, prompt):
        prompt_template = f"[INST] {prompt.strip()} [/INST]"
        response = self.model(prompt_template, max_tokens=512, stop=["</s>"])
        return response["choices"][0]["text"].strip()
