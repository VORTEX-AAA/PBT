import json
from urllib.request import urlopen

url = "https://open.er-api.com/v6/latest/USD"

with urlopen(url, timeout=10) as response:
    data = json.load(response)

usd_to_inr = data["rates"]["INR"]

print("🇮🇳 INR / USD FOREX")
print("------------------")
print(f"1 USD = ₹{usd_to_inr:.2f}")
print(f"1 INR = ${1 / usd_to_inr:.6f}")
print(f"Rate source: {data.get('provider', 'API')}")
