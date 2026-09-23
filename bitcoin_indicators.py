import time
from pathlib import Path

import pandas as pd

PRICE_FILE = Path("bitcoin_usd_live.csv")
INDICATOR_FILE = Path("bitcoin_technical_indicators.csv")
INTERVAL = 30  # seconds


def calculate_indicators(df):
    df = df.copy()

    df["sma_10"] = df["bitcoin_usd"].rolling(window=10).mean()
    df["sma_20"] = df["bitcoin_usd"].rolling(window=20).mean()
    df["sma_50"] = df["bitcoin_usd"].rolling(window=50).mean()

    df["ema_10"] = df["bitcoin_usd"].ewm(span=10, adjust=False).mean()
    df["ema_20"] = df["bitcoin_usd"].ewm(span=20, adjust=False).mean()

    delta = df["bitcoin_usd"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    df["rsi_14"] = 100 - (100 / (1 + rs))

    ema_12 = df["bitcoin_usd"].ewm(span=12, adjust=False).mean()
    ema_26 = df["bitcoin_usd"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema_12 - ema_26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_histogram"] = df["macd"] - df["macd_signal"]

    rolling_20 = df["bitcoin_usd"].rolling(window=20)
    df["bb_middle"] = rolling_20.mean()
    bb_std = rolling_20.std()
    df["bb_upper"] = df["bb_middle"] + (2 * bb_std)
    df["bb_lower"] = df["bb_middle"] - (2 * bb_std)

    df["roc_10"] = df["bitcoin_usd"].pct_change(periods=10) * 100

    return df


def update_indicators():
    if not PRICE_FILE.exists():
        print(f"Waiting for {PRICE_FILE}...")
        return

    df = pd.read_csv(PRICE_FILE)

    if df.empty:
        return

    df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True)
    df["bitcoin_usd"] = pd.to_numeric(df["bitcoin_usd"], errors="coerce")
    df = df.dropna(subset=["timestamp_utc", "bitcoin_usd"])

    result = calculate_indicators(df)
    result.to_csv(INDICATOR_FILE, index=False)

    latest = result.iloc[-1]
    print(
        f"{latest['timestamp_utc']} | "
        f"BTC={latest['bitcoin_usd']:,.2f} | "
        f"SMA20={latest['sma_20']:,.2f} | "
        f"EMA20={latest['ema_20']:,.2f} | "
        f"RSI14={latest['rsi_14']:.2f}"
    )


print("Bitcoin technical-indicator module started.")
print(f"Reading: {PRICE_FILE.resolve()}")
print(f"Writing: {INDICATOR_FILE.resolve()}")
print("Press Ctrl+C to stop.\n")

while True:
    try:
        update_indicators()
    except (OSError, ValueError, pd.errors.ParserError) as error:
        print(f"Data error: {error}")
    except Exception as error:
        print(f"Error: {error}")

    time.sleep(INTERVAL)
