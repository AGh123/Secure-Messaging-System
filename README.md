# CipherCapsule – Ephemeral-Key Secure Messaging System

CipherCapsule is a secure messaging system where **each message is encrypted with a unique, one-time symmetric key** derived from an **ephemeral Diffie–Hellman (DH) exchange**.  
Messages can be viewed **only once** and are **permanently deleted after being read**, ensuring strong confidentiality and **perfect forward secrecy**.

This project was developed as part of a **cryptography course** and demonstrates the **practical integration of symmetric and asymmetric cryptography** in a real client–server application using **FastAPI** and **Angular**.

---

## ✨ Key Features

### 🔐 Hybrid Cryptography

- Ephemeral Diffie–Hellman key exchange
- AES-256-GCM for message encryption
- RSA-2048 identity keys per user

### 🧨 Self-Destructing Messages

- Messages are deleted immediately after being read
- Refreshing the page does not restore messages

### 🪪 Secure Authentication

- Passwords hashed using **bcrypt**
- Server-side session tokens
- Backend is the single source of truth

### 📥 Inbox-Based UX

- No message IDs exposed to users
- Inbox shows senders with unread message counts
- Click-to-open, read-once behavior

### 🧠 Forward Secrecy

- Each message uses a fresh encryption key
- Compromise of one key does not affect other messages

---

## 🏗️ Project Structure

```

Secure-Messaging-System/
│
├── backend/
│   ├── app/
│   │   ├── crypto/        # Cryptographic primitives (RSA, DH, AES-GCM)
│   │   ├── models/        # Database models
│   │   ├── routes/        # FastAPI routes (auth, messages)
│   │   ├── schemas/       # Request/response schemas
│   │   ├── database.py
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── models/    # Frontend data models
│   │   │   ├── services/  # Angular services
│   │   │   ├── app.ts
│   │   │   ├── app.html
│   │   │   └── app.scss
│   │   ├── index.html
│   │   ├── main.ts
│   │   └── styles.scss
│   └── angular.json
│
└── README.md

```

---

## ⚙️ Requirements

### Backend

- Python **3.10+** (tested with Python 3.12)
- `pip`
- Virtual environment (recommended)

### Frontend

- Node.js **18+**
- `npm`
- Angular CLI

---

## 🚀 How to Run the Project (From Scratch)

These steps assume a **completely clean laptop**.

---

## 1️⃣ Backend Setup (FastAPI)

### Step 1: Navigate to backend directory

```bash
cd backend
```

### Step 2: Create and activate a virtual environment

```bash
python -m venv venv
```

**Activate it:**

- **Windows**

```bash
venv\Scripts\activate
```

- **macOS / Linux**

```bash
source venv/bin/activate
```

You should now see `(venv)` in your terminal.

---

### Step 3: Install backend dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4: Run the backend server

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```
http://127.0.0.1:8000
```

You can verify it by opening:

```
http://127.0.0.1:8000/docs
```

This shows the automatically generated FastAPI documentation.

---

## 2️⃣ Frontend Setup (Angular)

Open a **new terminal window** (leave backend running).

### Step 1: Navigate to frontend directory

```bash
cd frontend
```

---

### Step 2: Install frontend dependencies

```bash
npm install
```

---

### Step 3: Start the Angular development server

```bash
ng serve
```

The frontend will be available at:

```
http://localhost:4200
```

---

## 🧪 How to Use the Application

### Register

- Create a new username and password
- Passwords are hashed using bcrypt

### Login

- Authenticate and start a secure session

### Inbox

- View senders who have sent you messages
- Each sender shows a badge with unread message count

### Send Message

- Select a user
- Type and send a message
- Message is encrypted using a one-time AES key

### Read Message

- Click a sender in the inbox
- Message is decrypted **once**
- Message is immediately deleted from the database

### Refresh Behavior

- Once read, messages are permanently gone
- Refreshing the page does not restore them

---

## 🔐 Security Design Overview

### Cryptographic Workflow

1. Sender generates an ephemeral Diffie–Hellman key pair
2. A one-time shared secret is derived
3. An AES-256-GCM key is derived from the shared secret
4. Message is encrypted and stored temporarily

On message read:

- Message is decrypted
- Ciphertext and encryption keys are deleted

---

### Why This Is Secure

✔ Perfect forward secrecy
✔ No long-term symmetric keys
✔ No plaintext message storage
✔ No message replay
✔ Backend-verified authentication

---

## 🧠 Important Design Decisions

- Sender identity is never trusted from the client
- Backend derives sender identity from session tokens
- Message IDs are never exposed to users
- Only minimal plaintext metadata is stored
- Backend is the authoritative source of authentication

These decisions mirror real secure messaging system designs.

---

## 🛠️ Development Notes

- Database: SQLite (created automatically on backend startup)
- CORS enabled for local development
- Designed for educational and demonstration purposes
- Not intended for production use without further hardening

---

## 🧑‍🎓 Academic Context

This project demonstrates:

- Symmetric cryptography (AES-256-GCM)
- Asymmetric cryptography (RSA-2048, Diffie–Hellman)
- Hybrid encryption design
- Secure session management
- Practical cryptographic system implementation
