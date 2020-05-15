import requests
import json
from nsetools import Nse
from pprint import pprint


def opt_chain_analysis(stock_code, data_points):
    nse = Nse()
    try:
        lot_size = nse.get_fno_lot_sizes()[stock_code]
    except KeyError:
        print('Wrong stock symbol, or the stock is not traded as derivatives')
        return

    if stock_code == "NIFTY" or stock_code == "NIFTYIT" or stock_code == "BANKNIFTY":
        deriv_type = "indices"
    else:
        deriv_type = "equities"
    url = "https://www.nseindia.com/api/option-chain-" + deriv_type + "?symbol=" + stock_code
    headers = {
        'User-Agent': 'Chrome/81.0.4044.138'
    }


    data_json = requests.get(url, headers=headers).json()
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


    for i in range(0, data_points):
        print (f'Call Point {i + 1} :- Strike Price = {ce_strk_dict[i][0]} : OI = {ce_strk_dict[i][1] * lot_size}')

    print('==========================================================================')

    for i in range(0, data_points):
        print (f'Put Point {i + 1} :- Strike Price = {pe_strk_dict[i][0]} : OI = {pe_strk_dict[i][1] * lot_size}')

    print('==========================================================================')

    for i in range(0, data_points):
        print (f'Max Pain Point {i + 1} :- Strike Price = {max_pain_dict[i][0]} : OI = {max_pain_dict[i][1] * lot_size}')

code = input("Enter Stock Code : ")
data_points = input("How many data points you want per category? : ")
opt_chain_analysis(code.upper(), int(data_points))