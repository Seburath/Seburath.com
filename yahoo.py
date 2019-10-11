from yahoofinancials import YahooFinancials


def chartData(ticker):
	ticker = ticker
	yahoo_financials = YahooFinancials(ticker)
	historical_stock_prices = yahoo_financials.get_historical_price_data('2018-09-03', '2019-09-15', 'daily')
	dataset = {"close": [], "dates": []}

	for daily in historical_stock_prices[ticker]['prices']:
		dataset['close'].append(round(daily['close'], 3))
		dataset['dates'].append(daily['formatted_date'])

	return dataset
