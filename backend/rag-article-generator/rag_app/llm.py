import os
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from .config import MISTRAL_MODEL

def get_llm(temperature: float = 0.0):
    """
    Return a ChatMistralAI instance. Requires env var MISTRAL_API_KEY.
    """
    # Raises at call time if missing; that's fine to surface clearly.
    return ChatMistralAI(model=MISTRAL_MODEL, temperature=temperature)

def get_embeddings():
    """
    Return Mistral embeddings. Requires env var MISTRAL_API_KEY.
    """
    return MistralAIEmbeddings()
