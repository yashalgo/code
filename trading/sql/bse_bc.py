import os
import io
import zipfile
import time
import pandas as pd
import psycopg2
import requests
from sqlalchemy import create_engine, sql, text
from ..common.config import *
from ..common.chrome_utils import *
from ..common.indicators import *
from ..exch.exch_utils import *


def mark_bhavcopy_as_processed(conn, date):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO bse_bc_done (date) VALUES (%s)", (date,))
    # print(f'Marked bhavcopy for date "{date}" as processed')
    conn.commit()  # commit the transaction


def is_bhavcopy_processed(conn, date):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM bse_bc_done WHERE date=%s)",
            (date.strftime("%Y-%m-%d"),),
        )
        return cursor.fetchone()[0]


def get_bc_bse(date, dst_path=bse_bhav_dir):
    date_str = date.strftime("%d%m%y").upper()
    url = bse_bc_url.format(date_str)

    print(f"Downloading bhavcopy for {date_str}")
    try:
        response = request_url(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request to {url} failed. Error: {e}")
        return
    with zipfile.ZipFile(io.BytesIO(response.content), "r") as zip_file:
        zip_file.extractall(path=dst_path)


def append_to_stock_files_bse(df, date, conn, engine):
    date = date.strftime("%Y-%m-%d")

    # pre-processing
    df = df.drop(columns=["Unnamed: 13"], errors="ignore")
    df = df[df["SC_GROUP"].isin(["A ", "B ", "T ", "X", "XT"])]
    df = df.drop(columns=["PREVCLOSE", "NO_TRADES", "TDCLOINDI", "SC_TYPE", "LAST"])
    df = df.rename(
        columns={
            "SC_CODE": "code",
            "SC_NAME": "name",
            "NO_OF_SHRS": "volume",
            "NET_TURNOV": "turnover",
            "SC_GROUP": "series",
        }
    )
    df.columns = map(str.lower, df.columns)

    df["date"] = date

    c = conn.cursor()
    c.execute("SELECT DISTINCT name FROM bse_daily WHERE date=%s", (date,))

    existing_symbols = {row[0] for row in c.fetchall()}
    s2 = set(df["name"].unique())
    # print(len(existing_symbols), len(s2), end=" | ")
    new_rows = []
    # print(existing_symbols == s2)
    for symbol in s2:
        # print(symbol)
        if symbol in existing_symbols:
            # print(f"Skipping {symbol} as it already exists in the database")
            continue
        ###
        symbol_escaped = symbol.replace("'", "''")
        last_rows = pd.read_sql_query(
            f"SELECT * FROM bse_daily WHERE name = '{symbol_escaped}' ORDER BY date DESC LIMIT 200",
            engine,
        )

        stock_df = df[df["name"] == symbol].copy()
        print(type(stock_df), stock_df)
        all_rows = pd.concat([last_rows, stock_df])
        # print(all_rows)
        all_rows["ema_10"] = calculate_ema(all_rows, 10, False)
        all_rows["ema_20"] = calculate_ema(all_rows, 20, uppercase=False)
        all_rows["ema_50"] = calculate_ema(all_rows, 50, uppercase=False)
        all_rows["ema_200"] = calculate_ema(all_rows, 200, uppercase=False)
        all_rows["adr"] = calculate_adr(all_rows, uppercase=False)
        all_rows["atr"] = calculate_atr(all_rows, uppercase=False)
        all_rows["avg_turnover"] = calculate_avg_turnover(all_rows, 50, uppercase=False)
        all_rows["m1_gain"] = calculate_gain(all_rows, 21, uppercase=False)
        all_rows["m3_gain"] = calculate_gain(all_rows, 63, uppercase=False)
        all_rows["m6_gain"] = calculate_gain(all_rows, 126, uppercase=False)
        all_rows["dist_from_52w_high"] = calculate_distance_from_high(
            all_rows, uppercase=False
        )
        all_rows["dist_from_52w_low"] = calculate_distance_from_low(
            all_rows, uppercase=False
        )

        # Only keep the last row (the new row)
        stock_df = all_rows.iloc[-1:]
        new_rows.append(stock_df)

    if new_rows:
        new_rows_df = pd.concat(new_rows)
        new_rows_df.columns = map(str.lower, new_rows_df.columns)
        new_rows_df.to_sql("bse_daily", engine, if_exists="append", index=False)


def main():
    os.chdir(bse_stocks_dir)
    conn_str = "postgresql://postgres:password@localhost:5432/stocks_data"
    # conn = psycopg2.connect(conn_str)
    engine = create_engine(conn_str)
    conn = engine.raw_connection()

    with conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS bse_bc_done (date DATE PRIMARY KEY)")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bse_daily (
            code TEXT,
            name TEXT,
            series TEXT,
            open NUMERIC(10,2),
            high NUMERIC(10,2),
            low NUMERIC(10,2),
            close NUMERIC(10,2),
            volume INTEGER,
            turnover REAL,
            date DATE,
            ema_10 NUMERIC(10,2),
            ema_20 NUMERIC(10,2),
            ema_50 NUMERIC(10,2),
            ema_200 REAL,
            adr NUMERIC(10,2),
            atr NUMERIC(10,2),
            avg_turnover REAL,
            m1_gain NUMERIC(10,2),
            m3_gain NUMERIC(10,2),
            m6_gain NUMERIC(10,2),
            dist_from_52w_high NUMERIC(10,2),
            dist_from_52w_low NUMERIC(10,2)
            )
            """
        )
    conn.commit()

    trading_days = get_bse_trading_days()
    for trading_day in trading_days:
        start = time.time()
        print(trading_day, end=" | ")
        file_name = f"EQ{trading_day.strftime('%d%m%y').upper()}.CSV"
        bhavcopy_path = os.path.join(bse_bhav_dir, file_name)
        if not os.path.exists(bhavcopy_path):
            get_bc_bse(trading_day)
        if os.path.exists(bhavcopy_path) and not is_bhavcopy_processed(
            conn, trading_day
        ):
            df = pd.read_csv(bhavcopy_path)
            append_to_stock_files_bse(df, trading_day, conn, engine)
            mark_bhavcopy_as_processed(conn, trading_day.strftime("%Y-%m-%d"))
        print(f"Elapsed time: {time.time() - start}")

    conn.close()
    engine.dispose()


if __name__ == "__main__":
    main()
