from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SymptomCheck(Base):
    __tablename__ = "symptom_checks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symptoms = Column(Text)
    result = Column(Text)
    severity = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class SymptomInput(BaseModel):
    symptoms: str

class SymptomResponse(BaseModel):
    result: str
    severity: str | None = None

class HistoryItem(BaseModel):
    symptoms: str
    result: str
    severity: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
