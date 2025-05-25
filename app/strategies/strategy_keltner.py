from app.strategies.strategy import Strategy
import ta

class Strategy_Keltner(Strategy):
    def __init__(self, name, ma = 20, atr_multiply = 1.5, atr_window = 14, lookback = 5):
        super().__init__(name)
        self.description = "entry when  \
            and ma > ema_trend \
            and di >0 \
            and Close under ma+atr, \
            and close > ema_trend \
            exit when price is below ema - atr"
        self.ma = ma
        self.atr_multiply = atr_multiply
        self.atr_window = atr_window
        self.lookback = lookback
    
    def add_indicator(self):
        self.df['ma'] = ta.trend.EMAIndicator(self.df['Close'], window=self.ma).ema_indicator() 
        
        self.df['upper'] = self.df['ma'] + ta.volatility.AverageTrueRange(self.df['High'], self.df['Low'], self.df['Close'], window=self.atr_window).average_true_range() * self.atr_multiply
        self.df['trailing'] = self.df['ma'].shift(1) - ta.volatility.AverageTrueRange(self.df['High'], self.df['Low'], self.df['Close'], window=14).average_true_range().shift(1) * self.atr_multiply
        # self.df['trailing'] = self.df['Close'].rolling(window=20).min()
        self.df['trailing'] = self.df['trailing'].rolling(window=2).max()
        self.df['uptrend'] = self.df['ma'] > self.df['ma'].shift(self.lookback)
        self.df = self.df.dropna()
    
    def add_signal(self):
        rule_entry = (
            (self.df['Close'] > self.df['upper']) &
            (self.df['uptrend']) 
        )
        self.df['entry_signal'] = rule_entry.astype(int)

        rule_exit = (
            (self.df['Close'] < self.df['trailing'])
        )
        self.df['exit_signal'] = rule_exit.astype(int)

        self.df['exit_partial'] = 0