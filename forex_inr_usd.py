import json
import time
from datetime import datetime
from urllib.request import urlopen
from zoneinfo import ZoneInfo

URL = "https://open.er-api.com/v6/latest/USD"
chennai = ZoneInfo("Asia/Kolkata")

while True:
    try:
        with urlopen(URL, timeout=10) as response:
            data = json.load(response)

        usd_to_inr = data["rates"]["INR"]
        now = datetime.now(chennai)

        print()
        print("🇮🇳 INR / USD FOREX")
        print("------------------")
        print("Time:", now.strftime("%Y-%m-%d %H:%M:%S"))
        print(f"1 USD = ₹{usd_to_inr:.2f}")
        print(f"1 INR = ${1 / usd_to_inr:.6f}")
        print(f"Rate source: {data.get('provider', 'API')}")
        print("Next update in 10 seconds...")

    except Exception as error:
        print("Error:", error)
        print("Retrying in 10 seconds...")

    time.sleep(10)
