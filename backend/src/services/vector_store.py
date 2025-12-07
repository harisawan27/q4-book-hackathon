from typing import List
from qdrant_client.http import models
from src.core.database import get_qdrant_client
from src.core.config import get_settings
from src.models.rag import VectorChunk
import uuid

settings = get_settings()

async def index_chunks(chunks: List[VectorChunk], embeddings: List[List[float]]):
    """
    Upserts chunks and their embeddings into Qdrant.
    """
    client = get_qdrant_client()
    
    points = []
    for chunk, embedding in zip(chunks, embeddings):
        # Generate a deterministic or random ID
        point_id = str(uuid.uuid4())
        
        points.append(models.PointStruct(
            id=point_id,
            vector=embedding,
            payload=chunk.model_dump()
        ))
        
    # Upsert in batches if needed, Qdrant client handles basic batching often
    client.upsert(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        points=points
    )
    print(f"Indexed {len(points)} chunks.")
