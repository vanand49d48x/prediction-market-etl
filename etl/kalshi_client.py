from __future__ import annotations

import logging
from typing import Any, Dict, List

import requests

from .config import KALSHI_BASE_URL, KALSHI_API_KEY

logger = logging.getLogger(__name__)


def _headers() -> dict[str, str]:
    headers: dict[str, str] = {"Accept": "application/json"}
    if KALSHI_API_KEY:
        headers["Authorization"] = f"Bearer {KALSHI_API_KEY}"
    return headers


def fetch_markets() -> List[Dict[str, Any]]:
    """
    Fetch markets from Kalshi.

    This assumes a 'GET /markets' style endpoint returning JSON with key 'markets'.
    Adjust parsing according to the actual API response you receive.
    """
    url = f"{KALSHI_BASE_URL.rstrip('/')}/markets"
    logger.info("Fetching Kalshi markets from %s", url)

    resp = requests.get(url, headers=_headers(), timeout=30)
    resp.raise_for_status()
    data = resp.json()

    markets = data.get("markets", data)  # sometimes the list may be top-level

    if not isinstance(markets, list):
        logger.warning("Unexpected Kalshi markets payload shape: %s", type(markets))
        return []

    logger.info("Fetched %d Kalshi markets", len(markets))
    return markets
