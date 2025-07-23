"""
📋 review_center.py
EN: Lets user review and manage pending GPT-generated modules via the proposal_manifest.yaml.
DE: Ermöglicht das Review & Management von Vorschlägen via proposal_manifest.yaml.
"""

import yaml
import os

MANIFEST = "proposals/proposal_manifest.yaml"

def load_manifest():
    with open(MANIFEST, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_manifest(entries):
    with open(MANIFEST, "w", encoding="utf-8") as f:
        yaml.dump(entries, f, allow_unicode=True)

def review_proposals():
    proposals = load_manifest()
    for entry in proposals:
        if entry["status"] == "pending":
            print("\n📄 Vorschlag:", entry["title"])
            print("📝 Beschreibung:", entry["description"])
            print("📁 Modul:", entry["file"])

            try:
                with open(entry["file"], "r", encoding="utf-8") as f:
                    code = f.read()
                print("\n🧠 Code-Vorschau:\n" + "\n".join(code.splitlines()[:15]) + "\n...")
            except:
                print("⚠️ Modul konnte nicht gelesen werden.")

            choice = input("Akzeptieren [a] / Ablehnen [r] / Überspringen [Enter]: ").strip().lower()
            if choice == "a":
                entry["status"] = "accepted"
            elif choice == "r":
                entry["status"] = "rejected"

    save_manifest(proposals)
    print("\n✅ Manifest aktualisiert.")

if __name__ == "__main__":
    review_proposals()
