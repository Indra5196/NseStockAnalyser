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


def get_opt_chain_url(stock_code):
    if stock_code == "NIFTY" or stock_code == "NIFTYIT" or stock_code == "BANKNIFTY":
        deriv_type = "indices"
    else:
        deriv_type = "equities"
    return "https://www.nseindia.com/api/option-chain-" + deriv_type + "?symbol=" + stock_code


def get_expiry_date(all_exp_dates):

    today = datetime.now()
    last_thurs = today + relativedelta(day=31, weekday=TH(-1))
    curr_month = last_thurs.month

    flag = 0
    if today > last_thurs:
        curr_month = curr_month + 1
        if curr_month > 12:
            flag = 1
            curr_month = 1

    month_year = cl.month_abbr[curr_month] + '-' + str(today.year + flag)

    curr_month_exp_dates = []
    for i_date in all_exp_dates:
        if month_year in i_date:
            curr_month_exp_dates.append(i_date)

    if len(curr_month_exp_dates) == 1:
        return curr_month_exp_dates[0]

    for i in range(0, len(curr_month_exp_dates)):
        print(f'{i+1} : {curr_month_exp_dates[i]}')

    while True:
        try:
            opt_id = int(input(f"Please select expiry date (Input Range 1 - {len(curr_month_exp_dates)}) : "))
            if not 1 <= opt_id <= len(curr_month_exp_dates):
                raise ValueError
            break
        except ValueError:
            print('Please enter a valid option')

    return curr_month_exp_dates[opt_id - 1]


def get_opt_chain_data_json(stock_code):
    data_json = requests.get(get_opt_chain_url(stock_code), headers=headers).json()
    data_records = data_json['records']['data']
    exp_date = get_expiry_date(data_json['records']['expiryDates'])

    opt_data = []
    for data in data_records:
        if data['expiryDate'] == exp_date:
            opt_data.append(data)

    return opt_data, exp_date

