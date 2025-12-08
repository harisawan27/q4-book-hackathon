from src.models.db import Session, Message, Feedback
from src.core.database import AsyncSessionLocal
import uuid

async def log_session(session_id: uuid.UUID, metadata: dict = None):
    async with AsyncSessionLocal() as session:
        new_session = Session(id=session_id, user_metadata=metadata)
        session.add(new_session)
        await session.commit()

async def log_message(session_id: uuid.UUID, role: str, content: str, selected_context: str = None, retrieved_chunks: list = None) -> uuid.UUID:
    async with AsyncSessionLocal() as session:
        msg = Message(
            session_id=session_id,
            role=role,
            content=content,
            selected_context=selected_context,
            retrieved_chunks=retrieved_chunks
        )
        session.add(msg)
        await session.commit()
        await session.refresh(msg)
        return msg.id

async def log_message_with_id(session_id: uuid.UUID, role: str, content: str, message_id: uuid.UUID, selected_context: str = None):
    async with AsyncSessionLocal() as session:
        msg = Message(
            id=message_id,
            session_id=session_id,
            role=role,
            content=content,
            selected_context=selected_context
        )
        session.add(msg)
        await session.commit()

async def log_feedback(message_id: uuid.UUID, score: int, comment: str = None):
    async with AsyncSessionLocal() as session:
        feedback = Feedback(
            message_id=message_id,
            score=score,
            comment=comment
        )
        session.add(feedback)
        await session.commit()