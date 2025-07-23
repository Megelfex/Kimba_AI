"""
🤖 auto_merge_module.py
EN: Scans the proposal manifest for accepted modules, validates them,
and automatically moves them into the active 'modules/' directory.

DE: Scannt das Vorschlags-Manifest nach akzeptierten Modulen, validiert sie
und verschiebt sie automatisch in das aktive 'modules/'-Verzeichnis.
"""

import os
import shutil
import yaml
from auto_tester import test_module
from datetime import datetime

MANIFEST = "proposals/proposal_manifest.yaml"
MODULE_DIR = "modules"
GENERATED_DIR = "proposals/generated_modules"
MERGE_LOG = "proposals/merge_log.txt"

def load_manifest():
    with open(MANIFEST, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_manifest(entries):
    with open(MANIFEST, "w", encoding="utf-8") as f:
        yaml.dump(entries, f, allow_unicode=True)

def merge_accepted_modules():
    """
    EN: Processes all accepted modules and moves them to the module directory if valid.
    DE: Verarbeitet alle akzeptierten Module und verschiebt sie bei Validierung in das aktive Verzeichnis.
    """
    manifest = load_manifest()
    changed = False

    for entry in manifest:
        if entry["status"] == "accepted" and not entry.get("merged", False):
            src = entry["file"]
            filename = os.path.basename(src)
            dest = os.path.join(MODULE_DIR, filename)

            # ✅ Sicherheitstest
            result = test_module(src)
            if result.get("syntax_ok", False) and result.get("has_docstrings", False):
                try:
                    shutil.copy2(src, dest)
                    entry["merged"] = True
                    changed = True
                    log_merge(entry, status="success")
                    print(f"✅ Modul aktiviert: {filename}")
                except Exception as e:
                    log_merge(entry, status="error", error=str(e))
                    print(f"❌ Fehler beim Verschieben: {e}")
            else:
                log_merge(entry, status="failed_test")
                print(f"⚠️ Modul nicht bestanden: {filename}")
    
    if changed:
        save_manifest(manifest)

def log_merge(entry, status="success", error=None):
    """
    Logs merge result to a simple text file.
    """
    with open(MERGE_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}] {entry['id']} - {status.upper()}")
        if error:
            f.write(f" | Fehler: {error}")

if __name__ == "__main__":
    merge_accepted_modules()
