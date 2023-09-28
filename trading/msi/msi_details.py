### USING msi_data instead of this

# import logging
# import os
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# import re
# import time
# import multiprocessing

# from ..common.chrome_utils import *
# from ..common.config import *
# from ..exch.exch_utils import *


# logging.basicConfig(
#     filename="app.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )


# def load_invalid_stocks(filename):
#     try:
#         with open(filename, "r") as file:
#             return set(file.read().splitlines())
#     except FileNotFoundError:
#         logging.error(f"File not found: {filename}")
#         return set()


# def add_invalid_stock(filename, stock):
#     with open(filename, "a") as file:
#         file.write(stock + ",")


# def try_until_success(driver, details_css, values_css, max_attempts=2, wait_time=3):
#     attempts = 0
#     while attempts < max_attempts:
#         details = [
#             elem.text for elem in driver.find_elements(By.CSS_SELECTOR, details_css)
#         ]
#         values = [
#             elem.text for elem in driver.find_elements(By.CSS_SELECTOR, values_css)
#         ]
#         values2 = [i for i in values if i != ""]
#         if values2:
#             return details, values
#         wait_time += 3 * attempts
#         time.sleep(wait_time)
#         attempts += 1

#     logging.error(f"Failed to retrieve details/values after {max_attempts} attempts.")


# def scrape_stock(stock):
#     data = {}
#     try:
#         driver = get_chromedriver_basic()
#         url = f"https://marketsmithindia.com/mstool/eval/{stock}/evaluation.jsp#/"
#         driver.get(url)

#         WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located(
#                 (
#                     By.CSS_SELECTOR,
#                     ".custom-block-1 .details-block-1 .details, .custom-details-row-1 .details-block-2 .details, #details_placeholder_mcap .value-block-1 .value, #details_placeholder_masterscore .value-block-2 .value",
#                 )
#             )
#         )
#         time.sleep(3)

#         css_selectors = [
#             (
#                 ".custom-block-1 .details-block-1 .details",
#                 "#details_placeholder_mcap .value-block-1 .value",
#             ),
#             (
#                 ".custom-details-row-1 .details-block-2 .details",
#                 "#details_placeholder_masterscore .value-block-2 .value",
#             ),
#             (
#                 ".custom-block-2 .details-block-4 .details",
#                 "#details_placeholder_yield .value-block-4 .value",
#             ),
#             (
#                 ".custom-block-3 .details-block-5 .details",
#                 "#details_placeholder_alpha .value-block-5 .value",
#             ),
#             (
#                 ".custom-details-row-2 .details-block-3 .details",
#                 "#details_placeholder_eps .value-block-3 .value",
#             ),
#         ]

#         for idx, (details_css, values_css) in enumerate(css_selectors, 1):
#             details, values = try_until_success(driver, details_css, values_css)
#             parsed_data = parse_data_updated(details, values)
#             data = {**data, **parsed_data}

#         driver.quit()
#     except Exception as e:
#         logging.exception(f"Error scraping {stock}.")
#         add_invalid_stock(msi_invalid_list, stock)
#     return stock, data


# def main():
#     logging.info("Starting...")
#     invalid_stocks = load_invalid_stocks(msi_invalid_list)
#     overall_start_time = time.time()

#     df = get_combined_master()
#     logging.info(f"Total Stocks Combined: {df.shape[0]}")

#     pool_size = min(multiprocessing.cpu_count() * 2, len(df))
#     pool = multiprocessing.Pool(processes=pool_size)

#     if os.path.exists(msi_scraped_data):
#         df_result = pd.read_csv(msi_scraped_data, index_col=0)
#     else:
#         all_expected_columns = [
#             "m_cap",
#             "sales",
#             "float_shares",
#             "no_funds",
#             "per_change_funds",
#             "shares_funds",
#             "per_change_shares_fund",
#             "master_score",
#             "eps_rating",
#             "price_strength",
#             "a_d_rating",
#             "group_rank",
#             "yield",
#             "book_value",
#             "ud_vol_ratio",
#             "ltdebt_equity",
#             "alpha",
#             "beta",
#             "eps_growth_rate",
#             "earnings_stability",
#             "pe_ratio",
#             "five_year_pe_range",
#             "return_on_equity",
#             "cash_flow_inr",
#         ]
#         df_result = pd.DataFrame(columns=all_expected_columns)

#     t1 = df_result.shape[0]
#     df_result = df_result.dropna(how="all")
#     t2 = df_result.shape[0]
#     logging.info(f"Invalid Stocks: {len(invalid_stocks)}")
#     logging.info(f"{t1} - {t1-t2} = {t2}")

#     existing_stocks = df_result.index.tolist()
#     stock_symbols = [
#         row["NSE_SYMBOL"]
#         if isinstance(row["NSE_SYMBOL"], str) and row["NSE_SYMBOL"].strip() != ""
#         else str(int(row["BSE_CODE"]))
#         for _, row in df.iterrows()
#     ]
#     stock_symbols_filtered = [
#         s for s in stock_symbols if s not in existing_stocks and s not in invalid_stocks
#     ]
#     logging.info(f"Remaining Stocks to Scrape: {len(stock_symbols_filtered)}")

#     if not stock_symbols_filtered:
#         logging.info("No stocks to scrape.")
#         return

#     save_interval = 50
#     for stock_count, (stock, data) in enumerate(
#         pool.imap_unordered(scrape_stock, stock_symbols_filtered), 1
#     ):
#         df_result.loc[stock] = data
#         if stock_count % save_interval == 0:
#             df_result = df_result.dropna(how="all")
#             df_result.to_csv(msi_scraped_data)
#             logging.info(
#                 f"Processed {stock_count} stocks. Time Elapsed: {time.time() - overall_start_time:.1f} seconds"
#             )

#     df_result = df_result.dropna(how="all")
#     df_result.to_csv(msi_scraped_data)
#     pool.close()
#     pool.join()

#     logging.info("Scraping process completed.")


# if __name__ == "__main__":
#     os.chdir(msi_scrape)
#     main()
#     logging.info("====== ALL DONE ======")
