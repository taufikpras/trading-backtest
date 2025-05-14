from app.backtest import Backtest
from app.strategies.strategy_close_ema import Strategy_Close_Ema
from pprint import pprint
import pandas as pd
import output
from output import format_rupiah, format_percent
import warnings
warnings.filterwarnings("ignore")


backtest = Backtest(40000000,0.01)

list_of_stg = []

ema8 = Strategy_Close_Ema("EMA8 1d",8)
list_of_stg.append({"stg":ema8, "start_date":"2019-01-01", "interval":"1d"})
ema20 = Strategy_Close_Ema("EMA20 1d", 20)
list_of_stg.append({"stg":ema20, "start_date":"2019-01-01", "interval":"1d"})
ema30 = Strategy_Close_Ema("EMA30 1d", 30)
list_of_stg.append({"stg":ema30, "start_date":"2019-01-01", "interval":"1d"})
ema50 = Strategy_Close_Ema("EMA50 1d", 50)
list_of_stg.append({"stg":ema50, "start_date":"2019-01-01", "interval":"1d"})


ema8 = Strategy_Close_Ema("EMA8 1wk",8)
list_of_stg.append({"stg":ema8, "start_date":"2019-01-01", "interval":"1wk"})
ema20 = Strategy_Close_Ema("EMA20 1wk", 20)
list_of_stg.append({"stg":ema20, "start_date":"2019-01-01", "interval":"1wk"})
ema30 = Strategy_Close_Ema("EMA30 1wk", 30)
list_of_stg.append({"stg":ema30, "start_date":"2019-01-01", "interval":"1wk"})
ema50 = Strategy_Close_Ema("EMA50 1wk", 50)
list_of_stg.append({"stg":ema50, "start_date":"2019-01-01", "interval":"1wk"})


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