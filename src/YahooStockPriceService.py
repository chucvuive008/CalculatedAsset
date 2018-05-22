import requests
from requests.exceptions import *

class YahooStockPriceService:
    def request_stock_info(self, Symbol):

            stock_info_url =  "http://download.finance.yahoo.com/d/quotes.csv?s=" + Symbol + "&f=snbaopl1"
            stocks_info = requests.get(stock_info_url).text.strip().split(",")
            return stocks_info

    def get_price(self,Symbol):
        try:
            stocks_info = self.request_stock_info(Symbol)
            if (stocks_info[-1] =='N/A'):
                raise NameError
            return float(stocks_info[-1])
        except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
            raise ConnectionError
