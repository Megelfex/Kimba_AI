import importlib
import os

# Speicherort aller Personas
PERSONA_DIR = "src/kimba_ai/core/personas"

# Standard-Konfiguration
DEFAULT_PERSONA = "persona_augusta"

# Persona-Auswahl
PERSONA_MAP = {
    "Augusta": "persona_augusta",
    "Bella": "persona_bella",
    "Carlotta": "persona_carlotta",
    "Frieren": "persona_frieren",
    "Iuno (API)": "persona_iuno_api",
    "Iuno (Local)": "persona_iuno_local",
    "Kimba (Cat)": "persona_kimba_cat",
    "Lucy": "persona_lucy",
    "Luna": "persona_luna",
    "Mikasa": "persona_mikasa",
    "Milly": "persona_milly",
    "Nami": "persona_nami",
    "Phrolova": "persona_phrolova",
    "Shorekeeper": "persona_shorekeeper"
}

CAT_PERSONA = "persona_kimba_cat"

class PersonaManager:
    def __init__(self):
        self.personas = {}
        self.active_persona_name = None
        self.active_persona = None
        self.cat_persona = None

        self.load_persona(DEFAULT_PERSONA)

    def load_persona(self, persona_module_name: str):
        """Lädt eine Persona und speichert sie im Dictionary."""
        if self.active_persona_name == persona_module_name:
            #print(f"[PersonaManager] ⚠️ Persona '{persona_module_name}' ist bereits aktiv.")
            return

        try:
            module_path = f"src.kimba_ai.core.personas.{persona_module_name}"
            module = importlib.import_module(module_path)
            persona_prompt = module.generate_persona_prompt()
            self.personas[persona_module_name] = persona_prompt
            self.active_persona_name = persona_module_name
            self.active_persona = persona_prompt
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
        return self.active_persona

    def get_cat_prompt(self):
        return self.cat_persona

    def get_persona_prompt(self, name: str):
        return self.personas.get(name)

    def get_persona_names(self):
        return list(PERSONA_MAP.keys())

    def set_active_persona(self, name):
        if name not in PERSONA_MAP:
            raise ValueError(f"Persona '{name}' nicht gefunden.")
        self.load_persona(PERSONA_MAP[name])
