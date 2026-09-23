import requests
import csv
import time
from datetime import datetime, timezone
from pathlib import Path

CSV_FILE = Path("bitcoin_usd_live.csv")
INTERVAL = 10  # seconds


def get_bitcoin_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    return float(data["bpi"]["USD"]["rate"].replace(",", ""))


def save_price(timestamp, price):
    file_exists = CSV_FILE.exists()

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["timestamp_utc", "bitcoin_usd"])

        writer.writerow([timestamp, price])


print("Bitcoin live price collector started.")
print(f"Saving to: {CSV_FILE.resolve()}")
print("Press Ctrl+C to stop.\n")

while True:
    try:
        price = get_bitcoin_price()
        timestamp = datetime.now(timezone.utc).isoformat()

        save_price(timestamp, price)

        print(f"{timestamp} | BTC/USD = ${price:,.2f}")

    except requests.RequestException as e:
        print(f"API error: {e}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(INTERVAL)
