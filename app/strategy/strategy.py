class Strategy():
    def __init__(self, name:str):
        self.name = name

    def set_df(self, df):
        self.df = df

    def add_indicator(self):
        self.df['trailing'] = self.df['Close']

    def add_signal(self):
        self.df['entry_signal'] = 0
        self.df['exit_signal'] = 0

    def find_signal(self):
        last_5_days_signals = self.df['entry_signal'].tail(3)
        if last_5_days_signals.any():
            return True
        else:
            return False