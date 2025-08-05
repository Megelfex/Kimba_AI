import importlib
import os

# Speicherort aller Personas
PERSONA_DIR = "core/personas"

# Standard-Konfiguration
DEFAULT_PERSONA = "persona_iuno_local"   # Start-Persona
CAT_PERSONA = "persona_kimba_cat"        # Immer geladen für Overlay-Katze

class PersonaManager:
    def __init__(self):
        self.active_persona = None
        self.cat_persona = None
        self.load_persona(DEFAULT_PERSONA)
        self.load_cat_persona(CAT_PERSONA)

    def load_persona(self, persona_module_name: str):
        """Lädt die Hauptpersona (z. B. Iuno, Augusta, Mikasa, etc.)."""
        try:
            module_path = f"core.personas.{persona_module_name}"
            module = importlib.import_module(module_path)
            self.active_persona = module.generate_persona_prompt()
            print(f"[PersonaManager] ✅ Hauptpersona geladen: {persona_module_name}")
        except ModuleNotFoundError:
            raise ValueError(f"❌ Persona '{persona_module_name}' nicht gefunden in {PERSONA_DIR}")

    def load_cat_persona(self, persona_module_name: str):
        """Lädt die Katzenpersona separat."""
        try:
            module_path = f"core.personas.{persona_module_name}"
            module = importlib.import_module(module_path)
            self.cat_persona = module.generate_persona_prompt()
            print(f"[PersonaManager] 🐾 Katzenpersona geladen: {persona_module_name}")
        except ModuleNotFoundError:
            raise ValueError(f"❌ Katzenpersona '{persona_module_name}' nicht gefunden in {PERSONA_DIR}")

    def switch_persona(self, new_persona_name: str):
        """Wechselt die aktive Hauptpersona."""
        self.load_persona(new_persona_name)
        return f"🔄 Persona gewechselt zu {new_persona_name}"

    def get_active_prompt(self):
        """Gibt den Prompt der aktuellen Hauptpersona zurück."""
        return self.active_persona

    def get_cat_prompt(self):
        """Gibt den Prompt der Katzenpersona zurück."""
        return self.cat_persona
