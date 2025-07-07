
import gradio as gr

def launch_gui(llm, memory, identity):
    def chat(user_input, history=None):
        response = llm.ask(user_input)
        memory.remember({"user": user_input, "kimba": response})
        return response

    gr.ChatInterface(chat, title="🤖 Kimba – Dein digitaler Soulmate").launch()
