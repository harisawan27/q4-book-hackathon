# Data Model: Integrated RAG Chatbot

## Database: Neon (PostgreSQL)

Used for logging, analytics, and session history. NOT for vector storage.

### Table: `sessions`
| Column | Type | Description |
|---|---|---|
| `id` | UUID | PK |
| `created_at` | TIMESTAMP | |
| `user_metadata` | JSONB | Browser info, IP (hashed) |

### Table: `messages`
| Column | Type | Description |
|---|---|---|
| `id` | UUID | PK |
| `session_id` | UUID | FK -> sessions.id |
| `role` | TEXT | 'user' or 'assistant' |
| `content` | TEXT | The message text |
| `selected_context` | TEXT | (Nullable) Text user highlighted |
| `retrieved_chunks` | JSONB | Array of chunk IDs/scores used |
| `created_at` | TIMESTAMP | |

### Table: `feedback`
| Column | Type | Description |
|---|---|---|
| `id` | UUID | PK |
| `message_id` | UUID | FK -> messages.id |
| `score` | INT | 1 (thumbs up) or -1 (thumbs down) |
| `comment` | TEXT | Optional user comment |

## Database: Qdrant (Vector Store)

### Collection: `book_chunks`

- **Vectors**: 1536 dimensions (OpenAI text-embedding-3-small)
- **Payload Schema**:
  ```json
  {
    "content": "string (text of the chunk)",
    "source_file": "string (path to .md file)",
    "url_slug": "string (docusaurus route)",
    "header_path": "string (hierarchy e.g. 'Module 1 > Setup')",
    "chunk_index": "integer"
  }
  ```
