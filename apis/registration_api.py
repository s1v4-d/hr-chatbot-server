from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from apis.models import User, get_db
from apis.auth_utils import hash_password

router = APIRouter()

class RegistrationRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str

@router.post("/register", tags=["Auth"])
def register(request: RegistrationRequest, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user_email = db.query(User).filter(User.email == request.email).first()
    if existing_user_email:
        raise HTTPException(status_code=400, detail="Email already in use.")

    # Check if username already exists
    existing_user_username = db.query(User).filter(User.username == request.username).first()
    if existing_user_username:
        raise HTTPException(status_code=400, detail="Username already taken.")

    # Create new user
    new_user = User(
        username=request.username,
        email=request.email,
        full_name=request.full_name,
        password_hash=hash_password(request.password),
        is_admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "success", "message": "User registered successfully."}