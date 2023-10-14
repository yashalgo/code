# Write main function
from ..common.io import *

if __name__ == "__main__":
    # exchange
    strings_set = ["combined_master", "nse_bands", "nse_master"]
    for s in strings_set:
        delete_files_with_string_recursive(s, exchange_data)

    # msi
    delete_files_with_string_recursive(".txt", msi_ind_grp / "tv")
