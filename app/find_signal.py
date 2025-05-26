from app.backtest import Backtest
from app.strategies.strategy_close_ema import Strategy_Close_Ema
from app.strategies.strategy_keltner import Strategy_Keltner
import output
from output import format_rupiah, format_percent
import warnings
warnings.filterwarnings("ignore")

list_of_stg = []
list_of_result = []
stg = Strategy_Keltner("keltner 150 1d", ma=150, atr_multiply=2, atr_window=10, lookback=5)
list_of_stg.append({"stg":stg, 
                    "start_date":"2019-01-01", 
                    "interval":"1d"})

backtest = Backtest(40000000,0.005)
result_accumulation_dict = {}
backtest_result, signal_df = backtest.backtest_watchlist(
    stg, 
    start_date="2019-01-01", 
    interval="1d"
)
output.print_table(signal_df)