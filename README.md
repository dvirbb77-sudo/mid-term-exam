# Status Dashboard Service

A production-ready internal status monitoring dashboard containerized with Docker and reverse-proxied via Nginx.

## Quick Start
To deploy the service on a clean Ubuntu host, run the following:

```bash
git clone [https://github.com/Ferrum-Axion/Mid-Term-Exam](https://github.com/Ferrum-Axion/Mid-Term-Exam)
cd Mid-Term-Exam
# Run as root, providing the mandatory API_KEY
API_KEY=your_secure_secret sudo -E ./install.sh