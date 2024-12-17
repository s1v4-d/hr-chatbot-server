from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.config import Config
from apis.auth_utils import verify_password, create_access_token
from apis.models import User, get_db

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", tags=["Auth"])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    # Create a token
    access_token = create_access_token({"sub": user.username, "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}