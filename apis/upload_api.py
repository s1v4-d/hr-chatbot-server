from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.augmentations.document_processor import DocumentProcessor
from backend.embeddings.embedding_generator import EmbeddingGenerator
from backend.vector_management.pinecone_manager import PineconeManager
from backend.config import Config
import os
import time
from apis.auth_utils import decode_token

router = APIRouter()
security = HTTPBearer()

document_processor = DocumentProcessor(chunk_size=1000, chunk_overlap=100)
embedding_generator = EmbeddingGenerator(model_name=Config.EMBEDDING_MODEL_NAME)
pinecone_manager = PineconeManager(
    api_key=Config.PINECONE_API_KEY,
    index_name=Config.PINECONE_INDEX_NAME
)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return payload

@router.post("/upload", tags=["Upload"])
async def upload_document(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    # Check if user is admin
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Only admin can upload documents.")

    start_time = time.time()

    # Validate file type
    if file.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a DOCX file.")

    try:
        temp_file_path = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)

        # Save file to disk
        with open(temp_file_path, "wb") as f:
            while chunk := await file.read(1024):
                f.write(chunk)

        # Schedule processing in the background
        background_tasks.add_task(process_document, temp_file_path, file.filename)
        end_time = time.time()

        return {"status": "Accepted", "message": "File is being processed", "processing_time": end_time - start_time}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

async def process_document(temp_file_path, filename):
    try:
        chunks = document_processor.process_docx(temp_file_path)
        to_upsert = []
        for idx, chunk in enumerate(chunks):
            vector_id = f"{filename}_{idx}"
            embedding = embedding_generator.generate_embedding(chunk)
            to_upsert.append((vector_id, embedding, {"chunk": chunk}))
        pinecone_manager.upsert_vectors(to_upsert)
        os.remove(temp_file_path)
    except Exception as e:
        print(f"Error during document processing: {e}")