from typing import List
from src.core.database import get_async_qdrant_client
from src.core.config import get_settings
from src.models.rag import VectorChunk

settings = get_settings()

async def search_similar_chunks(query_vector: List[float], limit: int = 5) -> List[VectorChunk]:
    """
    Searches Qdrant for similar chunks (Async).
    """
    client = get_async_qdrant_client()
    
    # Note: Async client methods are awaitable
    # In recent versions, search is available on async client too.
    response = await client.query_points(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )
    
    results = []
    for hit in response.points:
        results.append(VectorChunk(**hit.payload))
        
    return results