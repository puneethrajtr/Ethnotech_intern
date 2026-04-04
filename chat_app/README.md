# 💬 Chat Application

A **Real-Time Chat Application Backend** built using Python that allows users to communicate through private and group messaging. This project demonstrates core backend concepts such as authentication, API development, and real-time communication.

---

## 🚀 Features

* 🔐 User Authentication (JWT-based)
* 👤 User Registration & Login APIs
* 💬 Real-time messaging (private & group chat)
* 🧑‍🤝‍🧑 Group chat functionality
* 📡 RESTful API design
* 🗂 Message storage and retrieval
* ⚡ Scalable backend architecture

Modern chat applications typically include features like messaging, notifications, and real-time communication to enhance user interaction ([PubNub][1]).

---

## 🛠️ Tech Stack

* **Backend:** Python
* **Framework:** (Flask / Django / FastAPI – update based on your project)
* **Authentication:** JWT
* **Database:** (SQLite / PostgreSQL / MongoDB)
* **API Testing:** Postman

---

## 📂 Project Structure

```
chat_app/
│
├── app.py / main.py
├── models/
├── routes/
├── controllers/
├── utils/
├── database/
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/puneethrajtr/Ethnotech_intern.git
cd chat_app
```

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
```

### 3️⃣ Activate environment

```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python app.py
```

Server will start at:

```
http://127.0.0.1:5000/
```

---

## 📌 API Endpoints (Example)

| Method | Endpoint  | Description   |
| ------ | --------- | ------------- |
| POST   | /register | Register user |
| POST   | /login    | Login user    |
| GET    | /messages | Get messages  |
| POST   | /send     | Send message  |

---

## 🎯 Future Improvements

* ✅ WebSocket integration for real-time chat
* ✅ Frontend UI (React / HTML / CSS)
* ✅ Message notifications
* ✅ File sharing support
* ✅ Deployment (AWS / Render / Docker)

---

## 👨‍💻 Author

**Puneeth Raj T R**

---

## 📄 License

This project is open-source and available under the MIT License.

