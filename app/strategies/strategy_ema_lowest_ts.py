from app.strategies.strategy import Strategy
import ta

class Strategy_Close_Ema_Lowest_TS(Strategy):
    def __init__(self, name=None, ema_length = 8, ts_length = 20):
        if name is None:
            name = f"EMAWithTS {ema_length} {ts_length}"
        super().__init__(name)
        self.description = "entry when close > ema \
            and di >0 \
            and Close under ema+atr, \
            exit when price is below lowest ts"
        self.ema_length = ema_length
        self.ts_length = ts_length
    
    def add_indicator(self):
        self.df['ema_main'] = ta.trend.EMAIndicator(self.df['Close'], window=self.ema_length).ema_indicator()        
        self.df['upper'] = self.df['ema_main'] + ta.volatility.AverageTrueRange(self.df['High'], self.df['Low'], self.df['Close'], window=14).average_true_range()
        self.df['trailing'] = self.df['Close'].rolling(window=self.ts_length).min()
        self.df['trailing'] = self.df['trailing'].rolling(window=2).max()
        self.df['di'] = ta.trend.ADXIndicator(self.df['High'], self.df['Low'], self.df['Close'], window=14).adx_pos() -  ta.trend.ADXIndicator(self.df['High'], self.df['Low'], self.df['Close'], window=14).adx_neg()
        self.df = self.df.dropna()
    
    def add_signal(self):
        rule_entry = (
            (self.df['Close'] < self.df['upper']) &
            (self.df['Close'] > self.df['ema_main']) &
            (self.df['di'] > 0)
        )
        self.df['entry_signal'] = rule_entry.astype(int)

        rule_exit = (
            (self.df['Close'] < self.df['trailing'])
        )
        self.df['exit_signal'] = rule_exit.astype(int)

        self.df['exit_partial'] = 0