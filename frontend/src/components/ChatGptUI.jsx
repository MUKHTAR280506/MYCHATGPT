import React, { useState, useRef, useEffect } from "react";
import "./ChatGptUI.css";
import ReactMarkdown from "react-markdown";

export default function ChatGptUI() {

  const [messages, setMessages] = useState([]);
  const [chats, setChats] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);

  const scrollRef = useRef(null);
  const [input, setInput] = useState("");

  /* -------------------- LOAD ALL CHATS -------------------- */
  useEffect(() => {
    fetchChats();
  }, []);

  const fetchChats = async () => {
    const res = await fetch("http://localhost:8000/api/chats");
    const data = await res.json();
    setChats(data);
  };

  /* -------------------- LOAD MESSAGES OF A CHAT -------------------- */
  const loadChat = async (chatId) => {
    setCurrentChatId(chatId);

    const res = await fetch(`http://localhost:8000/api/chats/${chatId}`);
    const data = await res.json();

    const formatted = data.map(msg => ({
      id: msg.id,
      sender: msg.role === "user" ? "user" : "chatbot",
      text: msg.content
    }));

    setMessages(formatted);
  };

  /* -------------------- NEW CHAT -------------------- */
  const startNewChat = () => {
    setCurrentChatId(null);
    setMessages([
      { id: 1, sender: "chatbot", text: "Welcome to myChatGpt. Please ask your query" }
    ]);
  };

  /* -------------------- SEND MESSAGE -------------------- */
  const sendMessage = async () => {
    const trimmedMsg = input.trim();
    if (!trimmedMsg) return;

    const userMsg = {
      id: Date.now(),
      sender: "user",
      text: trimmedMsg
    };

    setMessages(prev => [...prev, userMsg]);
    setInput("");

    const payload = [
      { role: "system", content: "You are a helpful assistant. Provide response in nicely represented format" },
      ...messages.map(m => ({
        role: m.sender === "user" ? "user" : "assistant",
        content: m.text
      })),
      { role: "user", content: trimmedMsg }
    ];

    const res = await fetch(
      `http://localhost:8000/api/chat${currentChatId ? `?chat_id=${currentChatId}` : ""}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: payload })
      }
    );
    const newChatId = res.headers.get("X-Chat-Id");

    if (!currentChatId && newChatId) {
       setCurrentChatId(Number(newChatId));
    }
    const botId = "bot" + Date.now();

    setMessages(prev => [
      ...prev,
      { id: botId, sender: "chatbot", text: "" }
    ]);

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let result = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      result += chunk;

      setMessages(prev =>
        prev.map(msg =>
          msg.id === botId ? { ...msg, text: result } : msg
        )
      );
    }

    // Refresh chat list (in case new chat created)
    fetchChats();
  };

  /* -------------------- AUTO SCROLL -------------------- */
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  /* ---------------Chat  Rename function --------------*/
  
  const handleRename = async (chatId) => {
    const newTitle = prompt("Enter new chat title");
    if(! newTitle) return ;
    await fetch (`http://localhost:8000/api/chats/${chatId}?title=${encodeURIComponent(newTitle)}`,
    {method: "PUT"});

    fetchChats();
    
  };

  /*-------------------Chat Delete function ----------- */
  const handleDelete = async(chatId) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this Chat?");
    if(!confirmDelete) return;
    
    await fetch(`http://localhost:8000/api/chats/${chatId}`, 
                {method: "DELETE"}
    );
    if(currentChatId == chatId) {
      startNewChat();
    }
    fetchChats();
  }


  /* -------------------- UI -------------------- */
  return (
    <div className="fullpage">

      <div className="left-panel">
        <button className="newchat-btn" onClick={startNewChat}>
          New Chat
        </button>

        <details className="details" open>
          <summary>My Chats</summary>

          {chats.map(chat => (
            <div className="chats"
              key={chat.id}
            >  
             <span onClick={() => loadChat(chat.id)}>
              { chat.title || `Chat ${chat.id}`}
            </span>

            <div class="icon_button">
               <button onClick={() => handleRename(chat.id)}>✏️</button>
               <button onClick={() => handleDelete(chat.id)}>🗑</button>
            </div>
            </div> 
          ))}

        </details>
      </div>

      <div className="right-panel">

        <header className="right-header">
          <div>MyChatGpt</div>
        </header>

        <div className="chat-body" ref={scrollRef}>
          {messages.map(msg => (
            <div
              key={msg.id}
              className={`chat-message ${msg.sender === "user" ? "user" : "chatbot"}`}
            >
              <div className="message-content"><ReactMarkdown>{msg.text}</ReactMarkdown></div>
            </div>
          ))}
        </div>

        <div className="chat-input-container">
          <textarea
            className="chatinput-area"
            placeholder="Type your Query here...."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
            rows={1}
          />
          <button className="send-btn" onClick={sendMessage}>
            Send
          </button>
        </div>

      </div>
    </div>
  );
}