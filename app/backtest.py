from app.strategy.strategy import Strategy
import math
import pandas as pd


class Backtest:
    def __init__(self, initial_account, risk_per_trade, stg:Strategy):
        self.initial_account = initial_account
        self.risk_per_trade_pct = risk_per_trade 
        self.stg = stg
    
    def backtest(self):
        trades = []
        in_position = False
        entry_price = 0
        entry_date = None
        lot = 0
        initial_sl = 0
        account_history = []
        balance_by_date = {}
        current_balance = self.initial_account
        df = self.stg.df
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
        self.trades_df = pd.DataFrame(trades)

        # Perhitungan statistik umum
        total_profit = self.trades_df['profit'].sum() if not self.trades_df.empty else 0
        number_of_trades = len(self.trades_df)
        profitable_trades = self.trades_df[self.trades_df['profit'] > 0] if not self.trades_df.empty else 0
        precision = len(profitable_trades) / number_of_trades if number_of_trades > 0 else 0
        largest_profit = self.trades_df['profit'].max() if not self.trades_df.empty else 0
        largest_loss = self.trades_df['profit'].min() if not self.trades_df.empty else 0
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

        self.yearly_df = pd.DataFrame.from_dict(yearly_profit, orient='index')

        # Format output
        self.statistics_results = {
            'total_profit': total_profit,
            'number_of_trades': number_of_trades,
            'precision': precision,
            'largest_profit': largest_profit,
            'largest_loss': largest_loss,
            'yearly_cagr': self.yearly_df['profit_percent'].mean(),
            'yearly_cagr_value': self.yearly_df['profit_money'].mean(),
            'max_drawdown': max_drawdown
        }
        
    
