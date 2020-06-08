from NseStockAnalyser.imports import *
from NseStockAnalyser.utils import *


def put_call_ratio(stock_code):
    nse = Nse()

    nse.get_fno_lot_sizes()[stock_code]  # If stock code not present, it will cause exception. will be caught by
                                         # continuation_handler

    data_json = requests.get(get_opt_chain_url(stock_code), headers=headers).json()['filtered']
    call_data = data_json['CE']
    put_data = data_json['PE']

    return round(put_data['totOI'] / call_data['totOI'], 2), round(put_data['totVol'] / call_data['totVol'], 2)


@continuation_handler
def put_call_wrapper():
    code = input("Enter Stock Code : ")

    pc_oi, pc_vol = put_call_ratio(code.upper())

    print(f'P/C Ratio (Open Interest) : {pc_oi}')
    print(f'P/C Ratio (Volume) : {pc_vol}')
