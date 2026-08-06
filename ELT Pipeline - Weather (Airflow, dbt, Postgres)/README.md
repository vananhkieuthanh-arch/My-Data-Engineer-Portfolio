# Weather-data-ELT

Open-Meteo weather ELT for Vietnam (2023): API extract → landing → Postgres `raw` → dbt staging/marts → Airflow orchestration.

Pairs with the GBIF biodiversity pipeline and the combined Power BI file at repo root: `GBIF_&_Weather.pbix`.

## Stack

Python · Docker Compose · PostgreSQL · dbt · Apache Airflow · Power BI

## Quick start

1. Copy `.env.example` → `.env` and adjust ports if needed  
2. `docker compose up -d`  
3. Init DB/tables: `python src/init_db.py` (and related init scripts)  
4. Extract / load: `python src/weather_raw.py` then `python src/load_raw.py`  
5. dbt: run models under `dbt_project/`  
6. Optional: trigger the Airflow DAG `weather_elt`

Landing files under `data/` are local-only (gitignored).
