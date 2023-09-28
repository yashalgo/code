import pandas as pd
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    String,
    Integer,
    Column,
    DateTime,
    text,
)
from datetime import datetime
from ..common.config import *
from ..exch.exch_utils import *


def replace_data_in_master_table(df, engine):
    # Filter DataFrame to only keep the columns you need

    columns_to_keep = ["SYMBOL", "NAME OF COMPANY", "ISIN NUMBER"]
    df.columns = [col.strip() for col in df.columns]
    df = df[columns_to_keep].copy()

    # Add current timestamp
    current_time = datetime.now()
    df["last_updated"] = current_time

    # Define the table schema
    meta = MetaData()
    nse_master = Table(
        "nse_master",
        meta,
        Column("SYMBOL", String),
        Column("NAME OF COMPANY", String),
        Column("ISIN NUMBER", String),
        Column("last_updated", DateTime),
    )

    # Check if table has today's data
    with engine.connect() as connection:
        if not engine.dialect.has_table(connection, "nse_master"):
            nse_master.create(engine)
        else:
            query = text(
                "SELECT 1 FROM nse_master WHERE DATE(last_updated) = CURRENT_DATE LIMIT 1"
            )
            result = connection.execute(query).fetchone()
            if result:
                print("Data already updated today. Exiting without updating table.")
                return

    # Drop the table if it exists and recreate it
    if "nse_master" in meta.tables:
        nse_master.drop(engine, checkfirst=True)

    nse_master.create(engine)

    # Insert data from the DataFrame into the table
    df.to_sql("nse_master", engine, if_exists="append", index=False)


def main():
    conn_str = "postgresql://postgres:password@localhost:5432/stocks_data"
    engine = create_engine(conn_str)

    df = get_nse_master()
    # print(df.head())
    # return
    replace_data_in_master_table(df, engine)

    engine.dispose()


if __name__ == "__main__":
    main()
