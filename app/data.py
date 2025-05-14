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
        return f"./data/update-info-{self.interval}.json"
    
    def check_expired(self, ticker:str, data:pd.DataFrame):
        if os.path.exists(self.get_update_info_file()):
            # print("file exist")
            today = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(minutes=1)
            if ticker in self.update_info.keys():
                if data.empty == False:
                    if self.update_info[ticker]["last_update"] > today:
                        if self.update_info[ticker]["start_date"] > datetime.strptime(self.start_date, '%Y-%m-%d'):
                            return True
                        else:
                            return False
            
            return True
        else :
            # print("not_exist")
            return True
    
    def load_last_update(self):
        if os.path.exists(self.get_update_info_file()):
            dict_read = json.load( open( self.get_update_info_file() ) )
            
            for key in dict_read.keys():
                self.update_info[key] = {}
                self.update_info[key]["last_update"] = datetime.strptime(dict_read[key]["last_update"],'%Y-%m-%d %H:%M:%S')
                self.update_info[key]["start_date"] = datetime.strptime(dict_read[key]["start_date"],'%Y-%m-%d')
        else:
            self.update_info = {}
        
    def store_last_update(self):
        store_dict = {}
        for key in self.update_info.keys():
            store_dict[key] = {}
            store_dict[key]["last_update"] = self.update_info[key]["last_update"].strftime('%Y-%m-%d %H:%M:%S')
            store_dict[key]["start_date"] = self.update_info[key]["start_date"].strftime('%Y-%m-%d')
        json.dump( store_dict, open( self.get_update_info_file(), 'w' ) )
    
    def download_data(self,ticker):
        print(f'Download data {ticker}')
        data = yf.download(f'{ticker}.JK', start=self.start_date, end=self.end_date, progress=False, interval=self.interval)

        data2 = pd.DataFrame()
        for c in data.columns:
            data2[c[0]] = data[c[0]][f'{ticker}.JK']
        data = data2
        if data.empty == False:
            data.to_csv(self.get_price_file(ticker))
        
        print(f"Downloaded {ticker} data")
        print(f"update metadata info for {ticker}")
        self.update_info[ticker] = {}
        self.update_info[ticker]["last_update"] = datetime.now()
        self.update_info[ticker]["start_date"] = datetime.strptime(self.start_date,'%Y-%m-%d')
        
        return data
    
    def read_data(self, ticker):
        print(f"Read data {ticker}")
        try:
            if not os.path.exists(self.get_price_file(ticker)):
                data = self.download_data(ticker)
                print(f"{ticker} not exists")
            else:
                
                try:
                    data = pd.read_csv(self.get_price_file(ticker))
                except Exception as e:
                    print(f"Error reading CSV for {ticker}: {e}")
                    data = pd.DataFrame()
                
                data['Date'] = pd.to_datetime(data['Date'])
                data = data.set_index('Date')
                # print(f'{data.tail(1).index[0]} - {yesterday}')     
                
                if self.check_expired(ticker, data):
                    print(f"{ticker} data needs update")
                    data_update = self.download_data(ticker)
                    if data_update.empty == False:
                        data = data_update
                print(f"{ticker} data up to date")
            self.store_last_update()
        except Exception as e:
            print(f"Error reading data for {ticker}: {e.with_traceback()}")
            return pd.DataFrame()
        return data
    
    def read_watchlist(self):
        # read from file
        with open('./data/watchlist.txt', 'r') as file:
            watchlist = file.read().splitlines()
        
        return watchlist