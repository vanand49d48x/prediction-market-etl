from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterable, List


def _to_dt(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        # Many APIs use ISO-8601
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None


def normalize_kalshi(markets: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normalize Kalshi markets into our unified schema.

    Assumptions (adjust based on real data):
      - each market has:
        - 'id' or 'ticker'
        - 'title' or 'question'
        - 'category' (optional)
        - 'event_close_time' (optional)
        - 'yes_price', 'no_price' (or derived from orderbook)
        - 'volume_24h', 'liquidity' (optional)
    """
    out: List[Dict[str, Any]] = []

    for m in markets:
        market_id = m.get("id") or m.get("ticker") or ""
        if not market_id:
            continue

        title = m.get("title") or m.get("question")
        category = m.get("category")
        event_date = _to_dt(m.get("event_close_time") or m.get("expiry_time"))
        yes_price = m.get("yes_price")
        no_price = m.get("no_price")
        volume_24h = m.get("volume_24h") or m.get("volume")
        liquidity = m.get("liquidity")

        # For binary markets, we often just store the YES leg as outcome 'YES'
        record_yes = {
            "market_id": market_id,
            "title": title,
            "outcome": "YES",
            "yes_price": yes_price,
            "no_price": no_price,
            "volume_24h": volume_24h,
            "liquidity": liquidity,
            "category": category,
            "event_date": event_date,
            "source": "Kalshi",
        }
        out.append(record_yes)

    return out


def normalize_polymarket(markets: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normalize Polymarket markets into our unified schema.

    Assumptions (adjust based on real data):
      - each market has:
        - 'id'
        - 'question' or 'title'
        - 'category' (optional)
        - 'end_date' (optional)
        - an 'outcomes' list or prices fields
    """
    out: List[Dict[str, Any]] = []

    for m in markets:
        market_id = m.get("id") or m.get("_id") or ""
        if not market_id:
            continue

        title = m.get("question") or m.get("title")
        category = m.get("category")
        event_date = _to_dt(m.get("end_date") or m.get("expiryTime"))

        # Some Polymarket APIs expose individual outcome prices.
        # We'll try to be generic: if an 'outcomes' list exists, make one row per outcome.
        outcomes = m.get("outcomes") or []

        if isinstance(outcomes, list) and outcomes:
            for outcome in outcomes:
                outcome_name = outcome.get("name") or outcome.get("outcome") or "UNKNOWN"
                yes_price = outcome.get("price") or outcome.get("yes_price")
                no_price = outcome.get("no_price")
                volume_24h = outcome.get("volume_24h") or outcome.get("volume")
                liquidity = outcome.get("liquidity")

                out.append(
                    {
                        "market_id": market_id,
                        "title": title,
                        "outcome": outcome_name,
                        "yes_price": yes_price,
                        "no_price": no_price,
                        "volume_24h": volume_24h,
                        "liquidity": liquidity,
                        "category": category,
                        "event_date": event_date,
                        "source": "Polymarket",
                    }
                )
        else:
            # Fallback for simpler/binary representation
            yes_price = m.get("yes_price") or m.get("price")
            no_price = m.get("no_price")
            volume_24h = m.get("volume_24h") or m.get("volume")
            liquidity = m.get("liquidity")

            out.append(
                {
                    "market_id": market_id,
                    "title": title,
                    "outcome": "YES",
                    "yes_price": yes_price,
                    "no_price": no_price,
                    "volume_24h": volume_24h,
                    "liquidity": liquidity,
                    "category": category,
                    "event_date": event_date,
                    "source": "Polymarket",
                }
            )

    return out
