# Prediction Market ETL (Kalshi + Polymarket → Postgres → Tableau)

This repo fetches prediction market data from **Kalshi** and **Polymarket**, normalizes it,
stores it in **PostgreSQL**, and is ready for **Tableau** to connect.

## 1. Features

- Fetch markets from:
  - Kalshi (`KALSHI_BASE_URL`, default `https://api.kalshi.com/v1`)
  - Polymarket (`POLYMARKET_BASE_URL`, default `https://clob.polymarket.com`)
- Normalize both feeds into a single table: `prediction_markets`
- Append snapshots with `fetched_at` timestamps
- Run:
  - Locally (`python -m etl.run_etl`)
  - In Docker
  - On a cron via GitHub Actions

## 2. Environment Variables

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

Edit `.env`:

- `DB_URL` – PostgreSQL connection string
  - Example: `postgresql+psycopg2://user:password@host:5432/prediction_data`
- `KALSHI_BASE_URL` – (optional, default: `https://api.kalshi.com/v1`)
- `POLYMARKET_BASE_URL` – (optional, default: `https://clob.polymarket.com`)

If Kalshi requires auth for the endpoints you use, add:

- `KALSHI_API_KEY` or credentials as needed and update `kalshi_client.py`.

## 3. Database Schema

Run the SQL to create the table:

```bash
psql "$DB_URL_NO_DRIVER" -f sql/init_tables.sql
```

Where `DB_URL_NO_DRIVER` is like:
`postgresql://user:password@host:5432/prediction_data`

Table: `prediction_markets`

```sql
CREATE TABLE prediction_markets (
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
```

## 4. Local Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Set env:

```bash
export DB_URL="postgresql+psycopg2://user:pass@localhost:5432/prediction_data"
# optional overrides:
# export KALSHI_BASE_URL="https://api.kalshi.com/v1"
# export POLYMARKET_BASE_URL="https://clob.polymarket.com"
```

Run ETL:

```bash
python -m etl.run_etl
```

## 5. Docker Usage

Build:

```bash
docker build -t prediction-market-etl:latest .
```

Run:

```bash
docker run --rm \
  -e DB_URL="postgresql+psycopg2://user:pass@host.docker.internal:5432/prediction_data" \
  -e KALSHI_BASE_URL="https://api.kalshi.com/v1" \
  -e POLYMARKET_BASE_URL="https://clob.polymarket.com" \
  prediction-market-etl:latest
```

## 6. GitHub Actions (Scheduled ETL)

Configure repo secrets:

- `DB_URL`
- (optional) `KALSHI_BASE_URL`
- (optional) `POLYMARKET_BASE_URL`
- (and any auth values you add later)

The workflow in `.github/workflows/etl.yml` runs every 5 minutes
and on manual dispatch.

## 7. Tableau Connection

In Tableau Desktop / Server:

1. Connect → PostgreSQL
2. Host: your Postgres host (RDS / on-prem / etc.)
3. DB: `prediction_data`
4. Table: `prediction_markets`
5. Recommended: set as an **Extract** and schedule refresh.

Suggested views:

- **Overview:** total markets, by source, by category
- **Interest Rate / Macro:** filtered on categories like "Fed", "CPI", etc.
- **Election / Political:** election-related markets
- **Dislocations:** calculated fields for Kalshi vs Polymarket price differences

## 8. Extending

- Add more fields from Kalshi/Polymarket (orderbook depth, implied prob)
- Add other exchanges
- Add historical backfill scripts
- Implement auth for private/paid endpoints if required
