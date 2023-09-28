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


def replace_data_in_table(df, engine):
    columns_to_keep = [
        "Symbol",
        "CompanyName",
        "MarketCapital",
        "Industry Group",
        "TV_TICKER",
    ]
    df.columns = [col.strip() for col in df.columns]
    df = df[columns_to_keep].copy()

    current_time = datetime.now()
    df["last_updated"] = current_time

    # Define the table schema
    meta = MetaData()
    msi_ind_grp = Table(
        "msi_ind_grp",
        meta,
        Column("Symbol", String),
        Column("CompanyName", String),
        Column("MarketCapital", String),
        Column("Industry Group", String),
        Column("TV_TICKER", String),
        Column("last_updated", DateTime),
    )

    with engine.connect() as connection:
        if not engine.dialect.has_table(connection, "msi_ind_grp"):
            msi_ind_grp.create(engine)
        else:
            query = text(
                "SELECT 1 FROM msi_ind_grp WHERE DATE(last_updated) = CURRENT_DATE LIMIT 1"
            )
            result = connection.execute(query).fetchone()
            if result:
                print("Data already updated today. Exiting without updating table.")
                return

    # Drop the table if it exists and recreate it
    if "msi_ind_grp" in meta.tables:
        msi_ind_grp.drop(engine, checkfirst=True)

    msi_ind_grp.create(engine)

    # Insert data from the DataFrame into the table
    df.to_sql("msi_ind_grp", engine, if_exists="append", index=False)


def main():
    conn_str = "postgresql://postgres:password@localhost:5432/stocks_data"
    engine = create_engine(conn_str)

    # Load the MSI IND GRP master data from the CSV
    try:
        df = pd.read_csv(msi_ind_grp_csv, index_col=False)
        # print(df.head())
    except FileNotFoundError:
        raise ValueError(
            "The specified BSE master CSV file was not found. Please ensure the path is correct."
        )
    replace_data_in_table(df, engine)

    engine.dispose()


if __name__ == "__main__":
    main()
