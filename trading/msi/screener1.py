import pandas as pd
from ..common.config import *
from ..common.tv_utils import *


def get_top_n_percent_stocks(df: pd.DataFrame, column: str, n: float) -> set:
    """
    Extract the top n% of stocks based on a specified column.

    Parameters:
    - df (pd.DataFrame): The dataframe containing the stock data.
    - column (str): The column name based on which the top stocks will be determined.
    - n (float): The percentage (in decimal form, e.g., 0.10 for 10%) of stocks to extract.

    Returns:
    - set: A set of stock symbols representing the top n%.
    """

    # Ensure valid input
    if not (0 < n <= 1):
        raise ValueError("The percentage should be between 0 and 1.")

    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the dataframe.")

    # Remove rows with NaN values in the specified column
    df_cleaned = df.dropna(subset=[column])

    # Sort the dataframe by the specified column in descending order
    df_sorted = df_cleaned.sort_values(by=column, ascending=False)

    # Extract the top n% of the sorted dataframe
    top_n_percent = df_sorted.head(int(n * len(df_sorted)))

    # Return the set of top n% stock symbols
    return set(top_n_percent["Unnamed: 0"].tolist())


# Load the data
df = pd.read_csv(msi_scraped_data)
filtered_stocks = get_top_n_percent_stocks(df, "price_strength", 0.10)
outfile = today_wl / f"screener1_{today_blank}.txt"
set_to_tv_ind(
    s=filtered_stocks,
    outfile=outfile,
    print_=True,
    filter_bands=True,
)
