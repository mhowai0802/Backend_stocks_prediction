import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore')
from common import method_profit_analysis
################################################################
NVIDIA = pd.read_csv("data_source/stocks_NVDA.csv",index_col=['Date'])
################################################################
NVIDIA['L14'] = NVIDIA['Low'].rolling(window=14).min()
#Create the "H14" column in the DataFrame
NVIDIA['H14'] = NVIDIA['High'].rolling(window=14).max()
#Create the "%K" column in the DataFrame
NVIDIA['%K'] = 100*((NVIDIA['Close'] - NVIDIA['L14']) / (NVIDIA['H14'] - NVIDIA['L14']) )
#Create the "%D" column in the DataFrame
NVIDIA['%D'] = NVIDIA['%K'].rolling(window=3).mean()
conditions = [
    ((NVIDIA['%K'] > NVIDIA['%D']) & (NVIDIA['%K'].shift(1) < NVIDIA['%D'].shift(1)) & (NVIDIA['%D'] < 20)),
    ((NVIDIA['%K'] < NVIDIA['%D']) & (NVIDIA['%K'].shift(1) > NVIDIA['%D'].shift(1)))
]
# Define the corresponding choices:
choices = ['Buy', 'Sell']
# Use np.select to create the new column:
NVIDIA['Signal'] = np.select(conditions, choices, default='None')
print(NVIDIA)
################################################################
method_profit_analysis(NVIDIA,'Stochastic_Oscillator')