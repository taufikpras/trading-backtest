from backtest import Backtest
from strategy.strategy_3ema import Strategy_3ema
from pprint import pprint
import output
import warnings
warnings.filterwarnings("ignore")


backtest = Backtest(40000000,0.01)
stg = Strategy_3ema("3 EMA")
return_df = backtest.backtest_watchlist(stg)
output.save_multiple_backtests_to_pdf(return_df,filename=f'{stg.name}.pdf', stg_name=stg.name)
pprint(return_df)

