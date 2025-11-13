import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://example.com/miniapp/").strip()

DB_DSN = os.getenv(
    "DB_DSN",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/tg_app",
).strip()
