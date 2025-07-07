import platform
import psutil
import socket
import datetime
import json
import os

SYSTEM_STATUS_PATH = "memory/system_status.json"

def get_system_identity():
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

# Testfunktion
if __name__ == "__main__":
    data = get_system_identity()
    for key, value in data.items():
        print(f"{key}: {value}")
