import socket

def send_overlay_command(character, command, port=None):
    """
    Sendet einen Animationsbefehl an das Overlay via Socket.

    Args:
        character (str): "iuno" oder "kimba"
        command (str): Name der Animation z. B. "happy", "sad", "idle"
        port (int, optional): Portnummer überschreiben (Standard 5001/5002)
    """
    default_ports = {
        "iuno": 5001,
        "kimba": 5002
    }

    port = port or default_ports.get(character)
    if not port:
        print(f"[Overlay] ⚠️ Ungültiger Charaktername: {character}")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", port))
            s.sendall(command.encode("utf-8"))
        print(f"[Overlay] ✅ Befehl '{command}' an {character} gesendet (Port {port})")
    except Exception as e:
        print(f"[Overlay] ❌ Fehler beim Senden an {character}: {e}")
