import csv
from StockPriceService import *
from stock import *
import requests
from YahooStockPriceService import*
    


class StocksReporter:        
    def calculate_asset_value(self, price_in_cents, number_of_shares): 
        return price_in_cents * number_of_shares 


    def calculate_net_asset_value(self, price_in_cents, number_of_shares):
        return sum(map(lambda i: self.calculate_asset_value(price_in_cents[i], number_of_shares[i]), range(len(price_in_cents))))
    
    def get_asset_value_for_stock(self, stock):
        new_stock = Stock()
        new_stock.symbol = stock.symbol
        new_stock.number_of_shares = stock.number_of_shares

        try:                                   
            new_stock.price = self.stockPriceService.get_price(new_stock.symbol)
            new_stock.asset_value = self.calculate_asset_value(new_stock.price, new_stock.number_of_shares)
        except NameError:
             new_stock.error = "Invalid Symbol"
        except ConnectionError:
            new_stock.error = "Network Error"
            
        return new_stock

    def get_asset_values(self, stocks):
        return list(map(self.get_asset_value_for_stock, stocks))

    
    def set_stock_price_service(self, stockService):
        self.stockPriceService = stockService


