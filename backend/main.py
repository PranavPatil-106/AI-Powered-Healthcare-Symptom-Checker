from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List

from database import engine, get_db
import models
import auth
import llm_service

# Create tables (if not using migration tool like Alembic)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Symptom Checker")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except auth.JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/auth/signup", response_model=models.Token)
def signup(user: models.UserCreate, db: Session = Depends(get_db)):
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "username": new_user.username}

@app.post("/auth/login", response_model=models.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}

@app.post("/analyze", response_model=models.SymptomResponse)
def analyze_symptoms(input: models.SymptomInput, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        print(f"Analyzing symptoms for user {current_user.email}: {input.symptoms}")
        # Call LLM Service
        analysis_result = llm_service.analyze_symptoms(input.symptoms)
        result_text = analysis_result["result"]
        severity = analysis_result["severity"]
        
        print("LLM Result:", result_text[:50] + "...")
        print("Severity:", severity)
        
        # Save to History
        new_check = models.SymptomCheck(
            user_id=current_user.id,
            symptoms=input.symptoms,
            result=result_text,
            severity=severity
        )
        db.add(new_check)
        db.commit()
        print("Saved to DB")
        
        return {"result": result_text, "severity": severity}
    except Exception as e:
        print(f"ERROR in analyze_symptoms: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=List[models.HistoryItem])
def get_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    history = db.query(models.SymptomCheck).filter(models.SymptomCheck.user_id == current_user.id).order_by(models.SymptomCheck.created_at.desc()).all()
    return history
