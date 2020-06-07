import requests
import json
from nsetools import Nse
from nsepy import get_history
import datetime
from datetime import date
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta, TH
import pandas as pd
from nsetools import Nse

headers = {
    'User-Agent': 'Chrome/81.0.4044.138'
}