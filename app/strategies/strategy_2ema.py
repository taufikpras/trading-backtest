from app.strategies.strategy import Strategy
import ta

class Strategy_2ema(Strategy):
    def __init__(self, name, ema_main = 8, ema_trend = 200):
        super().__init__(name)
        self.description = "entry when  \
            and ema_main > ema_trend \
            and di >0 \
            and Close under ema_main+atr, \
            and close > ema_trend \
            exit when price is below ema - atr"
        self.ema_main = ema_main
        self.ema_trend = ema_trend
    
    def add_indicator(self):
        self.df['ema_main'] = ta.trend.EMAIndicator(self.df['Close'], window=self.ema_main).ema_indicator() 
        self.df['ema_trend'] = ta.trend.EMAIndicator(self.df['Close'], window=self.ema_trend).ema_indicator()        
        self.df['upper'] = self.df['ema_main'] + ta.volatility.AverageTrueRange(self.df['High'], self.df['Low'], self.df['Close'], window=14).average_true_range()
        self.df['trailing'] = self.df['ema_main'].shift(1) - ta.volatility.AverageTrueRange(self.df['High'], self.df['Low'], self.df['Close'], window=14).average_true_range().shift(1)
        self.df['trailing'] = self.df['trailing'].rolling(window=2).max()
        self.df['di'] = ta.trend.ADXIndicator(self.df['High'], self.df['Low'], self.df['Close'], window=14).adx_pos() -  ta.trend.ADXIndicator(self.df['High'], self.df['Low'], self.df['Close'], window=14).adx_neg()
        self.df = self.df.dropna()
    
    def add_signal(self):
        rule_entry = (
            (self.df['Close'] < self.df['upper']) &
            (self.df['Close'] > self.df['ema_trend']) &
            (self.df['ema_main'] > self.df['ema_trend']) &
            (self.df['di'] > 0)
        )
        self.df['entry_signal'] = rule_entry.astype(int)

        rule_exit = (
            (self.df['Close'] < self.df['trailing'])
        )
        self.df['exit_signal'] = rule_exit.astype(int)

        self.df['exit_partial'] = 0