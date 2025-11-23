import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise RuntimeError("DB_URL environment variable is required")

KALSHI_BASE_URL = os.getenv("KALSHI_BASE_URL", "https://api.kalshi.com/v1")
POLYMARKET_BASE_URL = os.getenv("POLYMARKET_BASE_URL", "https://clob.polymarket.com")

# Optional auth tokens for Kalshi (adapt as needed)
KALSHI_API_KEY = os.getenv("KALSHI_API_KEY")
