import csv
from datetime import datetime
from pathlib import Path

DATA_FILE = "data/forex_usdinr.csv"
OUTPUT_FILE = "data/forex_usdinr.svg"

rows = []

with open(DATA_FILE, newline="") as file:
    for row in csv.DictReader(file):
        rows.append((datetime.fromisoformat(row["timestamp"]), float(row["usd_inr"])))

if len(rows) < 2:
    raise SystemExit("Need at least 2 observations. Run forex_history.py first.")

width, height = 1000, 500
left, right, top, bottom = 70, 30, 40, 60
plot_w = width - left - right
plot_h = height - top - bottom

values = [value for _, value in rows]
vmin, vmax = min(values), max(values)

if vmin == vmax:
    vmin -= 0.01
    vmax += 0.01

def x_position(index):
    return left + (index / (len(rows) - 1)) * plot_w

def y_position(value):
    return top + (vmax - value) / (vmax - vmin) * plot_h

points = " ".join(
    f"{x_position(i):.1f},{y_position(value):.1f}"
    for i, (_, value) in enumerate(rows)
)

latest_time, latest_value = rows[-1]

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<text x="{left}" y="25" font-family="sans-serif" font-size="20">USD/INR — Historical Data</text>
<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="black"/>
<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="black"/>
<polyline points="{points}" fill="none" stroke="steelblue" stroke-width="2"/>
<text x="{left}" y="{height-20}" font-family="sans-serif" font-size="12">{rows[0][0].strftime('%H:%M:%S')}</text>
<text x="{width-right-70}" y="{height-20}" font-family="sans-serif" font-size="12">{latest_time.strftime('%H:%M:%S')}</text>
<text x="10" y="{top+5}" font-family="sans-serif" font-size="12">{vmax:.4f}</text>
<text x="10" y="{height-bottom}" font-family="sans-serif" font-size="12">{vmin:.4f}</text>
<text x="{left}" y="{height-5}" font-family="sans-serif" font-size="12">Latest: ₹{latest_value:.4f}</text>
</svg>
"""

Path(OUTPUT_FILE).write_text(svg, encoding="utf-8")
print(f"Saved chart to {OUTPUT_FILE}")
