import os
from backend.config import Config
from groq import Groq

class LLMFactory:
    """Factory class to create instances of Large Language Models."""

    @staticmethod
    def call_llm(system_message, query):
        api_key = Config.GROQ_API_KEY
        if not api_key:
            raise ValueError("API key not found.")

        groq_client = Groq(api_key=api_key)
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ]
        model = Config.LLM_MODEL_NAME
        if not model:
            raise ValueError("Model name not found.")

        chat_response = groq_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
            top_p=Config.TOP_P
        )
        return chat_response.choices[0].message.content

    @staticmethod
    def call_llm_stream(system_message, query):
        api_key = Config.GROQ_API_KEY
        if not api_key:
            raise ValueError("API key not found.")

        groq_client = Groq(api_key=api_key)
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ]
        model = Config.LLM_MODEL_NAME
        if not model:
            raise ValueError("Model name not found.")

        chat_stream = groq_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
            top_p=Config.TOP_P,
            stream=True
        )

        # chat_stream is an iterator of ChatCompletionChunk objects
        for chunk in chat_stream:
            # chunk is a ChatCompletionChunk object, not a dict
            # We can directly access chunk.choices
            if chunk.choices and chunk.choices[0].delta:
                delta = chunk.choices[0].delta
                if delta.content is not None:
                    token = delta.content
                    yield token
