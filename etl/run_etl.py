from __future__ import annotations

import logging
from datetime import datetime

import pandas as pd

from .db import get_engine
from .kalshi_client import fetch_markets as fetch_kalshi_markets
from .polymarket_client import fetch_markets as fetch_polymarket_markets
from .normalize import normalize_kalshi, normalize_polymarket

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting ETL run")

    # Fetch
    kalshi_raw = fetch_kalshi_markets()
    polymarket_raw = fetch_polymarket_markets()

    # Normalize
    kalshi_norm = normalize_kalshi(kalshi_raw)
    poly_norm = normalize_polymarket(polymarket_raw)

    combined = kalshi_norm + poly_norm

    if not combined:
        logger.warning("No records to insert; exiting.")
        return

    # Add fetched_at column
    fetched_at = datetime.utcnow()
    for rec in combined:
        rec["fetched_at"] = fetched_at

    df = pd.DataFrame(combined)

    logger.info("Prepared %d rows for insertion", len(df))

    engine = get_engine()

    # Append snapshot to prediction_markets
    with engine.begin() as conn:
        df.to_sql("prediction_markets", conn, if_exists="append", index=False)

    logger.info("ETL run complete, inserted %d rows", len(df))


if __name__ == "__main__":
    main()
