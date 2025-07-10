import requests, pprint

# generate a 24‑char password without symbols
resp = requests.get("http://127.0.0.1:8000/generate",
                    params={"length": 24, "symbols": False})
pprint.pprint(resp.json())

# analyze an arbitrary password
resp = requests.post("http://127.0.0.1:8000/analyze",
                     json={"password": "MyWeakPass123"})
pprint.pprint(resp.json())
