import re
from typing import List
from src.models.rag import VectorChunk

def parse_mdx_to_chunks(file_path: str, content: str) -> List[VectorChunk]:
    """
    Parses MDX content and splits it into chunks based on headers.
    Preserves context by tracking current headers.
    """
    lines = content.split('\n')
    chunks = []
    
    current_h1 = ""
    current_h2 = ""
    current_h3 = ""
    
    current_chunk_content = []
    
    # Helper to save current chunk
    def save_chunk():
        if current_chunk_content:
            text = "\n".join(current_chunk_content).strip()
            if text:
                # Build header path
                headers = [h for h in [current_h1, current_h2, current_h3] if h]
                header_path = " > ".join(headers)
                
                # Derive URL slug from file path (simplified assumption)
                # Assuming file_path is like "docs/intro/index.md"
                # Handle Windows paths which might have double backslashes
                url_slug = file_path.replace("docs\\", "").replace("docs/", "").replace(".md", "").replace("\\", "/")
                
                chunks.append(VectorChunk(
                    content=text,
                    source_file=file_path,
                    url_slug=url_slug,
                    header_path=header_path,
                    chunk_index=len(chunks)
                ))
            current_chunk_content.clear()

    for line in lines:
        # Simple header detection
        # Skip frontmatter logic for simplicity or handle it?
        # Assuming MDX, frontmatter is ---...--- at start. 
        
        # Detect Headers
        h1_match = re.match(r'^#\s+(.+)', line)
        h2_match = re.match(r'^##\s+(.+)', line)
        h3_match = re.match(r'^###\s+(.+)', line)
        
        if h1_match:
            save_chunk()
            current_h1 = h1_match.group(1)
            current_h2 = ""
            current_h3 = ""
            current_chunk_content.append(line) # Include header in chunk
        elif h2_match:
            save_chunk()
            current_h2 = h2_match.group(1)
            current_h3 = ""
            current_chunk_content.append(line)
        elif h3_match:
            save_chunk()
            current_h3 = h3_match.group(1)
            current_chunk_content.append(line)
        else:
            current_chunk_content.append(line)
            
    save_chunk() # Save last chunk
    
    return chunks
