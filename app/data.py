from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import os

class PriceData:
    def __init__(self, start_date:str='2018-01-01', end_date:str=datetime.today().strftime('%Y-%m-%d'), interval="1d"):
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        
    
    def get_price_file(self, ticker):
        return f'./data/price/{self.interval}/{ticker}.csv'
    
    def download_data(self,ticker):
        print(f'Download data {ticker}')
        data = yf.download(f'{ticker}.JK', start=self.start_date, end=self.end_date, progress=False, interval=self.interval)

        data2 = pd.DataFrame()
        for c in data.columns:
            data2[c[0]] = data[c[0]][f'{ticker}.JK']
        data = data2
        data.to_csv(self.get_price_file(ticker))

        return data
    
    def read_data(self, ticker):
        if not os.path.exists(self.get_price_file(ticker)):
            data = self.download_data(ticker)
        else:
            data = pd.read_csv(self.get_price_file(ticker))
            yesterday = datetime.today() - timedelta(days=2)
            # print(f'from csf : {data.tail(1).index[0]}')
            data['Date'] = pd.to_datetime(data['Date'])
            data = data.set_index('Date')
            # print(f'{data.tail(1).index[0]} - {yesterday}')
            if data.tail(1).index[0] <= yesterday:
                print("not update")
                data = self.download_data(ticker)
        
        return data
    
    def read_watchlist(self):
        # read from file
        with open('./data/watchlist.txt', 'r') as file:
            watchlist = file.read().splitlines()
        
        return watchlist