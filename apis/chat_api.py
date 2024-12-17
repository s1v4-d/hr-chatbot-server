from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from backend.chatbot.chatbot import HRChatbot
from apis.auth_utils import decode_token

router = APIRouter()
security = HTTPBearer()
chatbot = HRChatbot()

class QueryRequest(BaseModel):
    query: str
    multiquery: bool = False
    reranking: bool = False
    stream: bool = False

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return payload

@router.post("/chat", tags=["Chat"])
def chat(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    try:
        if request.stream:
            def response_generator():
                # talk_to_chatbot_stream returns a generator of tokens
                for token in chatbot.talk_to_chatbot_stream(
                    user_query=request.query,
                    multiquery=request.multiquery,
                    reranking=request.reranking
                ):
                    yield token

            return StreamingResponse(response_generator(), media_type="text/plain")
        else:
            response = chatbot.talk_to_chatbot(
                user_query=request.query,
                multiquery=request.multiquery,
                reranking=request.reranking
            )
            return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")