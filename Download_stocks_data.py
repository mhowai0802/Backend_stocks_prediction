from datetime import date
import yfinance as yf
from datetime import timedelta

stocks = ['NVDA']
end_date = date.today() - timedelta(days = 1)
for stock in stocks:
    stock_tick = yf.Ticker(stock)
    stocks_info = stock_tick.history(period="30d", interval="5m")
    stocks_info['Date'] = stocks_info.index.strftime('%Y-%m-%d %H:%M:%S')
    stocks_info.to_csv(f"data_source/stocks_{stock}_5min.csv")