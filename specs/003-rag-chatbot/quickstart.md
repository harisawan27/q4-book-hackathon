# Quickstart: RAG Chatbot Development

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional)
- API Keys:
  - `OPENAI_API_KEY`
  - `QDRANT_URL` & `QDRANT_API_KEY`
  - `NEON_DATABASE_URL` (format: `postgres://user:pass@host/db`)

## Backend Setup

1. Navigate to `backend/`
2. Create `.env` file with above keys.
3. Install deps: `pip install -r requirements.txt`
4. Initialize Qdrant Collection:
   ```bash
   python scripts/init_qdrant.py
   ```
5. Index the docs:
   ```bash
   python scripts/index_book.py --path ../website/docs
   ```
6. Run dev server: `uvicorn src.main:app --reload`

## Frontend Setup

1. Navigate to `website/`
2. Install deps: `npm install`
3. Run docusaurus: `npm run start`
4. The Chat Widget should appear in the bottom right corner.

## Testing

- **General Q&A**: Open chat, ask "What is ROS2?".
- **Context Q&A**: Select text on the page, verify it appears in chat input, ask "Explain this".
- **Admin**:
  - `POST /api/v1/index` to re-index.
  - Check Neon DB `messages` table for logs.