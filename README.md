# Enterprise Infrastructure Health & Uptime Monitor

A lightweight, containerized Python monitoring daemon designed to provide proactive observability across critical enterprise infrastructure components (domain controllers, firewalls, network switches, and internal services).

## 🚀 Overview
In environments with hundreds of endpoints and critical network infrastructure, unexpected downtime costs time and money. This tool continuously checks node availability via multiple protocols (ICMP, TCP ports, HTTP) and intelligently manages alert states to prevent alert fatigue.

## 🛠️ Core Features
* **Multi-Protocol Probing:** Verifies service availability using ICMP ping, raw TCP port checks (e.g., LDAP/389, DNS/53, HTTPS/443), and HTTP status codes.
* **Stateful Alerting:** Tracks state transitions to prevent spamming notifications—alerts fire immediately on failure and send a recovery message only when the service stabilizes.
* **Webhook Integration:** Sends cleanly formatted, rich notifications to Discord, Slack, or Microsoft Teams channels.
* **Containerized Deployment:** Fully containerized using Docker and Docker Compose for easy deployment on any Linux or Windows host.

## 📂 Repository Structure
```text
├── monitor.py           # Core Python monitoring loop and probing logic
├── Dockerfile           # Container build instructions
├── docker-compose.yml   # Orchestration configuration with environment variables
└── requirements.txt     # Python dependencies

