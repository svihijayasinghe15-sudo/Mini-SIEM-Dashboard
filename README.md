# 🛡️ BlueTeam Mini-SIEM & SOC Dashboard

An end-to-end, lightweight Security Information and Event Management (SIEM) tool built to simulate enterprise log ingestion, threat detection engineering, and real-time incident response monitoring.

## 🚀 Features
* **Live Log Generation:** Simulates realistic network traffic alongside automated brute-force attacks.
* **Analysis & Correlation Engine:** Parses unstructured logs in real-time using regex/string parsing and triggers automated alerts when predefined security thresholds are crossed (e.g., Brute Force: 5 failed logins).
* **Asynchronous Web Dashboard:** A sleek SOC dashboard built with Flask and JavaScript that pools alerts via a custom API and updates dynamically every 3 seconds without page reloads.

## 🛠️ Architecture Flow
1. `log_generator.py` streams raw security events into `security.log`.
2. `siem_core.py` acts as the detection engine, parsing lines and tracking anomalous behaviors.
3. Upon rule violation, alerts are structured into JSON format (`alerts.json`).
4. `app.py` reads the threat telemetry and displays it on a dark-themed UI.

## 📸 Dashboard Preview
<img width="1675" height="903" alt="Screenshot 2026-06-23 at 15 23 37" src="https://github.com/user-attachments/assets/8ac031b9-c43e-49c1-9654-20762e8ac53e" />


## 🔧 Setup & Installation
1. Clone the repo: `git clone https://github.com/YOUR-USERNAME/Mini-SIEM-Dashboard.git`
2. Start the log generator: `python3 log_generator.py`
3. In a separate terminal, start the analysis engine: `python3 siem_core.py`
4. Run the web application: `python3 app.py`
5. Navigate to `http://127.0.0.1:5000` in your local browser.
