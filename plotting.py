import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os



class Plotting:
    def __init__(self):
        self.df = pd.read_csv(os.path.join("data", "simulation.csv"))
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])

        self.stock_list = ["TAN", "FAN", "ICLN", "XLE"]


    def main(self):
        for stock in self.stock_list:
            self.plot(stock, "return")


    def plot(self, stock, type):
        column = f"{stock}_{type}"

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(self.df["timestamp"], self.df[column])

        # Format x-axis with month ticks
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.xticks(rotation=45)

        # Get y max value for label placement
        y_max = self.df[column].max()

        # Event 1: Aug 1 – Oct 1, 2024
        start_event1 = pd.to_datetime("2024-08-01")
        end_event1 = pd.to_datetime("2024-10-01")
        ax.axvspan(start_event1, end_event1, color="orange", alpha=0.3)

        # Add vertical label near mid-August at top
        event1_label_x = pd.to_datetime("2024-08-10")
        ax.text(event1_label_x, y_max, "China tightens export controls on REEs",
                rotation=90, fontsize=10, color="orange",
                verticalalignment='top', horizontalalignment='center')

        # Event 2: vertical line at April 2, 2025
        event2_date = pd.to_datetime("2025-04-02")
        ax.axvline(event2_date, color="red", linestyle="--", linewidth=2)

        # Add label slightly to the right of the line at top
        event2_label_x = event2_date + pd.Timedelta(days=5)
        ax.text(event2_label_x, y_max, "US announces wide-ranging tariffs",
                rotation=90, fontsize=10, color="red",
                verticalalignment='top', horizontalalignment='left')

        # Labels and layout
        plt.xlabel("Month")
        plt.ylabel("Spillover")
        plt.title(f"Spillover from REMX to {stock} ({type})")
        plt.tight_layout()

        plt.savefig(os.path.join("plots", f"{column}.png"))



if __name__ == "__main__":
    plot = Plotting()
    plot.main()
