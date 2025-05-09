from strategy.strategy import Strategy
import math
import pandas as pd
from data import PriceData
from output import format_percent, format_rupiah
from datetime import datetime
class Backtest:
    def __init__(self, initial_account, risk_per_trade):
        self.initial_account = initial_account
        self.risk_per_trade_pct = risk_per_trade 
        
    
    def backtest_single_stock(self, stg:Strategy):
        trades = []
        in_position = False
        entry_price = 0
        entry_date = None
        lot = 0
        initial_sl = 0
        account_history = []
        balance_by_date = {}
        current_balance = self.initial_account
        df = stg.df
        df['entry_trade'] = 0
        df['exit_trade'] = 0
        for date, row in df.iterrows():
            if row['entry_signal'] and not in_position:
                # Hitung lot
                initial_sl = row['trailing']
                risk_per_share = row['Close'] - row['trailing']
                if risk_per_share <= 0.05 * row['Close']:
                    risk_per_share = 0.05 * row['Close']

                if risk_per_share <= 0:
                    continue  # Skip invalid entry
                risk_per_trade = self.risk_per_trade_pct * current_balance
                lot = max(int(risk_per_trade / (risk_per_share * 100)), 1)
                entry_price = row['Close']
                entry_date = date
                row['entry_trade'] = 1
                in_position = True

            elif row['exit_partial'] and in_position:
                exit_price = row['Close']
                lot_partial = math.floor(lot / 2)
                lot = lot - lot_partial
                profit = (exit_price - entry_price) * lot_partial * 100
                current_balance += profit

                # Simpan trade
                trades.append({
                    'entry_date': entry_date,
                    'exit_date': date,
                    'entry_price': round(entry_price,2),
                    'exit_price': round(exit_price,2),
                    'lot': lot_partial,
                    'entry_cost': lot * 100 * entry_price,
                    'profit': round(profit,2),
                    'initial_sl': round(initial_sl,2),
                    'account_balance': round(current_balance,2)
                })

            elif row['exit_signal'] and in_position:
                exit_price = row['Close']
                profit = (exit_price - entry_price) * lot * 100
                current_balance += profit

                # Simpan trade
                trades.append({
                    'entry_date': entry_date,
                    'exit_date': date,
                    'entry_price': round(entry_price,2),
                    'exit_price': round(exit_price,2),
                    'lot': lot,
                    'entry_cost': lot * 100 * entry_price,
                    'profit': round(profit,2),
                    'initial_sl': round(initial_sl,2),
                    'account_balance': round(current_balance,2)
                })
                row['exit_trade'] = 1
                # Reset posisi
                in_position = False
                entry_price = 0
                entry_date = None
                lot = 0
                initial_sl = 0

            # Simpan balance setiap hari
            account_history.append(current_balance)
            balance_by_date[date] = current_balance

        # Buat DataFrame trade
        trades_df = pd.DataFrame(trades)

        # Perhitungan statistik umum
        total_profit = trades_df['profit'].sum() if not trades_df.empty else 0
        number_of_trades = len(trades_df)
        profitable_trades = trades_df[trades_df['profit'] > 0] if not trades_df.empty else 0
        precision = len(profitable_trades) / number_of_trades if number_of_trades > 0 else 0
        largest_profit = trades_df['profit'].max() if not trades_df.empty else 0
        largest_loss = trades_df['profit'].min() if not trades_df.empty else 0
        drawdowns = [account_history[i] - max(account_history[:i+1]) for i in range(len(account_history))]
        max_drawdown = min(drawdowns) if drawdowns else 0

        # Hitung profit per tahun
        balance_series = pd.Series(balance_by_date)
        balance_series.index = pd.to_datetime(balance_series.index)

        yearly_profit = {}
        years = balance_series.index.year.unique()

        for year in years:
            yearly_data = balance_series[balance_series.index.year == year]
            if not yearly_data.empty:
                start_balance = yearly_data.iloc[0]
                end_balance = yearly_data.iloc[-1]
                profit_money = end_balance - start_balance
                profit_percent = (profit_money / start_balance) if start_balance != 0 else 0
                yearly_profit[year] = {
                    'start_balance': start_balance,
                    'end_balance': end_balance,
                    'profit_money': profit_money,
                    'profit_percent': profit_percent
                }

        yearly_df = pd.DataFrame.from_dict(yearly_profit, orient='index')
        yearly_df.index.name = 'Year'
        yearly_df.reset_index(inplace=True)
        # Format output
        statistics_results = {
            'total_profit': total_profit,
            'number_of_trades': number_of_trades,
            'precision': precision,
            'largest_profit': largest_profit,
            'largest_loss': largest_loss,
            'yearly_cagr': yearly_df['profit_percent'].mean(),
            'yearly_cagr_value': yearly_df['profit_money'].mean(),
            'max_drawdown': max_drawdown
        }
        return statistics_results, yearly_df, trades_df
    
    def backtest_watchlist(self, stg:Strategy, start_date= '2018-01-01', end_date= datetime.today().strftime('%Y-%m-%d'), interval="1d"):
        price_data = PriceData(start_date = start_date, interval = interval)
        wl = price_data.read_watchlist()

        stat_dict = {}
        results_list = []
        signal_dict = {}
        for ticker in wl:
            df = price_data.read_data(ticker)
            stg.set_df(df)
            stg.add_indicator()
            stg.add_signal()
            stg.df = stg.df.loc[start_date:end_date]

            stat, yearly, trades = self.backtest_single_stock(stg)
            stat_dict[ticker] = stat
            stat_dict[ticker]['yearly_profit'] = yearly
            stat_dict[ticker]['trades'] = trades
            result = {
                'ticker': ticker,
                'stats': stat,
                'trades': trades,
                'yearly_profit': yearly
            }
            results_list.append(result)

            if(stg.find_signal()):
                initial_risk = int(df.loc[df.index[-1], 'Close'])  - int(df.loc[df.index[-1], 'trailing'])
                risk_per_trade = self.initial_account * self.risk_per_trade_pct
                lot = risk_per_trade / (initial_risk * 100)
                result = {
                    'ticker': ticker,
                    'entry': int(df.loc[df.index[-1], 'Close']),
                    'lot': math.floor(lot),
                    'risk_pct': f"{round(initial_risk / int(df.loc[df.index[-1], 'Close']) * 100,2)}%",
                    'initial_risk': initial_risk,
                    'trailing': int(df.loc[df.index[-1], 'trailing']),
                    'total_profit': stat['total_profit'],
                    'number_of_trades': stat['number_of_trades'],
                    'precision': stat['precision'],
                    'largest_profit': stat['largest_profit'],
                    'largest_loss': stat['largest_loss'],
                    'max_drawdown': stat['max_drawdown']
                }
                signal_dict[ticker] = result
        stat_df = pd.DataFrame.from_dict(stat_dict, orient='index')
        stat_df.index.name = 'Ticker'
        stat_df.reset_index(inplace=True)

        signal_df = pd.DataFrame.from_dict(signal_dict, orient='index')
        signal_df.sort_values('total_profit', ascending=False)
        signal_df['total_profit'] = signal_df['total_profit'].apply(format_rupiah)
        signal_df['largest_profit'] = signal_df['largest_profit'].apply(format_rupiah)
        signal_df['largest_loss'] = signal_df['largest_loss'].apply(format_rupiah)
        signal_df['max_drawdown'] = signal_df['max_drawdown'].apply(format_rupiah)
        signal_df['entry'] = signal_df['entry'].apply(format_rupiah)
        signal_df['initial_risk'] = signal_df['initial_risk'].apply(format_rupiah)
        signal_df['trailing'] = signal_df['trailing'].apply(format_rupiah)
        signal_df['precision'] = signal_df['precision'].apply(format_percent)
        return stat_df, signal_df
    
