# Secure Messaging Application

Secure web-based messaging platform developed as my bachelor's/graduate diploma project at Ivan Franko National University of Lviv (LNU).  
The project focuses on building a methodology-driven secure messaging system with emphasis on server-side security, authentication, data protection, and best practices in secure software development.

## Overview

This application allows authenticated users to register, send messages, and manage accounts in a secure manner. Key goals:
- Implement secure communication workflows (data in transit and at rest)
- Follow web security best practices (OWASP guidelines)
- Document architectural and security design decisions as part of a methodology study

The system uses a containerized setup for easy deployment and testing.

## Key Features & Security Controls

- User registration and authentication with JWT tokens
- Secure messaging (REST API endpoints)
- HTTPS for all communication
- Encrypted database storage (PostgreSQL)
- CSRF protection
- Secure session handling and access control
- Containerized infrastructure with Docker Compose

## Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML + Jinja
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **Security**: JWT authentication, HTTPS, encrypted storage, CSRF mitigation

## Project Structure

secure_messaging_app/
├── app/               # Core application code (backend, routes, models, security logic) \
├── hacker/            # Security testing / attack simulation module (for methodology/validation) \
├── postgres/          # Database configuration, schema, migrations \
├── docker-compose.yml # Orchestrates app + database services \
├── .gitignore \
└── LICENSE            # MIT License \


## Installation & Running

Requires Docker and Docker Compose.

```bash
# Clone the repo
git clone https://github.com/peacedetskiy/secure_messaging_app.git
cd secure_messaging_app
```

## Start the services (app + PostgreSQL)
docker-compose up --build

- The app should become available at http://localhost:some-port (check docker-compose.yml or logs for exact port).
- Database runs in a separate container.
- For development: inspect app/ for entry points (e.g., app.py, main.py, or run.py).

## Usage Notes

- Register/login via the web interface
- Send/receive messages through secure endpoints
- Security features (JWT, encryption, CSRF) are enforced server-side

This is a research/academic prototype — not intended for production use without further hardening.

Completed as part of the B.Sc. in Cybersecurity at Ivan Franko National University of Lviv (2024).
The thesis includes a methodology study on designing secure messaging systems, covering threat modeling, secure architecture, and implementation choices.
Full thesis/documentation available upon request.
