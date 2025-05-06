class Strategy():
    def __init__(self, df):
        self.df = df

    def add_indicator(self):
        self.df['trailing'] = self.df['Close']

    def add_signal(self):
        self.df['entry_signal'] = 0
        self.df['exit_signal'] = 0