from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import warnings

warnings.simplefilter(action="ignore", category=pd.errors.SettingWithCopyWarning)

from ..common.chrome_utils import *
from ..common.config import *
from ..common.io import *
from ..msi.msi_util import *

IND_GRP_IMG = f"{today_blank}_ind_grp.png"


def get_ind_grp_ranks():
    change_dir(msi_ind_grp / "csv")
    outfile = f"{today_blank}_ind_grp_ranks.csv"
    if check_file(outfile):
        print(f" CSV File already exists: {outfile}")
        return pd.read_csv(outfile)

    driver = get_msi_home(msi_ind_grp)
    driver.get(IND_GRP_RANKS)

    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "industryExport")))
    button.click()

    wait_for_download(msi_ind_grp)

    original_filename = os.path.join(msi_ind_grp, "industryGroupList.csv")
    os.rename(original_filename, outfile)
    df = pd.read_csv(outfile, index_col=False)
    df = df[df["NumberOfStocks"] > 1]

    df["MarketCapital"] = df["MarketCapital"].apply(get_numerical_value)
    df = df[df["MarketCapital"] > 500]

    df["Rank -1W"] = pd.to_numeric(
        df["IndustryGroupRankLastWeek"], errors="coerce", downcast="integer"
    )
    df["Rank -3M"] = pd.to_numeric(
        df["IndustryGroupRankLast3MonthAgo"], errors="coerce", downcast="integer"
    )
    df["Rank -6M"] = pd.to_numeric(
        df["IndustryGroupRankLast6MonthAgo"], errors="coerce", downcast="integer"
    )

    df["Rank"] = df["IndustryGroupRankCurrent"].rank()

    df["Change 1W"] = df["Rank -1W"] - df["Rank"]
    df["Change 3M"] = df["Rank -3M"] - df["Rank"]
    df["Change 6M"] = df["Rank -6M"] - df["Rank"]

    df = df.rename(
        columns={
            "IndustryGroupName": "Industry Group",
            "NumberOfStocks": "Stocks",
            "MarketCapital": "M_Cap",
        }
    )

    df["Change 1W Rank"] = (
        custom_rank(df["Change 1W"], df["M_Cap"], ascending=False) + 1
    )
    df["Change 3M Rank"] = (
        custom_rank(df["Change 3M"], df["M_Cap"], ascending=False) + 1
    )
    df["Change 6M Rank"] = (
        custom_rank(df["Change 6M"], df["M_Cap"], ascending=False) + 1
    )

    df["Industry Group"] = (
        df["Industry Group"].str.replace(" IN", "").str.replace("&amp;", "&")
    )
    df.to_csv(outfile, index=False)
    print(f"Fetched file {outfile} succesfully")
    return df


def render_mpl_table(
    data,
    col_widths,
    row_height=0.625,
    font_size=12,
    header_color="#40466e",
    row_colors=["#f1f1f2", "w"],
    edge_color="w",
    header_columns=0,
    ax=None,
    **kwargs,
):
    if ax is None:
        fig, ax = plt.subplots(
            figsize=(sum(col_widths) + 1, len(data) * row_height + 1)
        )
        ax.axis("off")

    numeric_data = data.apply(pd.to_numeric, errors="ignore")

    # colors = sns.color_palette("YlOrRd", 100)
    colors = sns.color_palette("RdYlGn", 100)[
        ::-1
    ]  # Reverse the palette so that red represents low values and green represents high values

    cell_colors = {}

    for col in numeric_data.columns:
        if col not in ["Stocks", "M_Cap"]:
            col_data = numeric_data[col]
            if pd.api.types.is_numeric_dtype(col_data):
                min_val, max_val = col_data.min(), col_data.max()
                range_val = max_val - min_val
                if range_val == 0:
                    range_val = 1

                if col in ["Change 1W", "Change 3M", "Change 6M"]:
                    cell_colors[col] = [
                        colors[99 - int((v - min_val) / range_val * 99)]
                        if pd.notna(v)
                        else "white"
                        for v in col_data
                    ]
                else:
                    cell_colors[col] = [
                        colors[int((v - min_val) / range_val * 99)]
                        if pd.notna(v)
                        else "white"
                        for v in col_data
                    ]

    mpl_table = ax.table(
        cellText=data.values,
        bbox=[0, 0, 1, 1],
        colLabels=data.columns,
        colWidths=col_widths,
        **kwargs,
    )
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for i, (k, cell) in enumerate(mpl_table._cells.items()):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight="bold", color="w")
            cell.set_facecolor(header_color)
        else:
            column = data.columns[k[1]]
            if column in cell_colors:
                cell.set_facecolor(
                    cell_colors[column][k[0] - 1]
                )  # k[0] - 1 because table includes header
            else:
                cell.set_facecolor(row_colors[k[0] % len(row_colors)])


def get_ind_group_image():
    outfile = os.path.join(msi_ind_grp / "img", IND_GRP_IMG)
    if os.path.exists(outfile):
        print(f" Image File already exists: {outfile}")
        return True

    data = get_ind_grp_ranks()

    print(f"Total valid Groups: {data.shape[0]}")
    rank_filter = math.floor(data.shape[0] * 0.05)
    top_5_percent_data = data[
        (
            data[["Rank", "Change 1W Rank", "Change 3M Rank", "Change 6M Rank"]]
            <= rank_filter
        ).any(axis=1)
    ]
    filtered_data = top_5_percent_data[
        [
            "Symbol",
            "Industry Group",
            "Stocks",
            "M_Cap",
            "Rank",
            "Rank -1W",
            "Rank -3M",
            "Rank -6M",
            "Change 1W",
            "Change 3M",
            "Change 6M",
        ]
    ]

    filtered_data = filtered_data.applymap(format_value)

    for col in ["Change 1W", "Change 3M", "Change 6M"]:
        filtered_data[col] = filtered_data[col].apply(lambda x: f"+{x}" if x > 0 else x)
    outfile_f = os.path.join(msi_ind_grp / "csv", f"{today_blank}_ind_grp_ranks_f.csv")

    filtered_data.to_csv(outfile_f)

    print(f"Saved filtered Ind Grp file: {outfile_f}")

    ### PROCESSING IMG
    os.chdir(msi_ind_grp / "img")
    col_widths = [
        max(filtered_data[col].astype(str).apply(len).max(), len(col)) * 0.2
        for col in filtered_data.columns
    ]
    row_height = 0.625

    fig, ax = plt.subplots(
        figsize=(sum(col_widths) + 1, len(filtered_data) * row_height + 1)
    )
    ax.axis("off")

    render_mpl_table(filtered_data, col_widths=col_widths, header_columns=0, ax=ax)

    fig.savefig(IND_GRP_IMG, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Img saved successfuly: {IND_GRP_IMG}")
    return True


if __name__ == "__main__":
    get_ind_group_image()
