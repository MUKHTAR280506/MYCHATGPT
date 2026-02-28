import os
import datetime
from typing import List, Dict,Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from config import init_db
from openai import OpenAI
from db_tables import Chat, Message
from database import OPENAI_API_KEY, OPENAI_MODEL , SessionLocal 
from sqlalchemy.orm import Session

OPENAI_API_KEY= OPENAI_API_KEY
MODEL= OPENAI_MODEL

if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY IN ENVIRONMENT")

# create openai client

client = OpenAI(api_key=OPENAI_API_KEY)



   

app = FastAPI(title="ChatGPT proxy for React UI")

@app.on_event("startup")
def on_startup():
    init_db()

# allow your frontend origins

origins= [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Chat-Id"]

)

class MessageSchema(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[MessageSchema]  

class ChatResponse(BaseModel):
    reply: str

def generate_chat_title(first_message : str) -> str:
    
    response = client.chat.completions.create (
        model = MODEL,
        messages = [
            {"role": "system",
             "content": "Generate a short 3 word title for this conversation"},
             {"role": "user", "content": first_message}
             ]
            )
    
    return response.choices[0].message.content.strip().replace('"','')    

def generate_stream(message_payload , chat_id: int, new_chat_created, first_message, db: Session):

    
   
    full_response = ""


    stream = client.chat.completions.create(
        model=MODEL,
        messages=message_payload,
        stream=True
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            full_response += content
            yield content

    bot_msg = Message(
        chat_id=chat_id,
        role="assistant",
        content= full_response
    )   

    db.add(bot_msg)
    
    if new_chat_created:
        title = generate_chat_title (first_message)
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        chat.title = title

  
    db.commit()
    


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest, chat_id: Optional[int]=None):

    db = SessionLocal()
    new_chat_created = False
    if not chat_id:
        new_chat = Chat(user_id="mukhtar")
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        chat_id = new_chat.id
        new_chat_created = True

    user_message = req.messages[-1]
    db_msg = Message(
        chat_id = chat_id,
        role="user",
        content=user_message.content

    )
  
    db.add(db_msg)
    db.commit()
    


    messages_payload = [
        {"role": m.role, "content": m.content}
        for m in req.messages
    ]

    response = StreamingResponse (
    generate_stream(messages_payload, chat_id, new_chat_created, user_message.content, db),
    media_type="text/plain"
    )

    response.headers["X-Chat-Id"] = str(chat_id)
    return response

@app.get("/api/chats")
def get_chats():
    db = SessionLocal()
    chats = db.query(Chat).order_by(Chat.id.desc()).all()
    db.close()
    return chats
       
       
@app.get("/api/chats/{chat_id}")
def get_chat_messages(chat_id: int):
    db = SessionLocal()
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    db.close()
    return messages

@app.put("/api/chats/{chat_id}")
def rename_chat(chat_id: int, title: str):
    db = SessionLocal()
    chat = db.query(Chat).filter(Chat.id==chat_id).first()
    if not chat:
        db.close()
        raise HTTPException(status_code=404, detail="Chat Not found")
    chat.title = title
    db.commit()
    db.close()

    return {"message": "Chat renamed successfully"}

@app.delete("/api/chats/{chat_id}")
def delete_chat(chat_id: int):
    db= SessionLocal()
    chat= db.query(Chat).filter(Chat.id==chat_id).first()
    if not chat:
        db.close()
        raise HTTPException (status_code=404, detail="Chat not found")
    
    db.delete(chat)
    db.commit()
    db.close()

    return {"message": "Chat deteleted Successfully"}
