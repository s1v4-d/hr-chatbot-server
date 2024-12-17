from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.upload_api import router as upload_router
from apis.chat_api import router as chat_router
from apis.login_api import router as login_router
from apis.registration_api import router as registration_router
from backend.config import Config
from apis.models import SessionLocal, User
from apis.auth_utils import hash_password

def ensure_admin_user():
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == Config.ADMIN_USERNAME).first()
        if not admin_user:
            new_admin = User(
                username=Config.ADMIN_USERNAME,
                email="admin@example.com",
                full_name="Admin User",
                password_hash=hash_password(Config.ADMIN_PASSWORD),
                is_admin=True
            )
            db.add(new_admin)
            db.commit()
    finally:
        db.close()

# Run the function at startup to ensure an admin user exists
ensure_admin_user()

# Initialize FastAPI app
app = FastAPI(
    title="HR Chatbot API",
    description="An API for document embedding, conversational interactions, and user authentication.",
    version="1.0.0"
)

# Configure CORS Middleware
origins = [
    "http://localhost:3000",  # React app during development
    "https://your-production-domain.com"  # Frontend domain in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(login_router, prefix="/api")
app.include_router(registration_router, prefix="/api")

@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "API is running"}