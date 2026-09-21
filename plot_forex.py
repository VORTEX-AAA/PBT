import csv
import time
from datetime import datetime
from pathlib import Path

DATA_FILE = "data/forex_usdinr.csv"
OUTPUT_FILE = "data/forex_usdinr.svg"

WIDTH, HEIGHT = 1000, 500
LEFT, RIGHT, TOP, BOTTOM = 70, 30, 40, 60


def generate_chart():
    rows = []

    with open(DATA_FILE, newline="") as file:
        for row in csv.DictReader(file):
            rows.append(
                (datetime.fromisoformat(row["timestamp"]), float(row["usd_inr"]))
            )

    if len(rows) < 2:
        print("Need at least 2 observations. Waiting for more data...")
        return

    plot_w = WIDTH - LEFT - RIGHT
    plot_h = HEIGHT - TOP - BOTTOM

    values = [value for _, value in rows]
    vmin, vmax = min(values), max(values)

    if vmin == vmax:
        vmin -= 0.01
        vmax += 0.01

    def x_position(index):
        return LEFT + (index / (len(rows) - 1)) * plot_w

    def y_position(value):
        return TOP + (vmax - value) / (vmax - vmin) * plot_h

    points = " ".join(
        f"{x_position(i):.1f},{y_position(value):.1f}"
        for i, (_, value) in enumerate(rows)
    )

    latest_time, latest_value = rows[-1]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<rect width="100%" height="100%" fill="white"/>
<text x="{LEFT}" y="25" font-family="sans-serif" font-size="20">USD/INR — Live Historical Data</text>
<line x1="{LEFT}" y1="{TOP}" x2="{LEFT}" y2="{HEIGHT-BOTTOM}" stroke="black"/>
<line x1="{LEFT}" y1="{HEIGHT-BOTTOM}" x2="{WIDTH-RIGHT}" y2="{HEIGHT-BOTTOM}" stroke="black"/>
<polyline points="{points}" fill="none" stroke="steelblue" stroke-width="2"/>
<text x="{LEFT}" y="{HEIGHT-20}" font-family="sans-serif" font-size="12">{rows[0][0].strftime('%H:%M:%S')}</text>
<text x="{WIDTH-RIGHT-70}" y="{HEIGHT-20}" font-family="sans-serif" font-size="12">{latest_time.strftime('%H:%M:%S')}</text>
<text x="10" y="{TOP+5}" font-family="sans-serif" font-size="12">{vmax:.4f}</text>
<text x="10" y="{HEIGHT-BOTTOM}" font-family="sans-serif" font-size="12">{vmin:.4f}</text>
<text x="{LEFT}" y="{HEIGHT-5}" font-family="sans-serif" font-size="12">Latest: ₹{latest_value:.4f} | Points: {len(rows)}</text>
</svg>
"""

    Path(OUTPUT_FILE).write_text(svg, encoding="utf-8")
    print(f"Chart updated | {latest_time.strftime('%H:%M:%S')} | Points: {len(rows)}")


while True:
    try:
        generate_chart()
    except Exception as error:
        print("Chart error:", error)

    time.sleep(10)
