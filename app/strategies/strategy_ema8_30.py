from app.strategies.strategy import Strategy
import ta

class Strategy_8_30(Strategy):
    
    
    def add_indicator(self):
        self.df['ema8'] = ta.trend.EMAIndicator(self.df['Close'], window=20).ema_indicator()
        self.df['ema30'] = ta.trend.EMAIndicator(self.df['Close'], window=50).ema_indicator()
        self.df['upper'] = self.df['ema30'] + ta.volatility.AverageTrueRange(self.df['High'], self.df['Low'], self.df['Close'], window=14).average_true_range()
        self.df['trailing'] = self.df['ema30'].shift(1) - ta.volatility.AverageTrueRange(self.df['High'], self.df['Low'], self.df['Close'], window=14).average_true_range().shift(1)
        self.df['trailing'] = self.df['trailing'].rolling(window=2).max()
        self.df['di'] = ta.trend.ADXIndicator(self.df['High'], self.df['Low'], self.df['Close'], window=14).adx_pos() -  ta.trend.ADXIndicator(self.df['High'], self.df['Low'], self.df['Close'], window=14).adx_neg()
        self.df = self.df.dropna()
    
    def add_signal(self):
        rule_entry = (
            (self.df['Close'] < self.df['upper']) &
            (self.df['Close'] > self.df['trailing']) &
            (self.df['Close'] > self.df['Close'].shift(1)) &
            (self.df['ema8'] > self.df['ema30']) &
            (self.df['Close'] > self.df['ema30']) &
            (self.df['di'] > 0)
        )
        self.df['entry_signal'] = rule_entry.astype(int)

        rule_exit = (
            (self.df['Close'] < self.df['trailing'])
        )
        self.df['exit_signal'] = rule_exit.astype(int)

        self.df['exit_partial'] = 0