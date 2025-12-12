CipherCapsule – Ephemeral-Key Secure Messaging System

CipherCapsule is a secure messaging system where each message is encrypted using a unique, one-time symmetric key derived from an ephemeral Diffie–Hellman exchange.
Messages can be viewed only once and are permanently deleted after being read, ensuring strong confidentiality and forward secrecy.

This project was developed as a cryptography course project and demonstrates the practical integration of symmetric and asymmetric cryptography in a real application using FastAPI and Angular.

✨ Key Features

🔐 Hybrid Cryptography

Ephemeral Diffie–Hellman key exchange

AES-256-GCM for message encryption

RSA-2048 identity keys per user

🧨 Self-Destructing Messages

Messages are deleted immediately after being read

Refreshing the page does not restore messages

🪪 Secure Authentication

Passwords hashed with bcrypt

Server-side session tokens

Backend is the single source of truth

📥 Inbox-Based UX

No message IDs exposed to users

Inbox shows senders with unread message counts

Click-to-open, read-once behavior

🧠 Forward Secrecy

Each message uses a fresh encryption key

Compromise of one key does not affect others

🏗️ Project Structure
Secure-Messaging-System/
│
├── backend/
│ └── app/
│ ├── crypto/ # Cryptographic primitives (RSA, DH, AES-GCM)
│ ├── models/ # SQLAlchemy models
│ ├── routes/ # FastAPI routes (auth, messages)
│ ├── schemas/ # Pydantic request/response schemas
│ ├── database.py
│ └── main.py
│
├── frontend/
│ ├── src/
│ │ ├── app/
│ │ │ ├── models/ # Frontend data models
│ │ │ ├── services/ # Angular services
│ │ │ ├── app.ts
│ │ │ ├── app.html
│ │ │ └── app.scss
│ │ ├── index.html
│ │ ├── main.ts
│ │ └── styles.scss
│ └── angular.json
│
└── README.md

⚙️ Requirements
Backend

Python 3.10+

pip

virtual environment recommended

Frontend

Node.js 18+

npm

Angular CLI

🚀 How to Run the Project
1️⃣ Backend Setup (FastAPI)
Navigate to backend directory
cd backend

Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate # Linux / macOS
venv\Scripts\activate # Windows

Install backend dependencies
pip install -r requirements.txt

Run the backend server
uvicorn app.main:app --reload

The backend will be available at:

http://127.0.0.1:8000

Test it quickly by opening:

http://127.0.0.1:8000/

Expected response:

{ "status": "CipherCapsule backend running" }

2️⃣ Frontend Setup (Angular)
Navigate to frontend directory
cd frontend

Install frontend dependencies
npm install

Start Angular development server
ng serve

The frontend will be available at:

http://localhost:4200

🧪 How to Use the Application

Register

Create a new username and password

Login

Authenticate and start a secure session

Inbox

See senders who have sent you messages

Each sender shows a badge with the number of unread messages

Send Message

Select a user from the user list

Type a message and send it

Message is encrypted and stored temporarily

Read Message

Click a sender in the inbox

Message is decrypted and displayed once

Message is immediately deleted from the database

Refresh Behavior

Once read, messages are gone permanently

Refreshing the page does not restore them

🔐 Security Design Overview
Cryptographic Workflow

Sender generates an ephemeral Diffie–Hellman key pair

A one-time shared secret is derived

An AES-256-GCM key is derived from the shared secret

The message is encrypted and stored temporarily

On read:

The message is decrypted

The ciphertext and encryption key are deleted

Why This Is Secure

✔ Forward secrecy

✔ No long-term symmetric keys

✔ No message replay

✔ No plaintext message storage

✔ Backend-verified authentication

🧠 Important Design Decisions

Sender identity is never trusted from the client

Backend derives sender identity from the session token

Message IDs are never exposed to users

Only minimal plaintext metadata is stored for inbox functionality

Backend is the authoritative source of authentication state

These decisions balance security, correctness, and usability, similar to real secure messaging systems.

🛠️ Development Notes

Database: SQLite (automatically created on backend startup)

CORS enabled for local development

Designed for educational and demonstration purposes

Not intended for production deployment without further hardening

🧑‍🎓 Academic Context

This project demonstrates:

Symmetric cryptography (AES-256-GCM)

Asymmetric cryptography (RSA, Diffie–Hellman)

Hybrid encryption design

Secure session management

Practical cryptographic system implementation
