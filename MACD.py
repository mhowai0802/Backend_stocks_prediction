import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore')
from common import method_profit_analysis
################################################################
NVIDIA = pd.read_csv("data_source/stocks_NVDA_new.csv",index_col=['Date'])
def buy_sell_macd(signal):
  Signal = []
  flag = -1
  for i in range(0, len(signal)):
    if signal['MACD'][i] > signal['Signal Line'][i]:
        if flag != 1:
            Signal.append('Buy')
            flag = 1
        else:
            Signal.append(np.nan)
    elif signal['MACD'][i] < signal['Signal Line'][i]:
        if flag == 1:
            Signal.append('Sell')
            flag = 0
        else:
            Signal.append(np.nan)
    else:
      Signal.append(np.nan)

  return Signal
################################################################
ShortEMA = NVIDIA['Close'].ewm(span=12, adjust=False).mean()
LongEMA = NVIDIA['Close'].ewm(span=26, adjust=False).mean()
MACD = ShortEMA - LongEMA
signal = MACD.ewm(span=9, adjust=False).mean()
NVIDIA['MACD'] = MACD
NVIDIA['Signal Line'] = signal
NVIDIA['Signal'] = buy_sell_macd(NVIDIA)
print(NVIDIA)
################################################################
method_profit_analysis(NVIDIA, 'MACD')