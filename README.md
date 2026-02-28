# 🚀 myChatGpt – Full-Stack Streaming ChatGPT Clone with Persistent Memory

myChatGpt is a production-ready full-stack AI chat application built using **FastAPI**, **React**, **SQLite**, and **OpenAI API**. A full-stack AI chat platform with real-time LLM streaming, persistent conversation memory, dynamic session management, and production-ready API architecture using FastAPI, React, SQLAlchemy, and OpenAI APIs.

It supports:

- ⚡ Real-time streaming LLM responses
- 💾 Persistent multi-session conversations
- 🧠 Auto-generated chat titles
- ✏️ Rename & 🗑 Delete conversations
- 📝 Markdown rendering (code blocks, lists, formatting)
- 🎯 ChatGPT-style UI with dynamic sidebar

This project demonstrates full-stack AI engineering, real-time streaming architecture, and database-driven conversational memory.

---

# 🌟 Key Features

## 🔥 Real-Time Streaming
- Uses FastAPI `StreamingResponse`
- Frontend consumes stream using `ReadableStream`
- Token-by-token response rendering (ChatGPT-like experience)

## 💬 Multi-Session Conversations
- Each conversation stored in SQLite
- Sidebar displays all past chats
- Click to load old conversations
- New chat resets UI state

## 🧠 Auto Chat Title Generation
- First user message generates AI-based short title
- Stored in database automatically

## 🛠 Chat Management
- Rename chat
- Delete chat (cascade deletes messages)


## 📝 Markdown Support
- Supports:
  - Code blocks
  - Lists
  - Headings
  - Inline formatting
- Rendered using `react-markdown`

---

# 🏗 Tech Stack

## Backend
- FastAPI
- SQLAlchemy ORM
- SQLite
- OpenAI Chat Completions API
- StreamingResponse

## Frontend
- React (Hooks)
- Fetch streaming API
- React Markdown
- Custom CSS UI

---

# 📂 Project Structure

```
MYCHATGPT/
│
├── backend/
│   ├── main.py
│   ├── db_tables.py
│   ├── database.py
│   ├── config.py
│   └── chat.db
│
├── frontend/
│   ├── ChatGptUI.jsx
│   ├── ChatGptUI.css
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# 🗄 Database Schema

## Chats Table

| Column      | Type      | Description |
|------------|----------|-------------|
| id         | Integer  | Primary Key |
| user_id    | String   | User Identifier |
| title      | String   | Chat title |
| created_at | DateTime | Created timestamp |
| updated_at | DateTime | Updated timestamp |

## Messages Table

| Column      | Type      | Description |
|------------|----------|-------------|
| id         | Integer  | Primary Key |
| chat_id    | Integer  | Foreign Key (Chats.id) |
| role       | String   | user / assistant / system |
| content    | Text     | Message text |
| created_at | DateTime | Created timestamp |

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/MYCHATGPT.git
cd MYCHATGPT
```

---

## 2️⃣ Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

Create `.env` file inside backend:

```
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL="gpt-4o"
SQLITE_URL = "sqlite:///chat.db"
```

Run backend:

```bash
uvicorn main:app --reload --port 8000
```

Backend runs at:
```
http://localhost:8000
```

---

## 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:
```
http://localhost:5173
```



# 🛠 API Endpoints

| Method | Endpoint | Description |
|--------|----------|------------|
| POST | /api/chat | Stream LLM response |
| GET | /api/chats | Get all chats |
| GET | /api/chats/{chat_id} | Get messages of chat |
| PUT | /api/chats/{chat_id}?title= | Rename chat |
| DELETE | /api/chats/{chat_id} | Delete chat |

---

# 🎯 Technical Highlights

- Real-time streaming architecture
- Database-backed persistent conversations
- RESTful API design
- Clean state management in React
- Proper separation of backend layers
- Markdown rendering with live updates
- Cascade delete relationships
- Dynamic sidebar with chat switching

---

# 📈 Future Enhancements

- 🔐 JWT Authentication (multi-user support)
- 🌐 WebSocket streaming
- 🧠 RAG (Retrieval Augmented Generation)
- 📦 Docker & Docker Compose deployment
- ☁ AWS EC2 deployment
- 🧵 Conversation summarization
- 📌 Pin important chats
- 📊 Usage analytics dashboard

---

# 💼 Resume-Ready Description

> Built a full-stack AI chat platform with real-time LLM streaming, persistent conversation memory, dynamic session management, and production-ready API architecture using FastAPI, React, SQLAlchemy, and OpenAI APIs.

---

#  Author

**Mukhtar Ahmad**  
AI Chatbot Developer | NLP Engineer | Data Scientist  

Specialized in:
- Generative AI
- LLM-powered applications
- Full-stack AI systems
- Real-time streaming architectures

