import pkg_resources
import subprocess
import sys
import yfinance as yf


def install_package(required):
    # required - a set of packages to be installed
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        python = sys.executable
        subprocess.check_call(
            [python, "-m", "pip", "install", *missing], stdout=subprocess.DEVNULL
        )
