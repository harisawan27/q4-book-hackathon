import ssl
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from qdrant_client import QdrantClient, AsyncQdrantClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import get_settings

settings = get_settings()

# Qdrant Client
def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )

# Qdrant Client (Async)
def get_async_qdrant_client() -> AsyncQdrantClient:
    return AsyncQdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )

# Neon Postgres (SQLAlchemy Async)
# Ensure the URL starts with postgresql+asyncpg://
# Also strip out sslmode and channel_binding which asyncpg doesn't support directly
DATABASE_URL = settings.NEON_DATABASE_URL
if DATABASE_URL:
    # Parse the URL to remove incompatible query params
    parsed = urlparse(DATABASE_URL)
    query_params = parse_qs(parsed.query)

    # Remove params that asyncpg doesn't support
    query_params.pop('sslmode', None)
    query_params.pop('channel_binding', None)

    # Rebuild query string
    new_query = urlencode(query_params, doseq=True)

    # Rebuild URL with postgresql+asyncpg://
    if parsed.scheme in ('postgres', 'postgresql'):
        new_scheme = 'postgresql+asyncpg'
    else:
        new_scheme = parsed.scheme

    DATABASE_URL = urlunparse((
        new_scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

# Create SSL context for secure connection
ssl_context = ssl.create_default_context()

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"ssl": ssl_context},
    # Connection pool settings to handle Neon's connection timeouts
    pool_pre_ping=True,  # Check connection health before using
    pool_recycle=300,    # Recycle connections after 5 minutes
    pool_size=5,         # Number of connections to keep
    max_overflow=10,     # Allow up to 10 additional connections
)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
