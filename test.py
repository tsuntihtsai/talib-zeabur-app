import requests

url = "https://tsentih.zeabur.app/indicators"

data = [
  {"date": "2025-09-01", "close": 100},
  {"date": "2025-09-02", "close": 102},
  {"date": "2025-09-03", "close": 101},
  {"date": "2025-09-04", "close": 105},
  {"date": "2025-09-05", "close": 107},
  {"date": "2025-09-06", "close": 106},
  {"date": "2025-09-07", "close": 108},
  {"date": "2025-09-08", "close": 110},
  {"date": "2025-09-09", "close": 109},
  {"date": "2025-09-10", "close": 111}
]

resp = requests.post(url, json=data)
print(resp.json())