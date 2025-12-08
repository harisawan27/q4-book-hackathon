import sys
import os
# Add parent directory to path to import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import get_qdrant_client
from src.core.config import get_settings
from qdrant_client.http import models

def init_qdrant():
    settings = get_settings()
    client = get_qdrant_client()
    collection_name = settings.QDRANT_COLLECTION_NAME
    
    # Check if collection exists
    collections = client.get_collections()
    exists = any(c.name == collection_name for c in collections.collections)
    
    if not exists:
        print(f"Creating collection: {collection_name}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=768,  # Gemini text-embedding-004
                distance=models.Distance.COSINE
            )
        )
        print("Collection created successfully.")
    else:
        print(f"Collection {collection_name} already exists.")

if __name__ == "__main__":
    init_qdrant()