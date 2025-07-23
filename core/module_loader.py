import os
import importlib.util

def load_modules_from_folder(folder="modules"):
    """
    📦 Dynamically loads all Python modules from the given folder.

    Args:
        folder (str): Path to the module directory.

    Returns:
        dict: Mapping of module name → module object
    """
    modules = {}
    for file in os.listdir(folder):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]
            path = os.path.join(folder, file)
            spec = importlib.util.spec_from_file_location(module_name, path)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
                modules[module_name] = mod
                print(f"✅ Modul geladen: {module_name}")
            except Exception as e:
                print(f"❌ Fehler beim Laden von {module_name}: {e}")
    return modules

# ▶️ Testlauf
if __name__ == "__main__":
    mods = load_modules_from_folder("modules")
    print(f"📊 Insgesamt geladen: {len(mods)} Module")
