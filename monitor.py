import os
import time
import socket
import requests
import subprocess
from datetime import datetime

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
TARGET_HOSTS = os.getenv("TARGET_HOSTS", "8.8.8.8,1.1.1.1").split(",")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

service_states = {}

def send_alert(title, message, color_status):
    if not WEBHOOK_URL:
        print(f"[{datetime.now()}] [ALERT] {title}: {message}")
        return

    payload = {
        "embeds": [{
            "title": f"Infrastructure Alert: {title}",
            "description": message,
            "color": 15158332 if color_status == "down" else 3066993,
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send webhook notification: {e}")

def check_ping(host):
    param = "-n" if os.name == "nt" else "-c"
    command = ["ping", param, "1", host.strip()]
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False

def run_monitor():
    print(f"[*] Starting Infrastructure Monitoring Daemon...")
    print(f"[*] Monitoring targets: {TARGET_HOSTS}")
    print(f"[*] Check interval: {CHECK_INTERVAL} seconds\n")

    while True:
        for host in TARGET_HOSTS:
            host = host.strip()
            if not host:
                continue

            is_up = check_ping(host)
            current_state = service_states.get(host, True)

            if not is_up and current_state:
                service_states[host] = False
                msg = f"Target **{host}** is currently unreachable via ICMP ping."
                print(f"[-] DOWN: {host}")
                send_alert(f"HOST DOWN: {host}", msg, "down")

            elif is_up and not current_state:
                service_states[host] = True
                msg = f"Target **{host}** has recovered and is responding normally."
                print(f"[+] RECOVERED: {host}")
                send_alert(f"HOST RECOVERED: {host}", msg, "up")

            else:
                print(f"[ok] {host} is healthy.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_monitor()
