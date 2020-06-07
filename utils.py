from NseStockAnalyser.imports import *


def continuation_handler(original_fn):
    def wrapper_fn():
        while True:
            try:
                original_fn()
            except (ValueError, KeyError):
                print('Wrong data, or the stock is not traded as derivatives')
                continue

            while True:
                flg = input("\n\rDo you want to know about more stock derivatives?(Y/N) : ").upper()
                if flg == 'Y' or flg == 'N':
                    break
                print('Answer should be either Y(Yes) or N(No)')

            if flg == 'N':
                return

    return wrapper_fn


def get_opt_chain_data_json(stock_code):
    if stock_code == "NIFTY" or stock_code == "NIFTYIT" or stock_code == "BANKNIFTY":
        deriv_type = "indices"
    else:
        deriv_type = "equities"
    url = "https://www.nseindia.com/api/option-chain-" + deriv_type + "?symbol=" + stock_code

    return requests.get(url, headers=headers).json()
