import numpy as np
import pandas as pd
import os



class Simulation:
    def __init__(self):
        self.df = pd.read_csv(os.path.join("data", "stock_data.csv"))
        self.stock_list = ["REMX", "TAN", "FAN", "ICLN", "XLE"]
        self.length = len(self.df)
        # Length should be 374. Index goes from 1 to 374 (meaning we use 1-index array).


    def main(self):
        self.load_data()
        self.compute_returns()
        self.compute_votality()


    def load_data(self):
        self.close = {}
        self.high = {}
        self.low = {}

        for stock in self.stock_list:
            self.close[stock] = np.empty(self.length + 1)
            self.high[stock] = np.empty(self.length + 1)
            self.low[stock] = np.empty(self.length + 1)

            self.close[stock][1:] = self.df[f"{stock}_close"].to_numpy()
            self.high[stock][1:] = self.df[f"{stock}_high"].to_numpy()
            self.low[stock][1:] = self.df[f"{stock}_low"].to_numpy()

    
    def compute_returns(self):
        self.returns = {}

        for stock in self.stock_list:
            self.returns[stock] = np.empty(self.length + 1)

            for i in range(2, self.length + 1):
                self.returns[stock][i] = np.log10(self.close[stock][i] / self.close[stock][i-1])

        print(self.returns["REMX"])


    def compute_votality(self):
        self.votality = {}

        for stock in self.stock_list:
            self.votality[stock] = np.empty(self.length + 1)

            sum = np.float64(0)
            for i in range(1, self.length + 1):
                sum += np.log(self.high[stock][i] / self.low[stock][i]) / (4 * np.log(2))
                self.votality[stock][i] = np.sqrt(sum / i)

        print(self.votality["REMX"])


        
########################################


if __name__ == "__main__":
    sim = Simulation()
    sim.main()