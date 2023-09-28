import pandas as pd
from ..common.config import *
from ..common.tv_utils import *
from ..exch.exch_utils import *


def get_top_percentile_stocks(df, column_name, percentile):
    """
    Get the top n percentile of stocks based on a specified column.

    Parameters:
    - df: DataFrame containing the stock data
    - column_name: Name of the column based on which the top stocks are to be fetched
    - percentile: The percentile value (as a float, e.g., 0.1 for 10%)

    Returns:
    - A DataFrame containing the top n percentile of stocks based on the specified column
    """
    # Calculate the threshold value for the desired percentile
    threshold = df[column_name].quantile(1 - percentile)

    # Filter the DataFrame to only include rows where the column value is above the threshold
    top_stocks = df[df[column_name] >= threshold]

    return set(top_stocks[top_stocks.columns[0]])


# Load the data

df = pd.read_csv(msi_scraped_data)
# print(df.columns)
result = get_top_percentile_stocks(df, "master_score", 0.1)
tv = set_to_tv_ind(result, "RS_FILTER.txt")
# print(tv)
