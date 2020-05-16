import requests
import json
from nsetools import Nse
from pprint import pprint

def opt_chain_wrapper():
    while (True):
        code = input("Enter Stock Code : ")
        data_points = input("How many data points you want per category? : ")
        ce_strk_dict, pe_strk_dict, max_pain_dict = opt_chain_analysis(code.upper(), int(data_points))

        for i in range(0, data_points):
            print (f'Call Point {i + 1} :- Strike Price = {ce_strk_dict[i][0]} : OI = {ce_strk_dict[i][1] * lot_size}')

        print('==========================================================================')

        for i in range(0, data_points):
            print (f'Put Point {i + 1} :- Strike Price = {pe_strk_dict[i][0]} : OI = {pe_strk_dict[i][1] * lot_size}')

        print('==========================================================================')

        for i in range(0, data_points):
            print (
                f'Max Pain Point {i + 1} :- Strike Price = {max_pain_dict[i][0]} : OI = {max_pain_dict[i][1] * lot_size}')


        while (True):
            flg = input("\n\rDo you want to know about more stock derivatives?(Y/N) : ").upper()
            if flg == 'Y' or flg == 'N':
                break
            print('Answer should be either Y(Yes) or N(No)')

        if flg == 'N':
            return


def put_call_wrapper():
    while (True):
        code = input("Enter Stock Code : ")
        pc_oi, pc_vol = put_call_ratio(code.upper())

        print(f'P/C Ratio (Open Interest) : {pc_oi}')
        print(f'P/C Ratio (Volume) : {pc_vol}')

        while (True):
            flg = input("\n\rDo you want to know about more stock derivatives?(Y/N) : ").upper()
            if flg == 'Y' or flg == 'N':
                break
            print('Answer should be either Y(Yes) or N(No)')

        if flg == 'N':
            return

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
        print('Wrong stock symbol, or the stock is not traded as derivatives')
        return

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

    return ce_strk_dict, pe_strk_dict, max_pain_dict

def put_call_ratio(stock_code):
    nse = Nse()
    try:
        nse.get_fno_lot_sizes()[stock_code]
    except KeyError:
        print('Wrong stock symbol, or the stock is not traded as derivatives')
        return

    data_json = get_opt_chain_data_json(stock_code)
    call_data = data_json['filtered']['CE']
    put_data = data_json['filtered']['PE']

    return round(put_data['totOI'] / call_data['totOI'], 2) , round(put_data['totVol'] / call_data['totVol'],2)


print("+++++++++++++++++ NSE STOCK ANALYSER ++++++++++++++++++++")
options = ['Option Chain Analysis', 'Put/Call Ratio', 'Exit']
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

    if opt_id == len(options):
        print('Thank you for using the application')
        break