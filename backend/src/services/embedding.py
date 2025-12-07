from typing import List
import google.generativeai as genai
from src.core.config import get_settings

settings = get_settings()
genai.configure(api_key=settings.GEMINI_API_KEY)

async def get_embedding(text: str) -> List[float]:
    """
    Generates embedding for a single string using text-embedding-004.
    """
    # Gemini embedding model
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_query"
    )
    return result['embedding']

async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of strings.
    """
    # Gemini handles batching
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=texts,
        task_type="retrieval_document"
    )
    return result['embedding']