from strategy.strategy import Strategy
import ta

class Strategy_ema20(Strategy):
    
    
    def add_indicator(self):
        self.df['ema20'] = ta.trend.EMAIndicator(self.df['Close'], window=20).ema_indicator()
        self.df['ema50'] = ta.trend.EMAIndicator(self.df['Close'], window=50).ema_indicator()
        self.df['upper'] = self.df['ema20'] + ta.volatility.AverageTrueRange(self.df['High'], self.df['Low'], self.df['Close'], window=14).average_true_range()
        self.df['trailing'] = self.df['ema20'].shift(1) - (ta.volatility.AverageTrueRange(self.df['High'], self.df['Low'], self.df['Close'], window=14).average_true_range().shift(1) * 0.5)
        self.df['trailing'] = self.df['trailing'].rolling(window=3).max()
        self.df['pct'] = (self.df['Close'] - self.df['trailing']) * 100 / self.df['Close']
        self.df['di'] = ta.trend.ADXIndicator(self.df['High'], self.df['Low'], self.df['Close'], window=14).adx_pos() -  ta.trend.ADXIndicator(self.df['High'], self.df['Low'], self.df['Close'], window=14).adx_neg()
        self.df = self.df.dropna()
    
    def add_signal(self):
        rule_entry = (
            (self.df['Close'] < self.df['upper']) &
            (self.df['Close'] > self.df['trailing']) &
            (self.df['ema20'] > self.df['ema50']) &
            (self.df['pct'] < 11) &
            (self.df['di'] > 0)
        )
        self.df['entry_signal'] = rule_entry.astype(int)

        rule_exit = (
            (self.df['Close'] < self.df['trailing'])
        )
        self.df['exit_signal'] = rule_exit.astype(int)

        self.df['exit_partial'] = 0