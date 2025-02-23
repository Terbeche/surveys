from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class QuestionBase(BaseModel):
    id: str
    text: str
    type: str
    options: Optional[List[str]] = None
    required: bool

class SurveyBase(BaseModel):
    title: str
    description: str
    questions: List[QuestionBase]

class SurveyCreate(SurveyBase):
    pass

class Survey(SurveyBase):
    id: int
    creator_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnswerBase(BaseModel):
    questionId: str
    value: Any

class SurveyResponseCreate(BaseModel):
    survey_id: int
    answers: List[AnswerBase]

class SurveyResponse(SurveyResponseCreate):
    id: int
    submitted_at: datetime

    class Config:
        from_attributes = True