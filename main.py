from NseStockAnalyser.option_chain_analysis import opt_chain_wrapper
from NseStockAnalyser.put_call_ratio import put_call_wrapper
from NseStockAnalyser.open_interest_graphs import oi_graph_wrapper

print("+++++++++++++++++ NSE STOCK ANALYSER ++++++++++++++++++++")
options = ['Option Chain Analysis', 'Put/Call Ratio', 'Open Interest Graphs', 'Exit']
while True:
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
