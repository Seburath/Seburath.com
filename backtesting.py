from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime
import backtrader as bt
from yahoo import stockToCSV

tradeLog = {'trades': []}

class TestStrategy(bt.Strategy):
	def log(self, txt, dt=None):
		dt = dt or self.datas[0].datetime.date(0)
		msgLog = '%s, %s' % (dt.isoformat(), txt)
		#print(msgLog)

	def __init__(self):
		self.dataclose = self.datas[0].close

	def notify_order(self, order):
		if order.status in [order.Completed]:
			if order.isbuy():
				msg = ('BUY EXECUTED, Price: %.2f, Cost: %.2f' %
                    (order.executed.price,
                     order.executed.value))
				self.log(msg)				

				self.buyprice = order.executed.price
				self.buycomm = order.executed.comm
			else: 
				msg = ('SELL EXECUTED, Price: %.2f, Cost: %.2f' %
                         (order.executed.price,
                          order.executed.value))
				self.log(msg)

			self.bar_executed = len(self)

		elif order.status in [order.Canceled, order.Margin, order.Rejected]:
			self.log('Order Canceled/Margin/Rejected')

		self.order = None

	def next(self):
		if not self.position:
			if self.dataclose[0] < self.dataclose[-1]:
				diff = 1-(self.dataclose[-1]/self.dataclose[0])
				if diff <= -0.10:
					msg = 'BUY CREATE, %.2f' % self.dataclose[0]
					self.log(msg)
					tradeLog['trades'].append(msg)
					self.order = self.buy(size=50)
		else:
			msg = 'SELL CREATE, %.2f' % self.dataclose[0]
			self.log(msg)
			tradeLog['trades'].append(msg)
			self.order = self.sell(size=50)


def execute_backtest(symbol):
	stockToCSV(symbol)
	cerebro = bt.Cerebro()
	cerebro.broker.setcash(100000.0)
	cerebro.addstrategy(TestStrategy)
	data = bt.feeds.YahooFinanceCSVData(
        dataname='CSV/{}.csv'.format(symbol),
        fromdate=datetime.datetime(2017, 9, 3),
        todate=datetime.datetime(2019, 9, 15),
        reverse=False)
	cerebro.adddata(data)
	print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
	tradeLog['open_portfolio'] = cerebro.broker.getvalue()
	cerebro.run()
	print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
	tradeLog['close_portfolio'] = cerebro.broker.getvalue()
	print(tradeLog)
	return tradeLog
