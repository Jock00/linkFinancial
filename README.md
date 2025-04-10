# 📊 Trade Dashboard (FastAPI + Polars + Chart.js)

A simple trade analysis dashboard built with **FastAPI**, **Polars**, and **Chart.js**.

This project loads trade data from a CSV file, stores it in a SQLite database, exposes APIs for analytics, and displays the data using interactive charts.

---

## 🚀 Features

- ✅ Load CSV into SQLite using Polars
- ✅ FastAPI backend with multiple endpoints
- ✅ Chart.js frontend with:
  - Volume by symbol
  - Buy/Sell trends over time (colored lines)
- ✅ Endpoints for:
  - Summary data
  - Trend per symbol
  - Most used symbol
  - Best symbol by traded value
  - Trades per day

---

## 🧱 Project Structure

```
.
├── analysis.py    # data analysis
├── endpoints.py                # FastAPI backend
├── generate_data.py      # Generate trades.csv
├── database.py     # Load CSV into SQLite
├── templates/
│   └── index.html        # Dashboard HTML
├── static/
│   └── chart.js          # Chart logic (Chart.js)
└── trades.db             # SQLite database (created after loading)
```

---

## ⚙️ Setup & Run

### 1. Install dependencies

```bash
pip install fastapi uvicorn polars jinja2
```

### 2. Generate trade data

```bash
python generate_data.py
```

### 3. Load data into SQLite

```bash
python database.py
```
extra ->
```bash
python analysis.py
```

### 4. Run the FastAPI server

```bash
uvicorn endpoints:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## 🌐 Available Endpoints

| Route                       | Description                           |
|----------------------------|---------------------------------------|
| `/api/summary`             | Volume, value, and position per symbol |
| `/api/trend/{symbol}`      | Daily trend (price/volume) for symbol |
| `/api/best_symbol`         | Symbol with highest traded value      |
| `/api/most_used`           | Most frequently traded symbol         |
| `/api/trades_per_day`      | Count of trades by day                |
| `/api/get_signs`           | List of all traded symbols            |
| `/api/buy_sell_trend`      | Daily buy/sell volume per symbol      |
| `/api/summary_and_trend`   | Combined data for dashboard           |

---

## 📈 Frontend Preview

![screenshot](preview.png)

> Uses Chart.js to render interactive charts for summary and trends.

---

## 📌 Notes

- This is a self-contained demo. You can adjust `generate_data.py` to simulate different trading patterns.
- Easily extendable with filters, authentication, or export options.

---

## 🧑‍💻 Created by

Alexandru Bucurie  


