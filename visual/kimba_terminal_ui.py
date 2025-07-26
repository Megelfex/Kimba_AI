import threading

def launch_terminal_ui(chat_callback):
    print("🖥️  Kimba Terminal gestartet. Tippe 'exit' zum Beenden.\n")

    def terminal_loop():
        while True:
            try:
                user_input = input("Kimba > ")
                if user_input.lower() in ["exit", "quit"]:
                    print("👋 Kimba Terminal wird beendet.")
                    break
                response = chat_callback(user_input)
                print(f"Kimba: {response}\n")
            except KeyboardInterrupt:
                print("\n⛔ Abbruch durch Benutzer.")
                break
            except Exception as e:
                print(f"[Fehler] {e}")

    # In einem eigenen Thread starten, um mit Gradio parallel zu laufen
    terminal_thread = threading.Thread(target=terminal_loop, daemon=True)
    terminal_thread.start()
