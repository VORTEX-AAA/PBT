import csv
import json
import os
import time
from datetime import datetime
from urllib.request import urlopen
from zoneinfo import ZoneInfo

URL = "https://open.er-api.com/v6/latest/USD"
DATA_FILE = "data/forex_usdinr.csv"
chennai = ZoneInfo("Asia/Kolkata")

os.makedirs("data", exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "usd_inr"])

while True:
    try:
        with urlopen(URL, timeout=10) as response:
            data = json.load(response)

        usd_to_inr = data["rates"]["INR"]
        now = datetime.now(chennai)

        with open(DATA_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([now.isoformat(), usd_to_inr])

        print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} | 1 USD = ₹{usd_to_inr:.4f}")

    except Exception as error:
        print("Error:", error)

    time.sleep(10)
