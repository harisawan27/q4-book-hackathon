from typing import AsyncGenerator
import google.generativeai as genai
from src.core.config import get_settings
from src.services.embedding import get_embedding
from src.services.retrieval import search_similar_chunks
from src.models.rag import ChatRequest

settings = get_settings()
genai.configure(api_key=settings.GEMINI_API_KEY)

SYSTEM_PROMPT = """You are a helpful AI assistant for the Docusaurus Robotics Book.

Your Rules:
1. For general greetings (e.g., "hi", "hello") or questions about your identity, reply politely and briefly. You do NOT need context for this.
2. For specific questions about robotics or the book's content, answer STRICTLY based on the provided context.
3. If the answer to a specific question is not in the context, say "I cannot answer this based on the book content."
4. Include citations to the source sections where appropriate (e.g., "Source: [Title](url)").
"""

async def stream_chat_response(request: ChatRequest) -> AsyncGenerator[str, None]:
    # 1. Embed query
    query_vector = await get_embedding(request.message)
    
    # 2. Retrieve context
    chunks = await search_similar_chunks(query_vector, limit=5)
    
    # 3. Assemble Context
    context_text = "\n\n".join([
        f"Source: {c.header_path} (URL: {c.url_slug})\nContent: {c.content}"
        for c in chunks
    ])
    
    if request.selected_text:
        user_prompt = f"""
        You have two sources of information:
        1. "Selected Text": Specific text the user has highlighted.
        2. "Retrieved Context": Background information from the book.

        If the User's Question refers to "this" or "it", it most likely refers to the "Selected Text".
        Answer based on the "Selected Text" first. Use "Retrieved Context" only if needed to explain concepts found in the "Selected Text".

        Selected Text:
        {request.selected_text}

        Retrieved Context:
        {context_text}

        User Question: {request.message}
        """
    else:
        user_prompt = f"""
        Context:
        {context_text}
        
        User Question: {request.message}
        """

    # 4. Stream Response
    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=SYSTEM_PROMPT
        )
        
        response = model.generate_content(user_prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"[ERROR] {str(e)}"