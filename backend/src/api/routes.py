from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from src.models.rag import ChatRequest
from src.services.chat import stream_chat_response
from src.services.logging_service import log_message, log_session
import uuid

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest, background_tasks: BackgroundTasks):
    """
    Streaming chat endpoint using SSE.
    """
    # Generate session ID if not provided (though request model says Optional, usually client manages state)
    session_id = request.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
        # Log new session
        background_tasks.add_task(log_session, uuid.UUID(session_id))
    else:
        # Ensure UUID format
        try:
             uuid.UUID(str(session_id))
        except ValueError:
             session_id = str(uuid.uuid4())

    # Log User Message
    background_tasks.add_task(
        log_message, 
        uuid.UUID(str(session_id)), 
        "user", 
        request.message, 
        request.selected_text
    )

    async def event_generator():
        # Generate ID for assistant message
        assistant_msg_id = uuid.uuid4()
        
        # Send metadata event first
        import json
        yield f"data: {json.dumps({'type': 'meta', 'message_id': str(assistant_msg_id)})}\n\n"
        
        full_response = ""
        async for token in stream_chat_response(request):
            full_response += token
            yield f"data: {token}\n\n"
        
        # Log Assistant Message with the pre-generated ID
        # Note: log_message needs to support passing ID if we want to match. 
        # But our log_message function generates it. We should modify log_message or just update the logic.
        # Actually, log_message takes args. We can modify it to accept id optionally.
        # For now, let's just log it and assume we won't match perfectly if we don't fix log_message.
        # BUT we sent the ID to the client! So we MUST use that ID in the DB.
        
        # We need to manually insert or update log_message signature.
        # Let's import the session logic here to force ID? Or update log_message?
        # Let's update log_message in logging_service.py to accept optional ID.
        
        from src.services.logging_service import log_message_with_id
        await log_message_with_id(
            uuid.UUID(str(session_id)), 
            "assistant", 
            full_response, 
            message_id=assistant_msg_id
        )
        
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Admin/Utility Routes
@router.post("/index")
async def index_endpoint(background_tasks: BackgroundTasks):
    # TODO: Add auth check (X-Admin-Secret)
    # Hardcoded path for now, assuming standard layout
    docs_path = "../website/docs"
    
    async def run_indexing():
        from src.services.ingestion import parse_mdx_to_chunks
        from src.services.embedding import get_embeddings
        from src.services.vector_store import index_chunks
        import glob
        import os
        
        files = glob.glob(os.path.join(docs_path, "**/*.md"), recursive=True)
        files += glob.glob(os.path.join(docs_path, "**/*.mdx"), recursive=True)
        
        all_chunks = []
        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                chunks = parse_mdx_to_chunks(file_path, content)
                all_chunks.extend(chunks)

        if not all_chunks:
            return

        BATCH_SIZE = 50
        for i in range(0, len(all_chunks), BATCH_SIZE):
            batch = all_chunks[i:i+BATCH_SIZE]
            texts = [c.content for c in batch]
            embeddings = await get_embeddings(texts)
            await index_chunks(batch, embeddings)

    background_tasks.add_task(run_indexing)
    return {"status": "indexing_started"}

@router.post("/feedback")
async def feedback_endpoint(score: int, message_id: uuid.UUID, comment: str = None):
    from src.services.logging_service import log_feedback
    await log_feedback(message_id, score, comment)
    return {"status": "feedback_received"}
