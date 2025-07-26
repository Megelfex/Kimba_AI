import sys
import os 
import gradio as gr

def launch_gui(llm, memory):
    """
    EN: Launches the Kimba Chat GUI using Gradio.
    It connects the LLM response system with memory logging and offers a simple user interface.

    DE: Startet die Kimba-Chat-Oberfläche über Gradio.
    Verknüpft das LLM-Antwortsystem mit Memory-Logging und bietet eine einfache Benutzeroberfläche.

    Args:
        llm (object): An instance of KimbaLLM or similar LLM interface.
        memory (object): An instance of KimbaMemory or similar memory interface.
        identity (dict): Dictionary representing Kimba's identity (not yet used directly here).
    """

    def chat(user_input, history=None):
        """
        EN: Handles a single chat interaction.
        Passes input to LLM, stores both user prompt and response in memory.

        DE: Verarbeitet eine einzelne Chat-Interaktion.
        Übergibt Eingabe an das LLM, speichert Nutzerfrage und Antwort im Gedächtnis.

        Args:
            user_input (str): Text entered by the user.
            history (list, optional): Not used currently.

        Returns:
            str: LLM response
        """
        response = llm.ask(user_input)
        memory.remember({"user": user_input, "kimba": response})
        return response

    # 🎨 Launch Gradio Chat UI
    gr.ChatInterface(chat, title="🤖 Kimba – Dein digitaler Soulmate").launch()
