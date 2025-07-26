import gradio as gr
import asyncio
from core.llm_router import KimbaLLMRouter
from visual.kimba_terminal_ui import launch_terminal_ui

llm = KimbaLLMRouter()

# Diese Funktion ist vollständig kompatibel mit type="messages"
def chat(messages: list):
    last_user_msg = messages[-1]["content"]
    reply = llm.ask(last_user_msg)
    return messages + [{"role": "assistant", "content": reply}]


def launch_gui():
    # Starte Terminal-UI parallel (optional)
    asyncio.get_event_loop().run_in_executor(None, launch_terminal_ui, lambda x: llm.ask(x))

    # Starte Gradio Chat UI
    iface = gr.ChatInterface(
    fn=chat,
    type="messages",  # wichtig!
    title="Kimba vX",
    description="Dein digitaler Soulmate im Terminal & Browser.",
    theme="soft",
)

    iface.launch(share=False)

if __name__ == "__main__":
    launch_gui()
