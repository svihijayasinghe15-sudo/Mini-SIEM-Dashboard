import time
import os
import json
from datetime import datetime

LOG_FILE = "security.log"
ALERT_FILE = "alerts.json"

# A Python dictionary to keep track of failed attempts.
# It will look like: {"185.220.101.5": 3}
failed_attempts = {}

print("🧠 SIEM Analysis Engine is running... Scanning for threats...")

# Setup our alerts file as a clean list if it doesn't exist yet
if not os.path.exists(ALERT_FILE):
    with open(ALERT_FILE, "w") as f:
        json.dump([], f)

def trigger_alert(ip, user, count):
    """This function runs whenever a security rule is broken."""
    alert_event = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_ip": ip,
        "target_user": user,
        "severity": "CRITICAL",
        "message": f"Brute Force Attack Detected! {count} failed logins."
    }
    
    # Read any existing alerts so we don't overwrite them
    try:
        with open(ALERT_FILE, "r") as f:
            alerts = json.load(f)
    except:
        alerts = []
        
    # Add our new alert to the list
    alerts.append(alert_event)
    
    # Save the updated list back to alerts.json (our mini-database)
    with open(ALERT_FILE, "w") as f:
        json.dump(alerts, f, indent=4)
    
    print(f"🚨 [ALERT] {alert_event['message']} targeting user '{user}' from IP {ip}")


# Open the log file to read it line-by-line
with open(LOG_FILE, "r") as f:
    while True:
        line = f.readline()
        
        # If the log generator hasn't written a new line yet, wait a moment
        if not line:
            time.sleep(0.1)
            continue
            
        # Parse the data out of the log line
        # Example line: [2026-06-23 15:00:00] IP=185.220.101.5 USER=root EVENT=LOGIN_FAILED
        if "EVENT=" in line:
            try:
                parts = line.strip().split(" ")
                # Extract the values by splitting on the '=' sign
                ip = parts[2].split("=")[1]
                user = parts[3].split("=")[1]
                event = parts[4].split("=")[1]
                
                # --- RULE CORE ---
                if event == "LOGIN_FAILED":
                    # Increase the count of failures for this specific IP
                    failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
                    
                    # If they hit exactly 5 failures, trigger the alert!
                    if failed_attempts[ip] == 5:
                        trigger_alert(ip, user, failed_attempts[ip])
                        
                elif event == "LOGIN_SUCCESS":
                    # If they successfully log in, reset their counter
                    if ip in failed_attempts:
                        failed_attempts[ip] = 0
                        
            except Exception as e:
                # If a line is messy or broken, ignore it and keep going
                continue


