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


def replace_data_in_bands_table(df, engine):
    # Filter DataFrame to only the columns you need
    columns_to_keep = ["Symbol", "Series", "Security Name", "Band", "Remarks"]
    df = df[columns_to_keep]

    # Add current timestamp
    current_time = datetime.now()
    df["last_updated"] = current_time

    # Define the table schema
    meta = MetaData()
    nse_bands = Table(
        "nse_bands",
        meta,
        Column("Symbol", String),
        Column("Series", String),
        Column("Security Name", String),
        Column("Band", String),
        Column("Remarks", String),
        Column("last_updated", DateTime),
    )

    # Check if table has today's data
    with engine.connect() as connection:
        if not engine.dialect.has_table(connection, "nse_bands"):
            nse_bands.create(engine)
        else:
            query = text(
                "SELECT 1 FROM nse_bands WHERE DATE(last_updated) = CURRENT_DATE LIMIT 1"
            )
            result = connection.execute(query).fetchone()
            if result:
                print("Data already updated today. Exiting without updating table.")
                return

    # Drop the table if it exists and recreate it
    if "nse_bands" in meta.tables:
        nse_bands.drop(engine, checkfirst=True)

    nse_bands.create(engine)

    # Insert data from the DataFrame into the table
    df.to_sql("nse_bands", engine, if_exists="append", index=False)


def main():
    conn_str = "postgresql://postgres:password@localhost:5432/stocks_data"
    engine = create_engine(conn_str)

    df = get_csv(nse_bands_url, nse_bands_csv)
    # print(df.head())
    replace_data_in_bands_table(df, engine)

    engine.dispose()


if __name__ == "__main__":
    main()
