import requests
import json
from nsetools import Nse


def opt_chain_analysis(stock_code):
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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }


    data_json = requests.get(url, headers=headers).json()
    ce_pe = data_json['filtered']['data']

    max_ce_oi, max_pe_oi, max_pain_oi, strk_price_max_ce, strk_price_max_pe, strk_price_max_pain = 0, 0, 0, 0, 0, 0
    for val in ce_pe:
        ce_oi = val['CE']['openInterest']
        pe_oi = val['PE']['openInterest']

        mp = ce_oi + pe_oi

        if ce_oi > max_ce_oi:
            max_ce_oi = ce_oi
            strk_price_max_ce = val['strikePrice']

        if pe_oi > max_pe_oi:
            max_pe_oi = pe_oi
            strk_price_max_pe = val['strikePrice']

        if mp > max_pain_oi:
            max_pain_oi = mp
            strk_price_max_pain = val['strikePrice']

    print(f'Max Put:- OI = {max_pe_oi * lot_size} : Strike Price = {strk_price_max_pe}')
    print(f'Max Call:- OI = {max_ce_oi * lot_size} : Strike Price = {strk_price_max_ce}')
    print(f'Max Pain:- OI = {max_pain_oi * lot_size} : Strike Price = {strk_price_max_pain}')

code = input("Enter Stock Code : ")
opt_chain_analysis(code.upper())