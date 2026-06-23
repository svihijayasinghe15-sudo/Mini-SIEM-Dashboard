import socket
import sys
from datetime import datetime

# We will run this on port 2222. (Real SSH runs on port 22, but port 2222 is safer for testing)
HOST = "0.0.0.0"  # This tells it to listen to any network connection coming in
PORT = 2222
LOG_FILE = "honeypot_activity.log"

print(f"🕸️ Honeypot active! Simulating fake SSH server on port {PORT}...")

# 1. Create a network socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    # 2. Bind the socket to our port and start listening
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
except Exception as e:
    print(f"❌ Failed to bind to port {PORT}. Error: {e}")
    sys.exit()

# 3. Keep the trap open forever
while True:
    try:
        # Wait for a connection (this pauses the script until someone connects)
        client_socket, client_address = server_socket.accept()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attacker_ip = client_address[0]
        
        print(f"🚨 [WARNING] Connection attempt detected from IP: {attacker_ip} at {timestamp}")
        
        # 4. Pretend to be a real Ubuntu SSH server by sending a classic banner
        # This tricks the attacker/scanner into thinking they found a real target
        ssh_banner = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n"
        client_socket.send(ssh_banner.encode())
        
        # 5. Wait a brief second to see if they try to send data (like a password)
        client_socket.settimeout(2.0)
        try:
            data = client_socket.recv(1024).decode().strip()
        except socket.timeout:
            data = "None (Port Scan Only)"
            
        # 6. Log the attack into a file
        log_entry = f"[{timestamp}] TARGET_PORT={PORT} ATTACKER_IP={attacker_ip} RECEIVED_DATA='{data}'\n"
        
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
            
        # Close the connection with the attacker
        client_socket.close()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down the honeypot safely. Goodbye!")
        server_socket.close()
        sys.exit()
    except Exception as e:
        # Catch unexpected errors gracefully so the honeypot doesn't crash
        continue


