import os

SERVICE_NAME = os.getenv("SERVICE_NAME", "message-service")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@postgres:5432/message_db",
)

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

SOCKETIO_PATH = os.getenv("SOCKETIO_PATH", "/socket.io")
SOCKETIO_NAMESPACE = os.getenv("SOCKETIO_NAMESPACE", "/chat")
