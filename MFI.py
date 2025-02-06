import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore')
from common import method_profit_analysis
################################################################
period = 14
NVIDIA = pd.read_csv("data_source/stocks_NVDA.csv",index_col=['Date'])
def buy_sell_mfi(signal, high=80, low=20):
  Signal = []
  flag = -1
  for i in range(0, len(signal)):
    if signal['MFI'][i] < low:
        if flag != 1:
            Signal.append('Buy')
            flag = 1
        else:
            Signal.append(np.nan)
    else:
        if flag == 1:
            Signal.append('Sell')
            flag = 0
        else:
            Signal.append(np.nan)
  return Signal
################################################################
typical_price = (NVIDIA['Close'] + NVIDIA['High'] + NVIDIA['Low']) / 3
money_flow = typical_price * NVIDIA['Volume']
positive_flow = []
negative_flow = []
for i in range(1, len(typical_price)):
  if typical_price[i] > typical_price[i-1]:
    positive_flow.append(money_flow[i-1])
    negative_flow.append(0)
  elif typical_price[i] < typical_price[i-1]:
    negative_flow.append(money_flow[i-1])
    positive_flow.append(0)
  else:
    positive_flow.append(0)
    negative_flow.append(0)
positive_mf = []
negative_mf = []
for i in range(period-1, len(positive_flow)):
  positive_mf.append(sum(positive_flow[i + 1 - period : i+1]))
for i in range(period-1, len(negative_flow)):
  negative_mf.append(sum(negative_flow[i + 1 - period : i+1]))
mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))
NVIDIA_new = NVIDIA[period:]
NVIDIA_new['MFI'] = mfi
NVIDIA_new['Signal'] = buy_sell_mfi(NVIDIA_new)
print(NVIDIA_new)
################################################################
method_profit_analysis(NVIDIA_new,"MFI")