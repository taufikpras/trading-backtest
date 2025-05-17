from app.strategies.base_strategy import BaseStrategy

class Strategy_3ema(BaseStrategy):
    def __init__(self, name, ema_short, ema_medium, ema_long):
        super().__init__(name)
        self.ema_short = ema_short
        self.ema_medium = ema_medium
        self.ema_long = ema_long

    def generate_signals(self, data):
        # Calculate EMAs
        data[f'ema_{self.ema_short}'] = data['close'].ewm(span=self.ema_short).mean()
        data[f'ema_{self.ema_medium}'] = data['close'].ewm(span=self.ema_medium).mean()
        data[f'ema_{self.ema_long}'] = data['close'].ewm(span=self.ema_long).mean()

        # Generate buy/sell signals
        data['signal'] = 0
        data.loc[
            (data[f'ema_{self.ema_short}'] > data[f'ema_{self.ema_medium}']) &
            (data[f'ema_{self.ema_medium}'] > data[f'ema_{self.ema_long}']),
            'signal'
        ] = 1  # Buy signal
        data.loc[
            (data[f'ema_{self.ema_short}'] < data[f'ema_{self.ema_medium}']) &
            (data[f'ema_{self.ema_medium}'] < data[f'ema_{self.ema_long}']),
            'signal'
        ] = -1  # Sell signal

        return data
