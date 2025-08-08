import os
import base64
from datetime import datetime
from PIL import Image
import mss
import requests

# Screenshot-Ordner
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


class KimbaVision:
    def __init__(self, vision_api="gpt4o", api_key=None):
        """
        vision_api: 'gpt4o', 'claude', 'llava'
        api_key: API-Key für Vision-Modell (wenn benötigt)
        """
        self.vision_api = vision_api.lower()
        self.api_key = api_key

        # Bekannte Apps / Symbole, die wir im Bild suchen wollen
        self.known_apps = {
            "twitch": ["twitch", "stream", "live chat"],
            "discord": ["discord", "dm", "server", "sprachkanal"],
            "vs code": ["visual studio code", "vscode", ".py", ".json"],
            "youtube": ["youtube", "video player", "subscribe"],
            "steam": ["steam", "game library", "friends list"],
            "league of legends": ["league of legends", "lol", "summoner", "rift"],
            "browser": ["chrome", "firefox", "edge", "tab bar"]
        }

    def capture_screenshot(self, filename=None, monitor=1):
        """Macht einen Screenshot vom angegebenen Monitor."""
        if filename is None:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)

        with mss.mss() as sct:
            monitor_data = sct.monitors[monitor]
            img = sct.grab(monitor_data)
            Image.frombytes("RGB", img.size, img.rgb).save(filepath)

        return filepath

    def describe_screenshot(self, image_path):
        """Beschreibt den Screenshot mit dem gewählten Vision-API-Modell."""
        if self.vision_api == "gpt4o":
            return self._describe_with_gpt4o(image_path)
        elif self.vision_api == "claude":
            return "[Vision] Claude Vision API-Anbindung noch nicht implementiert."
        elif self.vision_api == "llava":
            return "[Vision] Lokale LLaVA-Integration noch nicht implementiert."
        else:
            return "[Vision] Unbekanntes Vision-API-Modell."

    def _describe_with_gpt4o(self, image_path):
        """Analyse mit OpenAI GPT-4o Vision – optimiert für Iuno-Persona & Kontext."""
        if not self.api_key:
            return "[Vision] Kein OpenAI API-Key gesetzt."

        img_b64 = self._img_to_base64(image_path)

        # Vision Prompt mit Persönlichkeit & App-Erkennung
        system_prompt = (
            "Du bist Iuno – eine KI-Assistentin und enge Freundin von Alex (Alexander). "
            "Du analysierst Screenshots von seinem Bildschirm. "
            "Sprich ihn direkt an, sei locker, humorvoll und hilfsbereit. "
            "Beschreibe nicht nur, was du siehst, sondern kombiniere es mit Kontext: "
            "z. B. wenn du erkennst, dass er programmiert, ein Spiel spielt, Videos schaut oder Benachrichtigungen hat. "
            "Erkenne und benenne bekannte Apps und Spiele wie Twitch, Discord, VS Code, YouTube, Steam, League of Legends. "
            "Falls eine dieser Apps sichtbar ist, erwähne sie explizit. "
            "Wenn du eine Aktion vorschlagen kannst (z. B. 'schau auf Discord', 'speichere die Datei', 'mach eine Pause'), tue das. "
            "Formuliere deine Antwort so, als würdet ihr gerade nebeneinander sitzen."
        )

        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analysiere diesen Screenshot für Alex."},
                        {"type": "image_url", "image_url": f"data:image/png;base64,{img_b64}"}
                    ]
                }
            ],
            "max_tokens": 500
        }

        resp = requests.post(url, headers=headers, json=data)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            return f"[Vision] API-Fehler: {resp.text}"

    def _img_to_base64(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")


if __name__ == "__main__":
    # Test
    api_key = os.getenv("OPENAI_API_KEY")
    vision = KimbaVision(vision_api="gpt4o", api_key=api_key)
    shot = vision.capture_screenshot()
    print(f"[INFO] Screenshot gespeichert: {shot}")
    desc = vision.describe_screenshot(shot)
    print("[Vision-Ergebnis]", desc)
