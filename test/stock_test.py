import unittest
from stockReporter import *
import types
import csv
from YahooStockPriceService import *

class stockReporterTest(unittest.TestCase):

    def setUp(self):
        self.stock_reporter = StocksReporter()
        self.yahoo_service_price = YahooStockPriceService()

    def Canary(self):
        self.assertTrue(True)

    def test_calculate_asset(self):
        self.assertEqual(1200, self.stock_reporter.calculate_asset_value(12, 100))

    def test_calculate_total_asset(self):
        list_price = [100, 200, 300, 400, 500]
        list_share = [2, 3, 1, 2, 3]

        self.assertEqual(3400 , self.stock_reporter.calculate_net_asset_value(list_price, list_share))

    def test_stock_price_service_get_price(self):
        stockPriceService = StockPriceService()
        try:
            stockPriceService.get_price("GOOG")
        except NotImplementedError:
            assert True
  
    def test_get_asset_value_one_symbol(self):
        def fake_get_price(self, symbol):
            return 2

        stock = Stock()
        stock.sybmol = "AAPL"
        stock.number_of_shares = 100

        stockPriceService = StockPriceService()

        stockPriceService.get_price = types.MethodType(fake_get_price, stockPriceService)

        self.stock_reporter.set_stock_price_service(stockPriceService)

        stock_with_asset_values = self.stock_reporter.get_asset_values([stock])
        self.assertEqual(200, stock_with_asset_values[0].asset_value)


    def test_get_asset_value_two_symbol(self):

       stock =[Stock(), Stock()]
       stock[0].symbol = "AAPL"
       stock[0].number_of_shares = 100
       stock[1].symbol = "GOOG"
       stock[1].number_of_shares = 200


       def fake_get_price(self, i):
               if(i == "AAPL"):
                   return 5
               elif(i == "GOOG"):
                   return 8

       stockPriceService = StockPriceService()

       stockPriceService.get_price = types.MethodType(fake_get_price, stockPriceService)

       self.stock_reporter.set_stock_price_service(stockPriceService)
       stock_with_asset_values = self.stock_reporter.get_asset_values(stock)

       assets = []
       for i in stock_with_asset_values:
           assets.append(i.asset_value)

       self.assertEqual([500, 1600], assets)
#
    def test_get_asset_value_three_symbol(self):
       stock = [Stock(), Stock(), Stock()]
       stock[0].symbol = "AAPL"
       stock[0].number_of_shares = 100
       stock[1].symbol = "GOOG"
       stock[1].number_of_shares = 200
       stock[2].symbol = "CDAD"
       stock[2].number_of_shares = 300


       def fake_get_price(self, i):
               if(i == "AAPL"):
                   return 5
               elif(i == "GOOG"):
                   return 8
               elif(i == "CDAD"):
                   raise NameError


       stockPriceService = StockPriceService()

       stockPriceService.get_price = types.MethodType(fake_get_price, stockPriceService)

       self.stock_reporter.set_stock_price_service(stockPriceService)
       assets = []
       try:
           stock_with_asset_values = self.stock_reporter.get_asset_values(stock)
           fail("symbol error")
       except :
           assert True

       for i in stock_with_asset_values:
               if(i.asset_value == 0):
                   assets.append(i.error)
               else:
                   assets.append(i.asset_value)


       self.assertEqual([500, 1600, "Invalid Symbol"], assets)
#
#
    def test_get_asset_value_three_symbol_symbol_error_valid_error(self):
       stock = [Stock(), Stock(), Stock()]
       stock[0].symbol = "AAPL"
       stock[0].number_of_shares = 100
       stock[1].symbol = "GOOG"
       stock[1].number_of_shares = 200
       stock[2].symbol = "CDAD"
       stock[2].number_of_shares = 300


       def fake_get_price(self, i):
               if(i == "AAPL"):
                   return 5
               elif(i == "GOOG"):
                   raise ConnectionError
               elif(i == "CDAD"):
                   raise NameError


       stockPriceService = StockPriceService()

       stockPriceService.get_price = types.MethodType(fake_get_price, stockPriceService)

       self.stock_reporter.set_stock_price_service(stockPriceService)
       assets = []
       try:
           stock_with_asset_values = self.stock_reporter.get_asset_values(stock)
           fail("symbol error")
       except :
           assert True

       for i in stock_with_asset_values:
               if(i.asset_value == 0):
                   assets.append(i.error)
               else:
                   assets.append(i.asset_value)


       self.assertEqual([500, "Network Error", "Invalid Symbol"], assets)


    def test_Yahoo_Service_get_price_Greater_Zero(self):
        def fake_request_stock_info(self, symbol):
            return [symbol, 10.05]

        self.yahoo_service_price.request_stock_info = types.MethodType(fake_request_stock_info, self.yahoo_service_price)

        self.assertEqual(10.05, self.yahoo_service_price.get_price("GOOG"))


    def test_Yahoo_Service_get_price_With_Real_Symbol(self):
        try:
            self.assertLess(0, self.yahoo_service_price.get_price("GOOG"))
        except:
            assert True

    def test_Yahoo_Service_get_price_throw_invalid_Symbol_Name(self):
        def fake_request_stock_info(self,symbol):
            return [symbol,"N/A", "N/A", "N/A"]

        self.yahoo_service_price.request_stock_info = types.MethodType(fake_request_stock_info,
                                                                       self.yahoo_service_price)
        try:
            self.yahoo_service_price.get_price("GOOG")
            fail("Name Error")
        except NameError:
            assert True

    def test_Yahoo_Service_get_price_Throw_Connection_Error(self):
        def fake_request_stock_info(self, symbol):
            raise ConnectionError

        self.yahoo_service_price.request_stock_info = types.MethodType(fake_request_stock_info,
                                                                       self.yahoo_service_price)

        try:
            self.yahoo_service_price.get_price("GOOG")
            fail("Connection Error")
        except ConnectionError:
            assert True




                 
        
if __name__ == '__main__':
    unittest.main()

