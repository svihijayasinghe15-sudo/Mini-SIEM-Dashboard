# 🛡️ Enterprise Security Ecosystem: Mini-SIEM & Deception Honeypot

A unified, multi-component defensive security suite engineered to demonstrate real-time log ingestion, threat detection engineering, and proactive network deception mechanisms. 

This project bridges an offensive asset (a low-interaction network trap) directly into a centralized Security Information and Event Management (SIEM) pipeline, mimicking enterprise Security Operations Center (SOC) workflows.

---

## 🏗️ System Architecture & Data Flow

This ecosystem operates via four synchronous pipelines:

1. **Log Simulation (`log_generator.py`):** Continuously broadcasts background server traffic, introducing erratic user login activities and mock noise.
2. **Deception Trap (`honeypot.py`):** Establishes a simulated socket on port `2222` masquerading as a vulnerable OpenSSH server. It logs unauthorized discovery probes, interactions, and threat payloads.
3. **Correlation Engine (`siem_core.py`):** Constantly monitors both standard event files and honeypot interaction feeds. It applies specific behavioral thresholds (e.g., 5 failed log-in attempts) and elevates any honeypot interaction directly to a `CRITICAL` severity metric.
4. **Visual Analytics Console (`app.py`):** A lightweight Flask-driven microservice that surfaces the alert cache via a custom API endpoint. The front-end layout uses asynchronous JavaScript to poll changes and stream active indicators directly to the security screen without page refreshes.

---

## 🛠️ Features & Threat Detection Capabilities
* **Multi-Source Ingestion:** Simultaneously tails generic system logs and dedicated deception environment logs.
* **Stateful Brute Force Tracking:** Maps anomalous authentication counts specifically by source IP.
* **Proactive Network Deception:** Employs a custom banner payload response to intercept unauthorized reconnaissance scans.
* **Dynamic SOC Dashboard:** Dark-mode responsive design offering real-time situational awareness for security operators.

---

## 📸 Live Dashboard Preview
<img width="1680" height="891" alt="Screenshot 2026-06-23 at 16 23 19" src="https://github.com/user-attachments/assets/c46b3311-edc0-4089-a2f8-c19d99b4c369" />

---

## 🔧 Installation, Deployment, & Execution

To test or deploy this ecosystem within a secure virtual environment (e.g., Kali Linux), initiate the following deployment process:

### 1. Environment Replication
Clone this repository to your target machine:
```bash
git clone [https://github.com/svihijayasinghe15-sudo/Mini-SIEM-Dashboard.git](https://github.com/svihijayasinghe15-sudo/Mini-SIEM-Dashboard.git)
cd Mini-SIEM-Dashboard
