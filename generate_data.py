# generate_data.py
import csv
import random
from datetime import datetime, timedelta

SYMBOLS = ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA", "NVDA", "META"]
SIDES = ["BUY", "SELL"]
START_DATE = datetime(2024, 1, 1)
DAYS = 45
TRADES_PER_DAY = 200

def random_time():
    start = datetime.strptime("09:30", "%H:%M")
    end = datetime.strptime("16:00", "%H:%M")
    delta = end - start
    rand_minutes = random.randint(0, int(delta.total_seconds() / 60))
    return start + timedelta(minutes=rand_minutes)

def generate_trades():
    trades = []
    for i in range(DAYS):
        day = START_DATE + timedelta(days=i)
        if day.weekday() >= 5:  # Skip weekends
            continue
        for _ in range(TRADES_PER_DAY):
            timestamp = datetime.combine(day, random_time().time())
            symbol = random.choice(SYMBOLS)
            side = random.choice(SIDES)
            quantity = random.randint(10, 1000)
            price = round(random.uniform(50, 500), 2)
            trades.append([timestamp.strftime("%Y-%m-%d %H:%M:%S"), symbol, side, quantity, price])
    return trades

def save_csv(filename="trades.csv"):
    trades = generate_trades()
    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Symbol", "Side", "Quantity", "Price"])
        writer.writerows(trades)
    print(f"✅ Generated {len(trades)} trades into {filename}")

if __name__ == "__main__":
    save_csv()
