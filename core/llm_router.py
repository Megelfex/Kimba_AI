from llama_cpp import Llama
import os

class KimbaLLMRouter:
    def __init__(self):
        self.model_paths = {
            "default": "models/openhermes-2.5-mistral-7b.Q5_K_M.gguf",
            "creative": "models/mythomax-l2-13b.Q5_K_M.gguf",
            "core": "models/llama3.1-8b-instruct.Q5_K_M.gguf",
            "code": "models/deepseek-coder.Q5_K_M.gguf",
            "empathy": "models/dolphin-2.9-mixtral-8x7b.Q5_K_M.gguf"
        }

        self.models = {}  # lazy cache

    def load_model(self, purpose: str):
        path = self.model_paths.get(purpose, self.model_paths["default"])
        if not os.path.exists(path):
            raise FileNotFoundError(f"Modellpfad existiert nicht: {path}")

        if path not in self.models:
            print(f"🧠 Lade Modell für '{purpose}' ...")
            self.models[path] = Llama(
                model_path=path,
                n_ctx=2048,
                n_threads=8,
                n_gpu_layers=0,
                verbose=True
            )
        return self.models[path]

    def ask(self, prompt: str, purpose: str = "default"):
        model = self.load_model(purpose)
        prompt_template = f"[INST] {prompt.strip()} [/INST]"
        response = model(prompt_template, max_tokens=512, stop=["</s>"])
        return response["choices"][0]["text"].strip()
