from yahoofinancials import YahooFinancials
import pandas_datareader as web
import datetime

def chartData(ticker):
	ticker = ticker
	yahoo_financials = YahooFinancials(ticker)
	historical_stock_prices = yahoo_financials.get_historical_price_data('2017-09-03', '2019-09-15', 'daily')
	dataset = {"close": [], "dates": []}

	for daily in historical_stock_prices[ticker]['prices']:
		dataset['close'].append(round(daily['close'], 3))
		dataset['dates'].append(daily['formatted_date'])

	return dataset

def stockToCSV(ticker):
	start = datetime.datetime(2017, 9, 3)
	end = datetime.datetime(2019, 9, 15)
	df = web.DataReader(ticker, 'yahoo', start, end)
	df = df[["Open","High","Low","Close","Adj Close","Volume"]].round(2)
	df.to_csv('CSV/{}.csv'.format(ticker))
