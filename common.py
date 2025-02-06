import pandas as pd

def method_profit_analysis(stock, method):
    stock_signals = pd.concat([
        pd.DataFrame({"Price": stock.loc[stock["Signal"] == 'Buy', "Close"],
                      "Signal": stock.loc[stock["Signal"] == 'Buy', "Signal"]}),
        pd.DataFrame({"Price": stock.loc[stock["Signal"] == 'Sell', "Close"],
                      "Signal": stock.loc[stock["Signal"] == 'Sell', "Signal"]})
    ])
    stock_signals.sort_index(inplace=True)
    if stock_signals['Signal'][-1] == 'Buy':
        stock_signals.drop(stock_signals.tail(1).index, inplace=True)
    print(stock_signals)
    stock_profits = pd.DataFrame({
        "Price": stock_signals.loc[(stock_signals["Signal"] == "Buy") &
                                    stock_signals["Signal"] == 1, "Price"]
        ,
        "Profit": pd.Series(stock_signals["Price"] - stock_signals["Price"].shift(1)).loc[
            stock_signals.loc[
                (stock_signals["Signal"].shift(1) == "Buy")].index
        ].tolist()
        ,
        "End Date": stock_signals["Price"].loc[
            stock_signals.loc[
                (stock_signals["Signal"].shift(1) == "Buy")].index
        ].index
    })
    print(stock_profits)
    print(f"Length of records: {len(stock)}")
    print(f"Earning of {method}: {stock_profits['Profit'].sum()}")