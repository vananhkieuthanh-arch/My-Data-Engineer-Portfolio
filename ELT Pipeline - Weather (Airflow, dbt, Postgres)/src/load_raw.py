import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path 
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

LANDING = ROOT / "data" / "landing" / "weather"
API_FILE = "api_response.json"
DAILY_FILE = "weather_daily.json"

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "dbname": os.getenv("POSTGRES_DB"),
    "port": os.getenv("POSTGRES_PORT", "5433"),
}

INSERT_API_RESPONSE_SQL = """ 
INSERT INTO raw.weather_api_response (
    country_code, start_date, end_date, response_lat, response_long, 
    elevation_m, time_zone, payload, extracted_at, status, ingested_at
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s
) 
ON CONFLICT (country_code, start_date, end_date) DO UPDATE SET
    response_lat = EXCLUDED.response_lat,
    response_long = EXCLUDED.response_long,
    elevation_m = EXCLUDED.elevation_m,
    time_zone = EXCLUDED.time_zone,
    payload = EXCLUDED.payload,
    extracted_at = EXCLUDED.extracted_at,
    status = EXCLUDED.status,
    ingested_at = EXCLUDED.ingested_at;
"""

INSERT_DAILY_SQL = """ 
INSERT INTO raw.weather_daily (
    country_code, observation_date, response_lat, response_long, elevation_m,
    temp_mean_c, temp_max_c, temp_min_c, precip_mm, time_zone
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (country_code, observation_date) DO UPDATE SET
    response_lat = EXCLUDED.response_lat,
    response_long = EXCLUDED.response_long,
    elevation_m = EXCLUDED.elevation_m,
    temp_mean_c = EXCLUDED.temp_mean_c,
    temp_max_c = EXCLUDED.temp_max_c,
    temp_min_c = EXCLUDED.temp_min_c,
    precip_mm = EXCLUDED.precip_mm,
    time_zone = EXCLUDED.time_zone,
    extracted_at = now();
"""

# Locate latest dir
def latest_landing_dir() -> Path:
    dirs = sorted(LANDING.glob("dt=*"))
    if not dirs:
        raise SystemExit("No landing directory found under {LANDING}. Run weather_raw.py first.")
    return dirs[-1]   # return newest landing dirs

def load_all() -> int:
    out = latest_landing_dir()
    api_path = out / API_FILE
    api_data = api_path.read_text(encoding="utf-8")
    daily_path = out / DAILY_FILE
    daily_data = daily_path.read_text(encoding="utf-8")
    ingested_at = datetime.now(timezone.utc)

    api_meta = json.loads(api_data)
    daily_rows = json.loads(daily_data)

    # payload may be a dict (preferred) or a JSON string — always pass text for %s::jsonb
    payload = api_meta["payload"]
    if not isinstance(payload, str):
        payload = json.dumps(payload)

    api_values = (
        api_meta["country_code"], 
        api_meta["start_date"], 
        api_meta["end_date"], 
        api_meta["response_lat"], 
        api_meta["response_long"], 
        api_meta["elevation_m"], 
        api_meta["time_zone"],
        payload,
        api_meta["extracted_at"],
        api_meta["status"],
        ingested_at,
    )

    # Daily requires for loop
    daily_values = [
        (
            row["country_code"],
            row["observation_date"],
            row["response_lat"],
            row["response_long"],
            row["elevation_m"],
            row["temp_mean_c"],
            row["temp_max_c"],
            row["temp_min_c"],
            row["precip_mm"],
            row["time_zone"],
        )
        for row in daily_rows
    ]

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(INSERT_API_RESPONSE_SQL, api_values)
            cur.executemany(INSERT_DAILY_SQL, daily_values)
        conn.commit()
    
    return len(daily_values)

if __name__ == "__main__":
    n = load_all()
    print(f"Loaded {n} daily rows into Postgres from {latest_landing_dir()}.")