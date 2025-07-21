from polygon import RESTClient
import datetime as dt
import pandas as pd
import os


class ImportData:
    def __init__(self):
        f = open(os.path.join("data", "uwu.txt"), "r")
        api_key = f.read()
        f.close()

        self.client = RESTClient(api_key)
        self.df_main = pd.DataFrame()


    def get_one_stock_history(self, stock):
        stock_history = self.client.get_aggs(ticker = stock,
                                             multiplier = 1,
                                             timespan = "day",
                                             from_ = "2023-08-01",
                                             to = "2025-06-30")
        
        df = pd.DataFrame(stock_history)

        df = df[["high", "low", "close"]]
        df.columns = [f"{stock}_" + col for col in df.columns]

        self.df_main = pd.concat([self.df_main, df], axis=1)


    def get_all_stock_history(self, stock_list):
        for stock in stock_list:
            self.get_one_stock_history(stock)

        self.df_main.to_csv(os.path.join("data", "stock_data.csv"), index=False)



if __name__ == "__main__":
    stock_list = ["REMX", "TAN", "FAN", "ICLN", "XLE"]

    import_data = ImportData()
    import_data.get_all_stock_history(stock_list)