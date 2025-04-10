# database.py
import polars as pl
import sqlite3

def load_csv_to_sqlite(csv_path='trades.csv', db_path='trades.db'):
    df = pl.read_csv(csv_path, try_parse_dates=True)
    df = df.rename({
        'Timestamp': 'timestamp',
        'Symbol': 'symbol',
        'Side': 'side',
        'Quantity': 'quantity',
        'Price': 'price'
    })

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            timestamp TEXT,
            symbol TEXT,
            side TEXT,
            quantity INTEGER,
            price REAL
        )
    ''')
    cursor.executemany('''
        INSERT INTO trades (timestamp, symbol, side, quantity, price)
        VALUES (?, ?, ?, ?, ?)
    ''', df.rows())
    conn.commit()
    conn.close()
    print(f"✅ Data inserted into {db_path}")

if __name__ == '__main__':
    load_csv_to_sqlite()
