from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import os
import json

class PriceData:
    def __init__(self, start_date:str='2018-01-01', end_date:str=datetime.today().strftime('%Y-%m-%d'), interval="1d"):
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.update_info = {}
        self.load_last_update()
    
    def get_price_file(self, ticker):
        return f'./data/price/{self.interval}/{ticker}.csv'
    
    def get_update_info_file(self):
        return f"./data/update-info-{self.interval}.pkl"
    
    def check_expired(self, ticker:str):
        if os.path.exists(self.get_update_info_file()):
            # print("file exist")
            today = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(minutes=1)
            if ticker in self.update_info.keys():
                if self.update_info[ticker] > today:
                    return False
            
            return True
        else :
            # print("not_exist")
            return True
    
    def load_last_update(self):
        if os.path.exists(self.get_update_info_file()):
            dict_read = json.load( open( self.get_update_info_file() ) )
            
            for key in dict_read.keys():
                self.update_info[key] = datetime.strptime(dict_read[key],'%Y-%m-%d %H:%M:%S')
        
    
    def store_last_update(self):
        store_dict = {}
        for key in self.update_info.keys():
            store_dict[key] = self.update_info[key].strftime('%Y-%m-%d %H:%M:%S')
        json.dump( store_dict, open( self.get_update_info_file(), 'w' ) )
    
    def download_data(self,ticker):
        print(f'Download data {ticker}')
        data = yf.download(f'{ticker}.JK', start=self.start_date, end=self.end_date, progress=False, interval=self.interval)

        data2 = pd.DataFrame()
        for c in data.columns:
            data2[c[0]] = data[c[0]][f'{ticker}.JK']
        data = data2
        data.to_csv(self.get_price_file(ticker))
        self.update_info[ticker] = datetime.now()
        
        return data
    
    def read_data(self, ticker):
        print(f"Read data {ticker}")
        try:
            if not os.path.exists(self.get_price_file(ticker)):
                data = self.download_data(ticker)
                print(f"{ticker} not exists")
            else:
                data = pd.read_csv(self.get_price_file(ticker))
                data['Date'] = pd.to_datetime(data['Date'])
                data = data.set_index('Date')
                # print(f'{data.tail(1).index[0]} - {yesterday}')     
                
                if self.check_expired(ticker):
                    print(f"{ticker} data needs update")
                    data = self.download_data(ticker)
                print(f"{ticker} data up to date")
            self.store_last_update()
        except Exception as e:
            print(f"Error reading data for {ticker}: {e}")
            return pd.DataFrame()
        return data
    
    def read_watchlist(self):
        # read from file
        with open('./data/watchlist.txt', 'r') as file:
            watchlist = file.read().splitlines()
        
        return watchlist