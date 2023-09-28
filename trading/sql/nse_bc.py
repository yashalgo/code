import os
import io
import zipfile
import time
import pandas as pd
import requests
from sqlalchemy import create_engine, sql, text
from ..common.config import *
from ..common.chrome_utils import *
from ..common.indicators import *
from ..exch.exch_utils import *


def mark_bhavcopy_as_processed(conn, date):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO nse_bc_done (date) VALUES (%s)", (date,))
    conn.commit()


def is_bhavcopy_processed(conn, date):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM nse_bc_done WHERE date=%s)",
            (date.strftime("%Y-%m-%d"),),
        )
        return cursor.fetchone()[0]


def get_bc_nse(date, dst_path=nse_bhav_dir):
    date_str = date.strftime("%d%b%Y").upper()
    url = nse_bc_url.format(date_str[5:], date_str[2:5], date_str)

    print(f"Downloading bhavcopy for {date_str}")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content), "r") as z:
            z.extractall(path=dst_path)
    except requests.exceptions.RequestException as e:
        print(f"Request failed. Error: {str(e)}")
    except zipfile.BadZipFile:
        print("Failed to unzip file.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

    time.sleep(1)


def append_to_stock_files_nse(df, date, conn, engine):
    date = date.strftime("%Y-%m-%d")

    # pre-processing
    df = df.drop(columns=["Unnamed: 13"], errors="ignore")  # Add this line
    df = df[
        df["SERIES"].isin(["EQ", "BE"])
    ]  # Keep only rows with EQ, BE in series column
    df = df.drop(
        columns=["PREVCLOSE", "TIMESTAMP", "TOTALTRADES", "ISIN", "LAST"]
    )  # Remove columns
    df = df.rename(
        columns={
            "TOTTRDQTY": "volume",
            "TOTTRDVAL": "turnover",
        }
    )  # Rename columns
    df.columns = map(str.lower, df.columns)
    df["date"] = date

    c = conn.cursor()
    # print("Getting existing symbols...")
    c.execute("SELECT DISTINCT symbol FROM nse_daily WHERE date=%s", (date,))
    existing_symbols = {row[0] for row in c.fetchall()}

    new_rows = []  # List to store the new rows
    for symbol in df["symbol"].unique():
        if symbol in existing_symbols:
            continue

        last_rows = pd.read_sql_query(
            f"SELECT * FROM nse_daily WHERE symbol = '{symbol}' ORDER BY date DESC LIMIT 200",
            engine,
        )

        stock_df = df[df["symbol"] == symbol].copy()
        all_rows = pd.concat([last_rows, stock_df])

        all_rows.at[all_rows.index[-1], "ema_10"] = calculate_ema(all_rows, 10, False)
        all_rows.at[all_rows.index[-1], "ema_20"] = calculate_ema(
            all_rows, 20, uppercase=False
        )
        all_rows.at[all_rows.index[-1], "ema_50"] = calculate_ema(
            all_rows, 50, uppercase=False
        )
        all_rows.at[all_rows.index[-1], "ema_200"] = calculate_ema(
            all_rows, 200, uppercase=False
        )
        all_rows.at[all_rows.index[-1], "adr"] = calculate_adr(
            all_rows, uppercase=False
        )
        all_rows.at[all_rows.index[-1], "atr"] = calculate_atr(
            all_rows, uppercase=False
        )
        all_rows.at[all_rows.index[-1], "avg_turnover"] = calculate_avg_turnover(
            all_rows, 50, uppercase=False
        )
        all_rows.at[all_rows.index[-1], "m1_gain"] = calculate_gain(
            all_rows, 21, uppercase=False
        )
        all_rows.at[all_rows.index[-1], "m3_gain"] = calculate_gain(
            all_rows, 63, uppercase=False
        )
        all_rows.at[all_rows.index[-1], "m6_gain"] = calculate_gain(
            all_rows, 126, uppercase=False
        )
        all_rows.at[
            all_rows.index[-1], "dist_from_52w_high"
        ] = calculate_distance_from_high(all_rows, uppercase=False)
        all_rows.at[
            all_rows.index[-1], "dist_from_52w_low"
        ] = calculate_distance_from_low(all_rows, uppercase=False)

        # Only keep the last row (the new row)
        stock_df = all_rows.iloc[-1:]
        new_rows.append(stock_df)

    if new_rows:
        new_rows_df = pd.concat(new_rows)
        new_rows_df.columns = map(str.lower, new_rows_df.columns)
        new_rows_df.to_sql("nse_daily", engine, if_exists="append", index=False)


def main():
    # Create a SQLite database
    os.chdir(nse_stocks_dir)
    conn_str = "postgresql://postgres:password@localhost:5432/stocks_data"
    # conn = psycopg2.connect(conn_str)
    engine = create_engine(conn_str)
    conn = engine.raw_connection()

    with conn.cursor() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS nse_bc_done (
                date DATE
            )
        """
        )
        # Create a table for each stock
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS public.nse_daily (
                symbol TEXT,
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
                ema_200 NUMERIC(10,2),
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
        s1 = time.time()
        print(trading_day, end=" |")
        file_name = f"cm{trading_day.strftime('%d%b%Y').upper()}bhav.csv"
        bhavcopy_path = os.path.join(nse_bhav_dir, file_name)
        if not os.path.exists(bhavcopy_path):
            get_bc_nse(trading_day)
        if os.path.exists(bhavcopy_path) and not is_bhavcopy_processed(
            conn, trading_day
        ):
            df = pd.read_csv(bhavcopy_path)
            append_to_stock_files_nse(df, trading_day, conn, engine)
            mark_bhavcopy_as_processed(conn, trading_day.strftime("%Y-%m-%d"))

        print(f"Elapsed time: {time.time() - s1}")

    conn.close()
    engine.dispose()


if __name__ == "__main__":
    main()
