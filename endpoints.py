# api.py
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import polars as pl

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Load data once when app starts
def load_trades():
    conn = sqlite3.connect("trades.db")
    df = pl.read_database("SELECT * FROM trades", conn)
    conn.close()

    # Convert to datetime and extract date
    df = df.with_columns(
        pl.col("timestamp").str.strptime(
            pl.Datetime, "%Y-%m-%d %H:%M:%S",
            strict=False).alias("timestamp")
    )
    # optional
    df = df.with_columns(
        pl.col("timestamp").dt.date().alias("date")
    )

    return df


df = load_trades()


# Response models
class SummaryItem(BaseModel):
    symbol: str
    total_volume: int
    total_value: float
    net_position: int


class TrendItem(BaseModel):
    date: str
    avg_price: float
    volume: int


# Summary endpoint
@app.get("/api/summary", response_model=List[SummaryItem])
def get_summary():
    """Returns total volume, value, and net position per stock symbol."""

    # --- Total Volume ---
    volume = df.group_by("symbol").agg(
        pl.col("quantity").sum().alias("total_volume")
    )

    # --- Total Value ---
    price_times_qty = pl.col("quantity") * pl.col("price")
    value = df.group_by("symbol").agg(
        price_times_qty.sum().alias("total_value")
    )

    # --- Buys ---
    df_with_buys = df.with_columns(
        pl.when(pl.col("side") == "BUY")
        .then(pl.col("quantity"))
        .otherwise(0)
        .alias("buy_qty")
    )

    buy_totals = df_with_buys.group_by("symbol").agg(
        pl.col("buy_qty").sum().alias("buy_total")
    )

    # --- Sells ---
    df_with_sells = df.with_columns(
        pl.when(pl.col("side") == "SELL")
        .then(pl.col("quantity"))
        .otherwise(0)
        .alias("sell_qty")
    )

    sell_totals = df_with_sells.group_by("symbol").agg(
        pl.col("sell_qty").sum().alias("sell_total")
    )

    # --- Net Position ---
    position = buy_totals.join(sell_totals, on="symbol")

    position = position.with_columns(
        (pl.col("buy_total") - pl.col("sell_total"))
        .alias("net_position")
    )

    position = position.select(["symbol", "net_position"])

    # --- Final Join ---
    summary = volume.join(value, on="symbol")
    summary = summary.join(position, on="symbol")

    return summary.to_dicts()


# Trend endpoint
@app.get("/api/trend/{symbol}", response_model=List[TrendItem])
def get_trend(symbol: str):
    """Returns daily average price and volume for a given stock symbol."""

    # Filter for this symbol
    symbol_df = df.filter(pl.col("symbol") == symbol)

    if symbol_df.is_empty():
        raise HTTPException(status_code=404, detail="Symbol not found")

    # Group by date
    grouped = symbol_df.group_by("date").agg([
        pl.col("price").mean().alias("avg_price"),
        pl.col("quantity").sum().alias("volume")
    ])

    # Round average price
    grouped = grouped.with_columns(
        pl.col("avg_price").round(2)
    )

    # Convert date to string for JSON
    grouped = grouped.with_columns(
        pl.col("date").cast(str)
    )

    return grouped.to_dicts()


@app.get("/api/get_signs", response_model=List[str])
def get_signs():
    """Returns a list of all unique stock symbols."""
    symbols = df.select("symbol").unique().sort("symbol")
    return symbols["symbol"].to_list()


@app.get("/api/best_symbol")
def get_best_symbol():
    """Returns the symbol with the highest total traded value."""

    df_with_value = df.with_columns(
        (pl.col("quantity") * pl.col("price")).alias("trade_value")
    )

    value_by_symbol = df_with_value.group_by("symbol").agg(
        pl.col("trade_value").sum().alias("total_value")
    )

    sorted_symbols = value_by_symbol.sort("total_value", descending=True)
    best = sorted_symbols[0]

    symbol = best["symbol"].item()
    value = round(best["total_value"].item(), 2)

    return {
        "symbol": symbol,
        "total_value": value
    }


@app.get("/api/most_used")
def get_most_used_symbol():
    """Returns the most frequently traded symbol."""

    usage = df.group_by("symbol").agg(
        pl.count().alias("trade_count")
    )

    sorted_usage = usage.sort("trade_count", descending=True)
    top = sorted_usage[0]

    symbol = top["symbol"].item()
    count = int(top["trade_count"].item())

    return {
        "symbol": symbol,
        "trades": count
    }


@app.get("/api/buy_sell_trend")
def get_buy_sell_trend():
    """Returns daily buy/sell quantity per symbol for charting."""

    # Add 'date' column just to be sure (already should exist)
    trades = df

    # Filter to only needed columns
    trades = trades.select(["symbol", "side", "quantity", "date"])

    # Group by symbol, date, and side (BUY/SELL)
    grouped = trades.group_by(["symbol", "date", "side"]).agg(
        pl.col("quantity").sum().alias("volume")
    )

    # Convert to JSON-compatible format
    grouped = grouped.with_columns(
        pl.col("date").cast(str)
    )

    return grouped.to_dicts()


# -------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home_page.html", {"request": request})
