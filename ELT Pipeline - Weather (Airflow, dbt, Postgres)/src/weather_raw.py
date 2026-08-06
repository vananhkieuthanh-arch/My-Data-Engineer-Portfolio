import requests
import json
from typing import Tuple
from datetime import date, datetime
from pathlib import Path 

url = "https://archive-api.open-meteo.com/v1/archive"
API_FILE = "api_response.json"
DAILY_FILE = "weather_daily.json"

def get_weather_data():
    params = {
        "latitude": 16.1667,
        "longitude": 107.8333,
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "daily": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": "Asia/Bangkok",
    }

    res = requests.get(url, params=params).json()

    return res

def format_api_response(res):
    ok = "daily" in res and res["daily"].get("time")
    extracted_at = datetime.now().isoformat()
    return {
        "country_code": "VN",
        "start_date": res['daily']['time'][0],
        "end_date": res['daily']['time'][-1],
        "response_lat": res['latitude'],
        "response_long": res['longitude'], 
        "elevation_m": res['elevation'],
        "time_zone": res['timezone'],
        "payload": res,
        "status": "ok" if ok else "failed",
        "extracted_at": extracted_at
    }

def format_daily_rows(res):
    daily = res["daily"]
    extracted_at = datetime.now().isoformat()
    rows = []
    for i, date in enumerate(daily['time']):
        rows.append({
            "country_code": "VN",
            "observation_date": date,
            "response_lat": res['latitude'],
            "response_long": res['longitude'],
            "elevation_m": res['elevation'],
            "temp_mean_c": daily['temperature_2m_mean'][i],
            "temp_max_c": daily['temperature_2m_max'][i],
            "temp_min_c": daily['temperature_2m_min'][i],
            "precip_mm": daily['precipitation_sum'][i],
            "time_zone": res['timezone'],
            "extracted_at": extracted_at
        })
    return rows
    
# Set data landing ROOT
ROOT = Path(__file__).resolve().parents[1]

def landing_dir() -> Path:
    d = ROOT / "data" / "landing" / "weather" / f"dt={date.today().isoformat()}" 
    d.mkdir(parents=True, exist_ok=True)
    return d

# Save files to landing directory
def save_landing(api_meta: dict, daily_rows: list) -> Tuple[Path, Path]:
    out = landing_dir()
    api_path = out / API_FILE
    daily_path = out / DAILY_FILE

    api_path.write_text(json.dumps(api_meta, indent=2), encoding="utf-8")
    daily_path.write_text(json.dumps(daily_rows, indent=2), encoding="utf-8")
    return api_path, daily_path

if __name__ == "__main__":
    res = get_weather_data()
    api_meta = format_api_response(res)
    daily_rows = format_daily_rows(res)
    api_path, daily_path = save_landing(api_meta, daily_rows)
    print(f"Saved {api_path}")
    print(f"Saved {daily_path} with {len(daily_rows)} rows")