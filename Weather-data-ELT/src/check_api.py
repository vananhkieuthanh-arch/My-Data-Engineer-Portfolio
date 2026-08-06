import requests
import json

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 16.1667,
	"longitude": 107.8333,
	"start_date": "2023-01-01",
	"end_date": "2023-12-31",
	"daily": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
	"timezone": "Asia/Bangkok",
}
res = requests.get(url, params=params).json()
print(json.dumps(res))