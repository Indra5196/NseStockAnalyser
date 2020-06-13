from NseStockAnalyser.utils import *
from pprint import pprint


def index_52_wk_lows():

    index = get_index()
    # slicing off 1st index of the data list since it contains index data
    nifty50_stocks_data_json = get_index_stock_data_json(index)['data'][1:]

    try:
        data_pts = int(input(f'Enter number of data points (Input Range : 1 - {len(nifty50_stocks_data_json)}): '))
        if not 1 <= data_pts <= len(nifty50_stocks_data_json):
            raise ValueError
    except ValueError:
        print('Please enter a valid input')
        return

    stocks_list = []
    for stocks in nifty50_stocks_data_json:
        try:
            code = stocks['meta']['symbol']
        except KeyError:
            code = stocks['symbol']

        cur_price = float(stocks['lastPrice'])
        yr_low = float(stocks['yearLow'])
        yr_high = float(stocks['yearHigh'])
        price_diff_from_low = round(cur_price - yr_low, 2)
        price_diff_from_high = round(yr_high - cur_price, 2)
        percent_above_low = round((price_diff_from_low / yr_low) * 100, 2)
        percent_below_high = round((price_diff_from_high / yr_high) * 100, 2)
        best_buy_index = round(100 - ((price_diff_from_low / (yr_high - yr_low)) * 100), 2)
        stocks_list.append({'code': code, 'cur_price': cur_price, 'yr_low': yr_low, 'yr_high': yr_high,
                            'price_diff_from_low': price_diff_from_low, 'price_diff_from_high': price_diff_from_high,
                            'percent_above_low': percent_above_low, 'percent_below_high': percent_below_high,
                            'best_buy_index': best_buy_index})

    sort_types = ['% Above Low', '% Below High', 'Best Buy Index (100 - ((Price diff from low / high52 - low52) * 100))']
    while True:
        for i in range(0, len(sort_types)):
            print(f'{i+1} : {sort_types[i]}')

        try:
            opt = int(input(f'Which sorting order you prefer? (Input Range 1 - {sort_types}): '))
            if not 1 <= opt <= len(sort_types):
                raise ValueError
            break
        except ValueError:
            print("Please Enter Valid Input")

    if opt == 1:
        stocks_list = sorted(stocks_list, key=lambda i: i['percent_above_low'])
    elif opt == 2:
        stocks_list = sorted(stocks_list, key=lambda i: i['percent_below_high'])
    elif opt == 3:
        stocks_list = sorted(stocks_list, key=lambda i: i['best_buy_index'], reverse=True)

    df = pd.DataFrame(stocks_list)
    df.columns = ['Stock Code', 'Current Price(INR)', '52 Week Low', '52 Week High', 'Current - Low', 'High - Current',
                  '% Above Low', '% Below High', 'Best Buy Index']
    df.index = df.index + 1
    print('\n')
    print(df.head(data_pts))
    print('\n')
