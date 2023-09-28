import pandas as pd
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    String,
    Column,
    DateTime,
    text,
)
from datetime import datetime

# Note: Ensure the paths in the imports below are correct based on your project structure
from ..common.config import *
from ..exch.exch_utils import *


def replace_data_in_master_table(df, engine):
    # Filter DataFrame to only keep the columns you need
    columns_to_keep = [
        "Security Code",
        "Issuer Name",
        "Security Id",
        "Security Name",
        "Status",
        "Group",
        "ISIN No",
        "Industry",
        "Instrument",
        "Sector Name",
        "Industry New Name",
        "Igroup Name",
        "ISubgroup Name",
    ]
    df.columns = [col.strip() for col in df.columns]
    df = df[columns_to_keep].copy()

    # Add current timestamp
    current_time = datetime.now()
    df["last_updated"] = current_time

    # Define the table schema
    meta = MetaData()
    bse_master = Table(
        "bse_master",
        meta,
        Column("Security Code", String),
        Column("Issuer Name", String),
        Column("Security Id", String),
        Column("Security Name", String),
        Column("Status", String),
        Column("Group", String),
        Column("ISIN No", String),
        Column("Industry", String),
        Column("Instrument", String),
        Column("Sector Name", String),
        Column("Industry New Name", String),
        Column("Igroup Name", String),
        Column("ISubgroup Name", String),
        Column("last_updated", DateTime),
    )

    # Check if table has today's data
    with engine.connect() as connection:
        if not engine.dialect.has_table(connection, "bse_master"):
            bse_master.create(engine)
        else:
            query = text(
                "SELECT 1 FROM bse_master WHERE DATE(last_updated) = CURRENT_DATE LIMIT 1"
            )
            result = connection.execute(query).fetchone()
            if result:
                print("Data already updated today. Exiting without updating table.")
                return

    # Drop the table if it exists and recreate it
    if "bse_master" in meta.tables:
        bse_master.drop(engine, checkfirst=True)

    bse_master.create(engine)

    # Insert data from the DataFrame into the table
    df.to_sql("bse_master", engine, if_exists="append", index=False)


def main():
    conn_str = "postgresql://postgres:password@localhost:5432/stocks_data"
    engine = create_engine(conn_str)

    # Attempt to load the BSE master data from the CSV
    try:
        df = pd.read_csv(bse_master_csv, index_col=False)
        # print(df.head())
    except FileNotFoundError:
        raise ValueError(
            "The specified BSE master CSV file was not found. Please ensure the path is correct."
        )

    replace_data_in_master_table(df, engine)

    engine.dispose()


if __name__ == "__main__":
    main()
