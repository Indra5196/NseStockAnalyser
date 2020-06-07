from NseStockAnalyser.imports import *

# This link provides data regarding all stocks under NIFTY 50 Index
NIFTY50_DATA_URL = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'


def nifty_52_wk_lows():
    try:
        data_pts = int(input('Enter number of data points (Input Range : 1 - 50): '))
        if not 1 <= data_pts <= 50:
            raise ValueError
    except ValueError:
        print('Please enter a valid input')
        return

    # slicing off 1st index of the data list since it contains nifty 50 index data
    nifty50_stocks_data_json = requests.get(NIFTY50_DATA_URL, headers=headers).json()['data'][1:]

    stocks_list = []
    for stocks in nifty50_stocks_data_json:
        code = stocks['meta']['symbol']
        cur_price = stocks['lastPrice']
        yr_low = stocks['yearLow']
        price_diff_from_low = round(cur_price - yr_low, 2)
        percent_above_low = round((price_diff_from_low / yr_low) * 100, 2)
        stocks_list.append({'code': code, 'cur_price': cur_price, 'yr_low': yr_low,
                            'price_diff_from_low': price_diff_from_low,
                            'percent_above_low': percent_above_low})

    stocks_list = sorted(stocks_list, key=lambda i: i['percent_above_low'])

    df = pd.DataFrame(stocks_list)
    df.columns = ['Stock Code', 'Current Price(INR)', '52 Week Low', 'Price Difference', '% Above Low']
    df.index = df.index + 1
    print('\n')
    print(df.head(data_pts))
    print('\n')
