from backtest import Backtest
from strategy.strategy_3ema import Strategy_3ema
from strategy.strategy_ema30 import Strategy_ema30
from strategy.strategy_ema20 import Strategy_ema20
from pprint import pprint
import output
import warnings
warnings.filterwarnings("ignore")


backtest = Backtest(40000000,0.01)
stg = Strategy_3ema("3 EMA")
return_df, signal = backtest.backtest_watchlist(stg)
output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
output.print_table(signal)

stg = Strategy_ema30("EMA30 50")
return_df, signal = backtest.backtest_watchlist(stg)
output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
output.print_table(signal)

stg = Strategy_ema20("EMA20 1wk")
return_df, signal = backtest.backtest_watchlist(stg,"2016-01-01","1wk")
output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
output.print_table(signal)
