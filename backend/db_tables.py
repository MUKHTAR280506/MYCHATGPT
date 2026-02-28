import datetime
from database import Base

from sqlalchemy import Column, Integer, String, DateTime , ForeignKey , Text
from sqlalchemy.orm import relationship

class Chat(Base):

    __tablename__="chats"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String, default = "New Chat")
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    
    messages = relationship("Message",back_populates="chat", cascade="all, delete")

class Message(Base):
    __tablename__="messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    role = Column(String) # user / assistant / system
    content = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    chat = relationship("Chat", back_populates="messages")
