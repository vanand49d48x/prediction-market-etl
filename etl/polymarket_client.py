from __future__ import annotations

import logging
from typing import Any, Dict, List

import requests

from .config import POLYMARKET_BASE_URL

logger = logging.getLogger(__name__)


def fetch_markets() -> List[Dict[str, Any]]:
    """
    Fetch markets from Polymarket.

    This assumes a 'GET /markets' style endpoint returning JSON with key 'markets'
    or a raw list. Adjust as needed based on actual API response.
    """
    url = f"{POLYMARKET_BASE_URL.rstrip('/')}/markets"
    logger.info("Fetching Polymarket markets from %s", url)

    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    markets = data.get("markets", data)

    if not isinstance(markets, list):
        logger.warning("Unexpected Polymarket markets payload shape: %s", type(markets))
        return []

    logger.info("Fetched %d Polymarket markets", len(markets))
    return markets
