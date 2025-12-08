import sys
import os
import asyncio
import glob

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.ingestion import parse_mdx_to_chunks
from src.services.embedding import get_embeddings
from src.services.vector_store import index_chunks

async def main(docs_path: str):
    print(f"Scanning for .md and .mdx files in {docs_path}...")
    
    files = glob.glob(os.path.join(docs_path, "**/*.md"), recursive=True)
    files += glob.glob(os.path.join(docs_path, "**/*.mdx"), recursive=True)
    
    print(f"Found {len(files)} files.")
    
    all_chunks = []
    
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            chunks = parse_mdx_to_chunks(file_path, content)
            all_chunks.extend(chunks)
            
    print(f"Generated {len(all_chunks)} chunks total.")
    
    if not all_chunks:
        print("No chunks to index.")
        return

    # Process in batches to avoid hitting API limits or memory issues
    BATCH_SIZE = 50
    for i in range(0, len(all_chunks), BATCH_SIZE):
        batch = all_chunks[i:i+BATCH_SIZE]
        texts = [c.content for c in batch]
        
        print(f"Embedding batch {i//BATCH_SIZE + 1}...")
        embeddings = await get_embeddings(texts)
        
        print(f"Indexing batch {i//BATCH_SIZE + 1}...")
        await index_chunks(batch, embeddings)
        
    print("Indexing complete!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="Path to docs directory")
    args = parser.parse_args()
    
    asyncio.run(main(args.path))
