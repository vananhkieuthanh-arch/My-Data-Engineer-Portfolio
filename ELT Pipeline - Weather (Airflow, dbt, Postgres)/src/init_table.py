
# Daily weather data table
SQL = """CREATE TABLE IF NOT EXISTS raw.weather_daily(
    country_code        TEXT NOT NULL,
    observation_date    DATE NOT NULL,
    response_lat        DOUBLE PRECISION,
    response_long       DOUBLE PRECISION,
    elevation_m         DOUBLE PRECISION,
    temp_mean_c         DOUBLE PRECISION,
    temp_max_c          DOUBLE PRECISION,
    temp_min_c          DOUBLE PRECISION,
    precip_mm           DOUBLE PRECISION,
    time_zone           TEXT,
    extracted_at        TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (country_code, observation_date)
);

# API metadata table. 1 row per extracted API response
CREATE TABLE IF NOT EXISTS raw.weather_api_response(
    country_code        TEXT NOT NULL,
    start_date          DATE NOT NULL,
    end_date            DATE NOT NULL,
    response_lat        DOUBLE PRECISION,
    response_long       DOUBLE PRECISION,
    elevation_m         DOUBLE PRECISION,
    time_zone           TEXT,
    payload             JSONB,
    extracted_at        TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (country_code, start_date, end_date)
);"""

ALTER TABLE raw.weather_api_response
  ADD COLUMN IF NOT EXISTS status TEXT,
  ADD COLUMN IF NOT EXISTS ingested_at TIMESTAMPTZ;