from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
from app import models, schemas, auth
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/surveys/", response_model=schemas.Survey)
async def create_survey(
    survey: schemas.SurveyCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_survey = models.Survey(**survey.dict(), creator_id=current_user.id)
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey

@app.get("/surveys/", response_model=List[schemas.Survey])
async def get_surveys(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    surveys = db.query(models.Survey).filter(models.Survey.creator_id == current_user.id).all()
    return surveys

@app.get("/surveys/{survey_id}", response_model=schemas.Survey)
async def get_survey(
    survey_id: int,
    db: Session = Depends(get_db)
):
    survey = db.query(models.Survey).filter(models.Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

@app.post("/surveys/{survey_id}/respond", response_model=schemas.SurveyResponse)
async def submit_survey_response(
    survey_id: int,
    response: schemas.SurveyResponseCreate,
    db: Session = Depends(get_db)
):
    survey = db.query(models.Survey).filter(models.Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    db_response = models.SurveyResponse(**response.dict())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response 