from app.strategies.strategy import Strategy
import ta

class Strategy_Ema_High_Low(Strategy):
    def __init__(self, name, ema_length = 8):
        if name is None:
            name = f"Ema_High_Low {ema_length}"
        super().__init__(name)
        self.description = "entry when close > ema_high \
            and di >0 \
            exit when price is below ema - atr"
        self.ema_length = ema_length
    
    def add_indicator(self):
        self.df['ema_main'] = ta.trend.EMAIndicator(self.df['Close'], window=self.ema_length).ema_indicator()
        self.df['ema_high'] = ta.trend.EMAIndicator(self.df['High'], window=self.ema_length).ema_indicator()
        self.df['ema_low'] = ta.trend.EMAIndicator(self.df['Low'], window=self.ema_length).ema_indicator()
        self.df['trailing'] = self.df['ema_main'].shift(1) - ta.volatility.AverageTrueRange(self.df['High'], self.df['Low'], self.df['Close'], window=14).average_true_range().shift(1)
        self.df['trailing'] = self.df['trailing'].rolling(window=2).max()
        self.df['di'] = ta.trend.ADXIndicator(self.df['High'], self.df['Low'], self.df['Close'], window=14).adx_pos() -  ta.trend.ADXIndicator(self.df['High'], self.df['Low'], self.df['Close'], window=14).adx_neg()
        self.df = self.df.dropna()
    
    def add_signal(self):
        rule_entry = (
            (self.df['Close'] > self.df['ema_high']) &
            (self.df['Close'] > self.df['ema_main']) &
            (self.df['di'] > 0)
        )
        self.df['entry_signal'] = rule_entry.astype(int)

        rule_exit = (
            (self.df['Close'] < self.df['trailing'])
        )
        self.df['exit_signal'] = rule_exit.astype(int)

        self.df['exit_partial'] = 0