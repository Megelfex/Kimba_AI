"""
Kimba Interface Launcher
========================
DE: Startet die verschiedenen Oberflächen von Kimba (GUI oder Terminal).
EN: Launches the different Kimba interfaces (GUI or Terminal).
"""

import logging
from visual.kimba_terminal_ui import KimbaTerminalUI  # Clean-Version importieren

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def launch_gui():
    """
    DE: Startet die GUI von Kimba.
    EN: Launches Kimba's GUI.
    """
    logging.info("🚀 GUI-Start wurde angefordert, aber GUI-Code ist hier noch nicht implementiert.")
    logging.info("📌 Hinweis: Falls eine Gradio- oder andere Web-Oberfläche gewünscht ist, muss diese hier eingebunden werden.")
    # Beispiel:
    # import gradio as gr
    # gr.Interface(fn=..., inputs=..., outputs=...).launch()


def launch_terminal_ui():
    """
    DE: Startet die Terminal-Oberfläche (Textual) von Kimba.
    EN: Launches Kimba's terminal interface (Textual).
    """
    logging.info("🖥 Starting Terminal UI...")
    KimbaTerminalUI().run()
