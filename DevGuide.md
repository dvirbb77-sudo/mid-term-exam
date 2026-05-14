```markdown
# Developer & Operations Guide

## System Architecture
Traffic Flow: 
Public (Port 80) -> Nginx (Reverse Proxy) -> Docker (Loopback:5000) -> Flask (App)

## Development Setup
This project uses **Poetry** for dependency management. To set up a local environment:

```bash
poetry install
poetry shell
API_KEY=test python app.py