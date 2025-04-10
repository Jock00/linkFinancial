# analysis.py

import sqlite3
import polars as pl

# Step 1: Load data
conn = sqlite3.connect("trades.db")
df = pl.read_database("SELECT * FROM trades", conn)
conn.close()

# Step 2: Parse timestamp column
df = df.with_columns(
    pl.col("timestamp").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False)
)

# Step 3: Extract date column
df = df.with_columns(
    pl.col("timestamp").dt.date().alias("date")
)

# --- SUMMARY ---

# Step 4: Group by symbol for volume
grouped_volume = df.group_by("symbol").agg(
    pl.col("quantity").sum().alias("total_volume")
)

# Step 5: Group by symbol for total value
quantity_times_price = pl.col("quantity") * pl.col("price")
grouped_value = df.group_by("symbol").agg(
    quantity_times_price.sum().alias("total_value")
)

# Step 6: Calculate net position (buys - sells)
buy_sell_diff = pl.when(pl.col("side") == "BUY").then(pl.col("quantity")).otherwise(-pl.col("quantity"))
grouped_position = df.group_by("symbol").agg(
    buy_sell_diff.sum().alias("net_position")
)

# Step 7: Join everything together
summary = grouped_volume.join(grouped_value, on="symbol").join(grouped_position, on="symbol")

# Step 8: Show result
print("Summary per stock:")
print(summary)

# --- BUSIEST OVERALL DAY ---

# Step 9: Group by date
daily_volume = df.group_by("date").agg(
    pl.col("quantity").sum().alias("volume")
)

# Step 10: Sort to find busiest
busiest_overall = daily_volume.sort("volume", descending=True).head(1)

print("\nBusiest trading day overall:")
print(busiest_overall)

# --- BUSIEST DAY PER STOCK ---

# Step 11: Volume per stock per day
volume_per_day = df.group_by(["symbol", "date"]).agg(
    pl.col("quantity").sum().alias("volume")
)

# Step 12: Sort within each symbol
sorted_days = volume_per_day.sort(["symbol", "volume"], descending=[False, True])

# Step 13: Pick top day per stock
busiest_per_symbol = sorted_days.group_by("symbol").first()

print("\nBusiest day per stock:")
print(busiest_per_symbol)
