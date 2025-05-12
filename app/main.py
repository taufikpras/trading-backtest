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

stg = Strategy_ema20("EMA20 1wk")
return_df, signal = backtest.backtest_watchlist(stg=stg,start_date="2022-01-01",interval="1wk")
output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
output.print_table(signal)

stg = Strategy_ema20("EMA20 1d")
return_df, signal = backtest.backtest_watchlist(stg=stg,start_date="2022-01-01",interval="1d")
output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
output.print_table(signal)

stg = Strategy_8_30("EMA8_30 1wk")
return_df, signal = backtest.backtest_watchlist(stg=stg,start_date="2020-01-01",interval="1wk")
output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
output.print_table(signal)