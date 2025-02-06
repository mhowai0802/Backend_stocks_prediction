import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.patches as mpatches
from matplotlib.dates import date2num, DateFormatter, WeekdayLocator, \
    DayLocator, MONDAY
import seaborn as sns
import datetime
from datetime import date, timedelta
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
################################################################
NVIDIA = pd.read_csv("data_source/stocks_NVDA_new.csv", index_col=['Date'])
################################################################
def MA(stock):
    NVIDIA["20d"] = np.round(NVIDIA["Close"].rolling(window=20, center=False).mean(), 2)
    NVIDIA["200d"] = np.round(NVIDIA["Close"].rolling(window=200, center=False).mean(), 2)
    NVIDIA['20d-200d'] = NVIDIA['20d'] - NVIDIA['200d']
    NVIDIA["Regime"] = np.where(NVIDIA['20d-200d'] > 0, 1, 0)
    NVIDIA["Regime"] = np.where(NVIDIA['20d-200d'] < 0, -1, NVIDIA["Regime"])
    regime_orig = NVIDIA.iloc[-1]['Regime']
    NVIDIA.iloc[-1]['Regime'] = 0
    NVIDIA["Signal"] = np.sign(NVIDIA["Regime"] - NVIDIA["Regime"].shift(1))
    NVIDIA.iloc[-1]['Regime'] = regime_orig
    print(NVIDIA.tail())
    print(NVIDIA["Signal"].value_counts())
    ################################################################
    NVIDIA_signals = pd.concat([
        pd.DataFrame({"Price": NVIDIA.loc[NVIDIA["Signal"] == 1, "Close"],
                      "Regime": NVIDIA.loc[NVIDIA["Signal"] == 1, "Regime"],
                      "Signal": "Buy"}),
        pd.DataFrame({"Price": NVIDIA.loc[NVIDIA["Signal"] == -1, "Close"],
                      "Regime": NVIDIA.loc[NVIDIA["Signal"] == -1, "Regime"],
                      "Signal": "Sell"}),
    ])
    NVIDIA_signals.sort_index(inplace=True)
    print(NVIDIA_signals)
    NVIDIA_profits = pd.DataFrame({
        "Price": NVIDIA_signals.loc[(NVIDIA_signals["Signal"] == "Buy") &
                                    NVIDIA_signals["Regime"] == 1, "Price"]
        ,
        "Profit": pd.Series(NVIDIA_signals["Price"] - NVIDIA_signals["Price"].shift(1)).loc[
            NVIDIA_signals.loc[
                (NVIDIA_signals["Signal"].shift(1) == "Buy") & (NVIDIA_signals["Regime"].shift(1) == 1)].index
        ].tolist()
        ,
        "End Date": NVIDIA_signals["Price"].loc[
            NVIDIA_signals.loc[
                (NVIDIA_signals["Signal"].shift(1) == "Buy") & (NVIDIA_signals["Regime"].shift(1) == 1)].index
        ].index
    })

    print(f"Length of records: {len(NVIDIA)}")
    print(f"Earning of MA 20-200days: {NVIDIA_profits['Profit'].sum()}")
