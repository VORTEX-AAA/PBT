import requests
import csv
import time
from datetime import datetime, timezone
from pathlib import Path

CSV_FILE = Path("bitcoin_usd_live.csv")
INTERVAL = 30  # seconds


def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    return float(data["bitcoin"]["usd"])


def save_price(timestamp, price):
    file_exists = CSV_FILE.exists()

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["timestamp_utc", "bitcoin_usd"])

        writer.writerow([timestamp, price])


print("Bitcoin BTC/USD live collector started.")
print(f"Saving data to: {CSV_FILE.resolve()}")
print("Interval: 30 seconds")
print("Press Ctrl+C to stop.\n")


while True:
    try:
        price = get_bitcoin_price()
        timestamp = datetime.now(timezone.utc).isoformat()

        save_price(timestamp, price)

        print(f"{timestamp} | BTC/USD = ${price:,.2f}")

    except requests.RequestException as error:
        print(f"API error: {error}")

    except Exception as error:
        print(f"Error: {error}")

    time.sleep(INTERVAL)
