import platform
import psutil
import socket
import datetime
import json
import os

# Speicherort für Systemstatus-JSON-Datei
# Location for persisted system identity data
SYSTEM_STATUS_PATH = "memory/system_status.json"

def get_system_identity():
    """
    EN: Collects and returns system identity and environment information. Also writes a JSON file for reference.
    DE: Sammelt und gibt Systemidentität und Umgebungsinformationen zurück. Speichert zusätzlich eine JSON-Datei zur Referenz.

    Returns:
        dict: A dictionary containing system information including OS, CPU, RAM, uptime, etc.
    """
    identity = {
        "os": platform.system(),
        "os_version": platform.version(),
        "hostname": socket.gethostname(),
        "cpu": platform.processor(),
        "architecture": platform.machine(),
        "ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "boot_time": datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat(),
        "last_updated": datetime.datetime.now().isoformat()
    }

    os.makedirs(os.path.dirname(SYSTEM_STATUS_PATH), exist_ok=True)
    with open(SYSTEM_STATUS_PATH, "w", encoding="utf-8") as f:
        json.dump(identity, f, indent=2, ensure_ascii=False)

    return identity

# 🔧 Manual test call when run as standalone script
# 🔍 Manueller Test beim direkten Ausführen des Skripts
if __name__ == "__main__":
    data = get_system_identity()
    for key, value in data.items():
        print(f"{key}: {value}")
