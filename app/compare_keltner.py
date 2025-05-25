from app.backtest import Backtest
from app.strategies.strategy_close_ema import Strategy_Close_Ema
from app.strategies.strategy_keltner import Strategy_Keltner
from pprint import pprint
import pandas as pd
import output
from output import format_rupiah, format_percent
import warnings
warnings.filterwarnings("ignore")


backtest = Backtest(40000000,0.01)

list_of_stg = []

list_of_stg.append({"stg":Strategy_Close_Ema("EMA50 1d", 50), 
                    "start_date":"2019-01-01", 
                    "interval":"1d"})

list_of_stg.append({"stg":Strategy_Close_Ema("EMA150 1d", 150), 
                    "start_date":"2019-01-01", 
                    "interval":"1d"})

list_of_stg.append({"stg":Strategy_Close_Ema("EMA200 1d", 200), 
                    "start_date":"2019-01-01", 
                    "interval":"1d"})

list_of_stg.append({"stg":Strategy_Keltner("keltner 20 1d", ma=20, atr_multiply=1, atr_window=10, lookback=5), 
                    "start_date":"2019-01-01", 
                    "interval":"1d"})

list_of_stg.append({"stg":Strategy_Keltner("keltner 20 1d", ma=20, atr_multiply=1, atr_window=10, lookback=5), 
                    "start_date":"2019-01-01", 
                    "interval":"1d"})

list_of_stg.append({"stg":Strategy_Keltner("keltner 50 1d", ma=50, atr_multiply=1, atr_window=10, lookback=5), 
                    "start_date":"2019-01-01", 
                    "interval":"1d"})
list_of_stg.append({"stg":Strategy_Keltner("keltner 200 1d", ma=200, atr_multiply=1, atr_window=10, lookback=5), 
                    "start_date":"2019-01-01", 
                    "interval":"1d"})

list_of_result = backtest.multi_stg_backtest(list_of_stg)
result_accumulation_dict = {}
for result in list_of_result:
    if(result["stat"].empty == False):
        output.save_multiple_backtests_to_pdf(result["stat"],filename=f'{result["name"]}.pdf', stg_name=result["name"])
        summary_text = {
            "name": result["name"],
            "number_of_stocks": {result["stat"].shape[0]},
            "total_profit": format_rupiah(result["stat"]["total_profit"].sum()),
            "number_of_trades": result["stat"]["number_of_trades"].sum(),
            "precision": format_percent(result["stat"]["precision"].mean()),
            "largest_profit": format_rupiah(result["stat"]["largest_profit"].max()),
            "largest_loss": format_rupiah(result["stat"]["largest_loss"].min()),
            "max_drawdown": format_rupiah(result["stat"]["max_drawdown"].min()),
            "avg_cagr_percent": format_percent(result["stat"]["yearly_cagr"].mean()),
            "avg_cagr_value": format_rupiah(result["stat"]["yearly_cagr_value"].mean())
        }
        result_accumulation_dict[result["name"]] = summary_text

# print(result_accumulation_dict)
df_result = pd.DataFrame.from_dict(result_accumulation_dict, orient="index")
output.print_dataframe_to_pdf(df_result, filename="summary.pdf", title="Summary Backtest")
output.print_table(df_result)