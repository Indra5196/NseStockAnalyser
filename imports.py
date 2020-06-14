import requests
import json
from nsetools import Nse
from nsepy import get_history
import datetime
from datetime import datetime, date, timedelta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta, TH
import pandas as pd
from nsetools import Nse
import calendar as cl
import urllib.parse
import pandasgui
import warnings

headers = {
    'User-Agent': 'Chrome/81.0.4044.138'
}

warnings.filterwarnings("ignore")
pd.set_option("display.max_rows", None, "display.max_columns", None)
NSE_INDICES_URL = "https://www.nseindia.com/api/equity-master"
