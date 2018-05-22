from stockReporter import *



class stockUI:

    def get_report(self):
        yahooStockPriceService = YahooStockPriceService()
        stockReporter = StocksReporter()
        stockReporter.set_stock_price_service(yahooStockPriceService)
        stocks = []
        i = 0
        j = 0
        getFile = True

        while (getFile) :
            try:
                print("Please enter user stock record file name. (we have create stock record 'stocks.txt')")
                file_Name = input()



                with open(file_Name, "r") as stocks_info_file:
                    stocks_info = csv.reader(stocks_info_file, delimiter=" ")
                    for line in stocks_info:
                        stocks.append(Stock())
                        stocks[i].symbol = line[0]
                        stocks[i].number_of_shares = int(line[1])
                        i = i + 1
                getFile = False
            except FileNotFoundError:
                print("it is not correct file name.Please enter again")

        stocks = stockReporter.get_asset_values(stocks)

        print("{0:9} {1:11} {2:18}".format("Symbol", "Shares", "Net Asset Value"))
        stocks_with_error = []
        prices = []
        number_of_shares = []
        for stock in stocks:
            if(stock.price == 0):
                stocks_with_error.append(Stock())
                stocks_with_error[j].symbol = stock.symbol
                stocks_with_error[j].error = stock.error
                j = j + 1
            else:
                prices.append(stock.price)
                number_of_shares.append(stock.number_of_shares)
                print("{0: <10}{1: <12}{2: <18}".format(stock.symbol, stock.number_of_shares, format(stock.asset_value,'.2f')))
        
        total = stockReporter.calculate_net_asset_value(prices, number_of_shares)
        print("------------------------------------------------------------------------------")
        print("{0: <21} {1:18}" .format("Total", format(total, '.2f')))


        print("")
        print("Errors:")
        for error in stocks_with_error:
            print("{0:10} {1:30}" .format(error.symbol, error.error))



UI = stockUI()
UI.get_report()