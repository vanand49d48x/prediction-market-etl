CREATE TABLE IF NOT EXISTS prediction_markets (
    id SERIAL PRIMARY KEY,
    market_id TEXT NOT NULL,
    title TEXT,
    outcome TEXT,
    yes_price NUMERIC,
    no_price NUMERIC,
    volume_24h NUMERIC,
    liquidity NUMERIC,
    category TEXT,
    event_date TIMESTAMPTZ,
    source TEXT NOT NULL,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_prediction_markets_source
    ON prediction_markets (source);

CREATE INDEX IF NOT EXISTS idx_prediction_markets_market
    ON prediction_markets (market_id, source);

CREATE INDEX IF NOT EXISTS idx_prediction_markets_fetched
    ON prediction_markets (fetched_at);
