import numpy as np
import pandas as pd
import os



class Simulation:
    def __init__(self):
        self.df_data = pd.read_csv(os.path.join("data", "stock_data.csv"))
        self.stock_list = ["REMX", "TAN", "FAN", "ICLN", "XLE"]

        self.length = len(self.df_data)
        print(f"Length: {self.length}")
        # Length should be 480. Index goes from 1 to 480 (meaning we use 1-index array).

        self.roll = 200

        self.df_simulation = pd.DataFrame(index=range(self.length - self.roll))

        self.df_simulation["timestamp"] = self.df_data.loc[200:479, "timestamp"].reset_index(drop=True)

        for stock in self.stock_list[1:]:
            self.df_simulation[f"{stock}_return"] = pd.NA
            self.df_simulation[f"{stock}_volatility"] = pd.NA

        # print(self.df_simulation)


    def main(self):
        for day in range(self.roll, self.length):
            self.process_day(day, "return")
            self.process_day(day, "volatility")

        print(self.df_simulation.head(10))
        self.df_simulation.to_csv(os.path.join("data", "simulation.csv"), index=False)


    def process_day(self, day, type):
        self.load_data(day)
        self.compute_returns()
        self.compute_volatility()
        self.compute_error(type)
        self.compute_covariance()
        self.compute_GFEVD()
        self.normalize_GFEVD()
        self.compute_spillover()

        for stock in self.stock_list[1:]:
            self.df_simulation.at[day - self.roll, f"{stock}_{type}"] = self.spillover[stock]

        # print(self.df_simulation.iloc[0].to_dict())


    def load_data(self, day):
        """
        Create the close, high, and low array for each stock.
        Each array has length self.roll
        Each array correspond to the day range of (day - self.rool + 1, day).
        """
        self.close = {}
        self.high = {}
        self.low = {}

        # print(f"Range: {day - self.roll + 1} - {day}")

        for stock in self.stock_list:
            self.close[stock] = self.df_data[f"{stock}_close"].to_numpy()
            self.high[stock] = self.df_data[f"{stock}_high"].to_numpy()
            self.low[stock] = self.df_data[f"{stock}_low"].to_numpy()

            # Right now, the arrays are of length self.length
            # Index i in the array correspond to day i+1
            # We want the range of days from day - self.roll + 1, to day
            # The indices we want are from day - self.roll, to day - 1
            # Hence, the slicing is [day - self.roll, day]

            self.close[stock] = self.close[stock][day - self.roll : day]
            self.high[stock] = self.high[stock][day - self.roll : day]
            self.low[stock] = self.low[stock][day - self.roll : day]

        # print("Close: ", len(self.close["REMX"]), self.close["REMX"])

    
    def compute_returns(self):
        """
        Create the return array with size self.roll
        The first element is obsolete.
        """
        self.returns = {}

        for stock in self.stock_list:
            self.returns[stock] = np.empty(self.roll)

            for i in range(1, self.roll):
                self.returns[stock][i] = np.log10(self.close[stock][i] / self.close[stock][i-1])

        # print("Returns: ", len(self.returns["REMX"]), self.returns["REMX"])


    def compute_volatility(self):
        """
        Create the volatility array with size self.roll
        """
        self.volatility = {}

        for stock in self.stock_list:
            self.volatility[stock] = np.empty(self.roll)

            sum = np.float64(0)
            for i in range(self.roll):
                sum += np.log(self.high[stock][i] / self.low[stock][i]) / (4 * np.log(2))
                self.volatility[stock][i] = np.sqrt(sum / (i+1))

        # print("Volatility: ", len(self.volatility["REMX"]), self.volatility["REMX"])


    def compute_error(self, type):
        """
        Compute the error term for either "return" or "volatility".
        Create the error array with length self.roll
        The first element is obsolete.
        """
        self.error = {}

        for stock in self.stock_list:
            self.error[stock] = np.empty(self.roll)

            for i in range(2, self.roll):
                if type == "return":
                    self.error[stock][i] = self.returns[stock][i] - self.returns[stock][i-1]
                elif type == "volatility":
                    self.error[stock][i] = self.volatility[stock][i] - self.volatility[stock][i-1]
                else:
                    raise NameError()

        # print("Error: ", len(self.error["REMX"]), self.error["REMX"])


    def compute_covariance(self):
        data = np.stack([self.error[stock][2:] for stock in self.stock_list])

        self.covar = np.cov(data)

        # print("Covariance: ", self.covar)


    def compute_GFEVD(self):
        self.GFEVD = np.empty((5, 5))

        for i in range(5):
            for j in range(5):
                eps_i = np.zeros((5, 1))
                eps_i[i, 0] = 1

                eps_j = np.zeros((5, 1))
                eps_j[j, 0] = 1

                sigma = self.covar[i, i]

                self.GFEVD[i, j] = ((10 / sigma) * (eps_i.T @ self.covar @ eps_j)).item()

        # print("GFEVD: ", self.GFEVD)


    def normalize_GFEVD(self):
        for i in range(5):
            sum = 0
            for j in range(5):
                sum += self.GFEVD[i, j]
            
            for j in range(5):
                self.GFEVD[i, j] /= sum

        # print("GFEVD: ", self.GFEVD)


    def compute_spillover(self):
        self.spillover = {}
        for j in range(1, 5):
            spillover_val = self.GFEVD[j, 0] - self.GFEVD[0, j]
            self.spillover[self.stock_list[j]] = spillover_val

        # print("Spillover: ", self.spillover)



        
########################################


if __name__ == "__main__":
    sim = Simulation()
    sim.main()

    # sim.process_day(200, "return")