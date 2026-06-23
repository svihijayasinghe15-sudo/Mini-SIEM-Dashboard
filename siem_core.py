import time
import os
import json
from datetime import datetime

# Using explicit, absolute paths so Python can find files across different folders
SIEM_LOG = os.path.expanduser("~/MiniSIEM/security.log")
HONEYPOT_LOG = os.path.expanduser("~/MiniHoneypot/honeypot_activity.log")
ALERT_FILE = os.path.expanduser("~/MiniSIEM/alerts.json")

# Core state engine tracking failed logins
failed_attempts = {}

print("🧠 Upgraded SIEM Engine Active... Monitoring Server Logs AND Honeypot Traps...")

# Ensure files exist before reading so the script doesn't crash
for path in [SIEM_LOG, HONEYPOT_LOG]:
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("")

if not os.path.exists(ALERT_FILE):
    with open(ALERT_FILE, "w") as f:
        json.dump([], f)


def trigger_alert(ip, user, severity, message):
    """Structures and commits triggered alerts to our central alerts.json file."""
    alert_event = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_ip": ip,
        "target_user": user,
        "severity": severity,
        "message": message
    }
    
    try:
        with open(ALERT_FILE, "r") as f:
            alerts = json.load(f)
    except:
        alerts = []
        
    alerts.append(alert_event)
    
    with open(ALERT_FILE, "w") as f:
        json.dump(alerts, f, indent=4)
        
    print(f"🚨 [{severity}] {message} | IP: {ip}")


# Open both log files cleanly
file_siem = open(SIEM_LOG, "r")
file_honey = open(HONEYPOT_LOG, "r")

# Fast-forward to the end of existing logs so we only process new events
file_siem.seek(0, os.SEEK_END)
file_honey.seek(0, os.SEEK_END)

while True:
    # Check for activity in general server logs
    line_siem = file_siem.readline()
    if line_siem:
        if "EVENT=" in line_siem:
            try:
                parts = line_siem.strip().split(" ")
                ip = parts[2].split("=")[1]
                user = parts[3].split("=")[1]
                event = parts[4].split("=")[1]
                
                if event == "LOGIN_FAILED":
                    failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
                    if failed_attempts[ip] == 5:
                        trigger_alert(ip, user, "WARNING", f"Brute Force Threshold Breached ({failed_attempts[ip]} failures)")
                elif event == "LOGIN_SUCCESS":
                    if ip in failed_attempts:
                        failed_attempts[ip] = 0
            except:
                continue

    # Check for activity in the Honeypot Log
    line_honey = file_honey.readline()
    if line_honey:
        if "ATTACKER_IP=" in line_honey:
            try:
                # Example: [2026-06-23 16:00:00] TARGET_PORT=2222 ATTACKER_IP=127.0.0.1 RECEIVED_DATA='nc'
                parts = line_honey.strip().split(" ")
                ip = parts[2].split("=")[1]
                
                # Extract whatever data the attacker sent to our fake SSH banner
                data_sent = line_honey.split("RECEIVED_DATA=")[1].strip("'")
                
                # Rule: ANY touch on a honeypot is an instant CRITICAL incident
                trigger_alert(
                    ip=ip, 
                    user="root (Simulated SSH)", 
                    severity="CRITICAL", 
                    message=f"HONEYPOT TRAP TRIGGERED! Attacker payload: {data_sent}"
                )
            except:
                continue

    # If neither log file had any new data, sleep briefly to save CPU power
    if not line_siem and not line_honey:
        time.sleep(0.1)


