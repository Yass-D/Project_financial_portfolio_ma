import pandas as pd

# Perform a Cross MA backtest (based on moving averages) for the ADDOHA financial asset


class BacktestCrossMA:
    def __init__(self) -> None:
        self.df = pd.DataFrame()

    def load_data(self, path):
        self.df = pd.read_excel(path)
        self.df["Séance"] = pd.to_datetime(self.df["Séance"], dayfirst=True)
        self.df = self.df.set_index(self.df["Séance"])
        del self.df["Séance"]
        self.df.sort_index(ascending=True, inplace=True)

    def populate_indicators(self):
        self.df["ma50"] = self.df["Dernier Cours"].rolling(50).mean()
        self.df["ma80"] = self.df["Dernier Cours"].rolling(80).mean()

    def populate_signals(self):
        self.df["buy_signal"] = False
        self.df["sell_signal"] = False
        self.df.loc[(self.df["ma50"] > self.df["ma80"]), "buy_signal"] = True
        self.df.loc[(self.df["ma50"] < self.df["ma80"]), "sell_signal"] = True

    def run_backtest(self):
        balance = 1000
        position = None
        asset = "ADDOHA"
        fees = 0.001

        for index, row in self.df.iterrows():
            if position is None and row["buy_signal"]:
                open_price = row["Dernier Cours"]
                open_size = balance
                fee = open_size * fees
                open_size = open_size - fee
                balance = balance - fee
                position = {"open_price": open_price, "open_size": open_size}
                print(f"{index} - Buy for {balance}DH of {asset} at {open_price}DH")

            elif position and row["sell_signal"]:
                close_price = row["Dernier Cours"]
                trade_result = (close_price - position["open_price"]) / position[
                    "open_price"
                ]
                close_size = (
                    position["open_size"] + position["open_size"] * trade_result
                )
                fee = close_size * fees
                close_size = close_size - fee
                balance = balance + close_size - position["open_size"]
                position = None
                print(f"{index} - Sell for {balance}DH of {asset} at {close_price}DH")

        print(f"Final balance: {round(balance,2)}DH")


bt = BacktestCrossMA()
bt.load_data("ADDOHA.xlsx")
bt.populate_indicators()
bt.populate_signals()
bt.run_backtest()
