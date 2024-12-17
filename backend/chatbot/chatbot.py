from backend.chatbot.llm_factory import LLMFactory
from backend.config import Config
from backend.vector_management.vector_search import VectorSearch
import backend.chatbot.hr_chatbot_prompts as prompts

class HRChatbot:
    def __init__(self):
        print("[DEBUG] Initializing HRChatbot...")
        self.vector_search = VectorSearch(
            embedding_model_name=Config.EMBEDDING_MODEL_NAME,
            pinecone_api_key=Config.PINECONE_API_KEY,
            pinecone_index_name=Config.PINECONE_INDEX_NAME,
        )
        self.llm = LLMFactory

    def talk_to_chatbot(self, user_query, multiquery=False, reranking=False):
        context = self.vector_search.get_context(user_query, top_k=3, multiquery=multiquery, reranking=reranking)
        system_prompt = prompts.system_prompt()
        user_prompt = prompts.user_prompt(context, user_query)
        response = self.llm.call_llm(system_prompt, user_query)
        return response

    def talk_to_chatbot_stream(self, user_query, multiquery=False, reranking=False):
        context = self.vector_search.get_context(user_query, top_k=3, multiquery=multiquery, reranking=reranking)
        system_prompt = prompts.system_prompt()
        user_prompt = prompts.user_prompt(context, user_query)
        # Return a generator that yields tokens
        return self.llm.call_llm_stream(system_prompt, user_query)