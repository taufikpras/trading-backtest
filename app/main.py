from app.backtest import Backtest
from app.strategies.strategy_3ema import Strategy_3ema
from app.strategies.strategy_ema30 import Strategy_ema30
from app.strategies.strategy_ema20 import Strategy_ema20
from app.strategies.strategy_ema8_30 import Strategy_8_30
from pprint import pprint
import output
import warnings
warnings.filterwarnings("ignore")


backtest = Backtest(40000000,0.01)
# stg = Strategy_3ema("3 EMA")
# return_df, signal = backtest.backtest_watchlist(stg=stg)
# output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
# output.print_table(signal)

# stg = Strategy_ema30("EMA30 50")
# return_df, signal = backtest.backtest_watchlist(stg=stg)
# output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
# output.print_table(signal)

# stg = Strategy_ema20("EMA20 1wk")
# return_df, signal = backtest.backtest_watchlist(stg=stg,start_date="2022-01-01",interval="1wk")
# output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
# output.print_table(signal)

# stg = Strategy_ema20("EMA20 1d")
# return_df, signal = backtest.backtest_watchlist(stg=stg,start_date="2022-01-01",interval="1d")
# output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
# output.print_table(signal)

# stg = Strategy_8_30("EMA8_30 1wk")
# return_df, signal = backtest.backtest_watchlist(stg=stg,start_date="2020-01-01",interval="1wk")
# output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
# output.print_table(signal)

list_of_stg = []

ema20_wk = Strategy_ema20("EMA20 1wk")
ema20_dict = {"stg":ema20_wk, "start_date":"2022-01-01", "interval":"1wk"}
list_of_stg.append(ema20_dict)

ema20_d = Strategy_ema20("EMA20 1d")
ema20_dict = {"stg":ema20_d, "start_date":"2022-01-01", "interval":"1d"}
list_of_stg.append(ema20_dict)

ema8_30_wk = Strategy_8_30("EMA8_30 1wk")
ema8_30_dict = {"stg":ema8_30_wk, "start_date":"2020-01-01", "interval":"1wk"}
list_of_stg.append(ema8_30_dict)

ema8_30_d = Strategy_8_30("EMA8_30 1d")
ema8_30_dict = {"stg":ema8_30_d, "start_date":"2020-01-01", "interval":"1d"}
list_of_stg.append(ema8_30_dict)
ema30 = Strategy_ema30("EMA30 50")
ema30_dict = {"stg":ema30, "start_date":"2022-01-01", "interval":"1wk"}
list_of_stg.append(ema30_dict)

ema3 = Strategy_3ema("3 EMA")
ema3_dict = {"stg":ema3, "start_date":"2022-01-01", "interval":"1wk"}
list_of_stg.append(ema3_dict)

list_of_result = backtest.multi_stg_backtest(list_of_stg)
for result in list_of_result:
    # print(f"Ticker: {result['name']}")
    # print(f"stat: {result['stat']}")
    if(result["stat"].empty == False):
        output.save_multiple_backtests_to_pdf(result["stat"],filename=f'{result["name"]}.pdf', stg_name=result["name"])
    # output.print_table(result["signal"])