import time
import random
from datetime import datetime

# Simulated data to make our logs look realistic
ips = ["192.168.1.50", "10.0.0.15", "192.168.1.102", "172.16.5.4"]
users = ["alice", "bob", "charlie", "dev_user"]
events = ["LOGIN_SUCCESS", "LOGIN_FAILED", "FILE_ACCESSED", "PASSWORD_CHANGED"]

print("🚀 Fake Log Generator is running... Press Ctrl+C to stop.")

# This opens a file called 'security.log'. If it doesn't exist, Python creates it.
with open("security.log", "a") as log_file:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. Generate normal everyday traffic
        ip = random.choice(ips)
        user = random.choice(users)
        event = random.choice(events)
        
        # 2. Inject a simulated "hacker attack" (Brute Force) 20% of the time
        if random.random() < 0.2:
            ip = "185.220.101.5"  # A suspicious external IP address
            user = "root"         # Hackers love targeting the 'root' administrator account
            event = "LOGIN_FAILED"
        
        # Format the log line perfectly
        log_line = f"[{timestamp}] IP={ip} USER={user} EVENT={event}\n"
        
        # Write it to our log file and save it instantly
        log_file.write(log_line)
        log_file.flush() 
        
        # Also print it out to the screen so we can watch it happen live
        print(f"Generated: {log_line.strip()}")
        
        # Wait between 1 to 3 seconds before generating the next log event
        time.sleep(random.uniform(1, 3))

