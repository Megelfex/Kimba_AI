import os
import sys
import threading
import time

import gradio as gr

# Optional: Importiere Kimba-Komponenten (z. B. LLM-Router oder Task-Engine)
from core.llm_router import KimbaLLM

# Initialisiere Kimba-Modell (Pfad anpassen!)
kimba = KimbaLLM(model="models/openhermes-2.5-mistral-7b.Q5_K_M.gguf")

def kimba_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("===========================")
    print("     KIMBA TERMINAL UI     ")
    print("===========================")
    print("Type 'exit' to quit | Type 'gradio' to launch Gradio backup\n")

    while True:
        prompt = input("You: ")
        if prompt.lower() in ["exit", "quit"]:
            print("Bye!")
            break
        elif prompt.lower() == "gradio":
            print("\n[INFO] Launching Gradio backup UI ...")
            threading.Thread(target=start_gradio_ui, daemon=True).start()
            continue

        try:
            print("Kimba is thinking ...\n")
            response = kimba.ask(prompt)
            print(f"Kimba: {response}\n")
        except Exception as e:
            print(f"[ERROR] {str(e)}\n")

def start_gradio_ui():
    def chat_fn(user_input):
        return kimba.ask(user_input)

    gr.Interface(fn=chat_fn, inputs="text", outputs="text", title="Kimba Backup UI").launch()


if __name__ == "__main__":
    kimba_terminal()
