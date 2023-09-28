# %%
import sqlite3
import os
import pandas as pd
from datetime import datetime, timedelta

# Query 1: Top 100 stocks based on M1_Gain
query_1 = """
SELECT * FROM stocks
WHERE Avg_Turnover > 50000000
ORDER BY M1_Gain DESC
LIMIT 100
"""

# Query 2: Top 100 stocks based on M3_Gain
query_2 = """
SELECT * FROM stocks
WHERE Avg_Turnover > 50000000
ORDER BY M3_Gain DESC
LIMIT 100
"""

# Query 3: Top 100 stocks based on M6_Gain
query_3 = """
SELECT * FROM stocks
WHERE Avg_Turnover > 50000000
ORDER BY M6_Gain DESC
LIMIT 100
"""


# get df from sql query
def query_to_df(query, db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(query, conn)
    return df


def calculate_gain(df, period):
    min_last_period = df["LOW"].shift(1).rolling(window=period).min()
    return (df["CLOSE"] / min_last_period - 1) * 100


df = query_to_df("SELECT * FROM stocks", conn)

df["M1_Gain"] = calculate_gain(df, 21)
df["M3_Gain"] = calculate_gain(df, 63)
df["M6_Gain"] = calculate_gain(df, 126)

# Filter stocks with Avg Turnover > 5 Cr
df = df[df["TURNOVER"] > 50000000]

# Sort and limit
top_m1 = df.sort_values(by="M1_Gain", ascending=False).head(100)
top_m3 = df.sort_values(by="M3_Gain", ascending=False).head(100)
top_m6 = df.sort_values(by="M6_Gain", ascending=False).head(100)
