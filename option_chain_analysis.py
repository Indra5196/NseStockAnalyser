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


def continuation_handler(original_fn):
    def wrapper_fn():
        while (True):
            try:
                original_fn()
            except (ValueError, KeyError):
                print('Wrong data, or the stock is not traded as derivatives')
                continue

            while (True):
                flg = input("\n\rDo you want to know about more stock derivatives?(Y/N) : ").upper()
                if flg == 'Y' or flg == 'N':
                    break
                print('Answer should be either Y(Yes) or N(No)')

            if flg == 'N':
                return

    return wrapper_fn


@continuation_handler
def opt_chain_wrapper():
    code = input("Enter Stock Code : ")
    data_points = int(input("How many data points you want per category? : "))
    try:
        ce_strk_dict, pe_strk_dict, max_pain_dict, lot_size = opt_chain_analysis(code.upper(), data_points)
    except ValueError:
        raise ValueError


    for i in range(0, data_points):
        print (f'Call Point {i + 1} :- Strike Price = {ce_strk_dict[i][0]} : OI = {ce_strk_dict[i][1] * lot_size}')

    print('==========================================================================')

    for i in range(0, data_points):
        print (f'Put Point {i + 1} :- Strike Price = {pe_strk_dict[i][0]} : OI = {pe_strk_dict[i][1] * lot_size}')

    print('==========================================================================')

    for i in range(0, data_points):
        print (f'Max Pain Point {i + 1} :- Strike Price = {max_pain_dict[i][0]} : OI = {max_pain_dict[i][1] * lot_size}')


def open_interest_graphs(stock_code, no_days, strike_price, opt_type):
    index = False
    if stock_code == "NIFTY" or stock_code == "NIFTYIT" or stock_code == "BANKNIFTY":
        index = True

    end_date = date.today()
    start_date = end_date - datetime.timedelta(days = no_days)
    expiry_date = end_date + relativedelta(day=31, weekday=TH(-1))  # Last thursday of the month

    if opt_type == "CE" or opt_type == "PE":
        stock_opt = get_history(symbol=stock_code,
                                start=start_date,
                                end=end_date,
                                option_type=opt_type,
                                strike_price=strike_price,
                                expiry_date=expiry_date,
                                index=index)

        x = list(dict(stock_opt['Open Interest']).keys())
        y = list(dict(stock_opt['Open Interest']).values())

    elif opt_type == "TOTAL":
        stock_opt_ce = get_history(symbol=stock_code,
                                start=start_date,
                                end=end_date,
                                option_type="CE",
                                strike_price=strike_price,
                                expiry_date=expiry_date)

        stock_opt_pe = get_history(symbol=stock_code,
                                start=start_date,
                                end=end_date,
                                option_type="PE",
                                strike_price=strike_price,
                                expiry_date=expiry_date)

        x = list(dict(stock_opt_ce['Open Interest']).keys())
        a = list(dict(stock_opt_ce['Open Interest']).values())
        b = list(dict(stock_opt_pe['Open Interest']).values())
        y = [i + j for i, j in zip(a, b)]

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.xlabel('Date')
    plt.ylabel('Open Interest')

    plt.title(f'{opt_type} Open Interest variation at strike price of Rs.{strike_price} in the past {no_days} days\n')
    plt.show()


@continuation_handler
def put_call_wrapper():
    code = input("Enter Stock Code : ")
    try:
        pc_oi, pc_vol = put_call_ratio(code.upper())
    except ValueError:
        raise ValueError

    print(f'P/C Ratio (Open Interest) : {pc_oi}')
    print(f'P/C Ratio (Volume) : {pc_vol}')


@continuation_handler
def oi_graph_wrapper():
    try:
        stock_code = input("Enter Stock Code : ").upper()
        nse = Nse()
        try:
            nse.get_fno_lot_sizes()[stock_code]
        except KeyError:
            raise KeyError

        no_days = int(input("Please enter number of days you want past data of (Min = 2, Max = 20) : "))
        if no_days < 2 or no_days > 20:
            raise ValueError

        strike_price = int(input("Please enter strike price : "))

        if strike_price not in [x['strikePrice'] for x in get_opt_chain_data_json(stock_code)['filtered']['data']]:
            print("Data for this strike price is not available")
            raise ValueError

        while True:
            opt_type = input("Please Enter Option Type (CE/PE/TOTAL) : ").upper()
            if opt_type == 'CE' or opt_type == 'PE' or opt_type == "TOTAL":
                break
            else:
                print('Please enter valid option type')

    except ValueError:
        raise ValueError

    open_interest_graphs(stock_code, no_days, strike_price, opt_type)


def get_opt_chain_data_json(stock_code):
    if stock_code == "NIFTY" or stock_code == "NIFTYIT" or stock_code == "BANKNIFTY":
        deriv_type = "indices"
    else:
        deriv_type = "equities"
    url = "https://www.nseindia.com/api/option-chain-" + deriv_type + "?symbol=" + stock_code
    headers = {
        'User-Agent': 'Chrome/81.0.4044.138'
    }

    return requests.get(url, headers=headers).json()


def opt_chain_analysis(stock_code, data_points):
    nse = Nse()
    try:
        lot_size = nse.get_fno_lot_sizes()[stock_code]
    except KeyError:
        raise KeyError

    data_json = get_opt_chain_data_json(stock_code)
    ce_pe = data_json['filtered']['data']

    ce_strk_dict, pe_strk_dict, max_pain_dict = {}, {}, {}

    for val in ce_pe:
        try:
            ce_oi = val['CE']['openInterest']
            pe_oi = val['PE']['openInterest']
        except KeyError:
            continue

        mp = ce_oi + pe_oi

        ce_strk_dict.update({val['strikePrice'] : ce_oi})
        pe_strk_dict.update({val['strikePrice']: pe_oi})
        max_pain_dict.update({val['strikePrice']: ce_oi + pe_oi})

    ce_strk_dict = sorted(ce_strk_dict.items(), key=lambda item: item[1], reverse=True)
    pe_strk_dict = sorted(pe_strk_dict.items(), key=lambda item: item[1], reverse=True)
    max_pain_dict = sorted(max_pain_dict.items(), key=lambda item: item[1], reverse=True)

    return ce_strk_dict, pe_strk_dict, max_pain_dict, lot_size


def put_call_ratio(stock_code):
    nse = Nse()
    try:
        nse.get_fno_lot_sizes()[stock_code]
    except KeyError:
        raise KeyError

    data_json = get_opt_chain_data_json(stock_code)
    call_data = data_json['filtered']['CE']
    put_data = data_json['filtered']['PE']

    return round(put_data['totOI'] / call_data['totOI'], 2) , round(put_data['totVol'] / call_data['totVol'],2)


print("+++++++++++++++++ NSE STOCK ANALYSER ++++++++++++++++++++")
options = ['Option Chain Analysis', 'Put/Call Ratio', 'Open Interest Graphs', 'Exit']
while(True):
    for i in range(0, len(options)):
        print(f'{i+1} : {options[i]}')

    try:
        opt_id = int(input("What analysis you want to perform? (Please enter option ID) : "))
    except ValueError:
        print('Please enter a valid option')
        continue

    if opt_id < 1 or opt_id > len(options):
        print('Please enter a valid option')
        continue

    if opt_id == 1:
        opt_chain_wrapper()

    if opt_id == 2:
        put_call_wrapper()

    if opt_id == 3:
        oi_graph_wrapper()

    if opt_id == len(options):
        print('Thank you for using the application')
        break