from datetime import datetime,date, timedelta
import pandas as pd
import numpy as np
import os
from glob import glob
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pathlib import Path
from kiteconnect import KiteConnect, KiteTicker, exceptions
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pyotp
import sys
import subprocess
import pkg_resources
import plotly.graph_objects as go
import json
from finvizfinance.screener.custom import Custom
import stumpy
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings("ignore")
import shutil
from scipy.cluster.hierarchy import linkage, dendrogram
from clustimage import Clustimage
from IPython.display import Image, display, clear_output
import cv2