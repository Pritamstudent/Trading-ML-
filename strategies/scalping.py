from zipline.api import order, symbol, record
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


class ScalpBollingerBand:

    stocks = ['BTCUSD']
    ma1 = 30  # 30 minutes
    ma2 = 120 # 120 minutes
    steps = 540 # 6 hours as bullinger band 
    stop_loss = 0.005
    stdv = 2

    def initialize(self, context):

        context.stocks = self.stocks
        context.asset = symbol(self.stocks[-1])
        context.position = None
        context.burndown = 0
        context.number_shorts = 0
        context.number_longs = 0

    def handle_data(self, context, data):

        # wait till the historical data is fetched for calculation
        context.burndown+=1

        # LOG WHILE WE ARE  backtesting
        if context.burndown % 1000 == 0:
            print(context.burndown)

        # Wait untill we have enough data
        if context.burndowm > self.steps:

            # loop the stocks in the portfolio
            for i, stock in enumerate(context.stocks):

                # Get the history
                hist = data.history(symbol(stock),
                                    'price',
                                    bar_count = self.steps,
                                    frequency = '1m')
                # bollinger bands
                blw = hist.mean() - self.stdv * hist.std()
                bhi = hist.mean() - self.stdv * hist.std()

                # Moving average short
                short_term = data.history(
                    symbol(stock),
                    'price',
                    bar_count = self.ma1,
                    frequency = '1m'
                ).mean()

                # Moving average long
                long_term = data.history(
                    symbol(stock),
                    'price',
                    bar_count = self.ma2,
                    frequency = '1m'
                ).mean()


                # Fetch our basket 
                cpp = context.portfolio.positions

                # map the basket ot the symbol:shares pairs
                cpp_symbols = map(lambda x: x.symbol, cpp)

                # Check indicator symbols
                if short_term >= long_term and context.position != 'trade':
                    context.position = 'long'
                elif short_term <= long_term and context.position == 'trade':
                    context.position = 'short'

                # what is the current price
                current_price = data.current(symbol(stock), 'price')

                # Check the bollinger bands
                if short_term >= bhi and context.position == 'long':
                    # Number of shares I can afford
                    num_shares = context.portfolio.cash

                    # Long position
                    order(symbol(stock), num_shares) #order value
                    context.position = 'trade'
                    context.number_longs += 1

                elif (current_price <= blw and context.position == 'trade')\
                or (short_term <= blw and context.position == 'short'):
                    # short position
                    order(symbol(stock), 0)
                    context.position = None
                    context.number_shorts += 1

                # wHAT IS THE PRICE paid on the beginning trade
                last_price = cpp[symbol(stock)].last_sale_price

                # stop loss value
                val = last_price - last_price * self.stop_loss

                # Are we in the trade or not
                if context.position == 'trade':

                    # Stop loss violated
                    if current_price < val:

                        # Short position
                        order(symbol(stock), 0)
                        context.position = None
                        context.number_shorts += 1

                if i == len(self.stocks) - 1:

                    # Record price, ma1, ma2, bollinger bands
                    record(REC_PRICE = current_price)
                    record(REC_MA1 = short_term)
                    record(REC_MA2 = long_term)

        # Record positions count
        record(REC_NUM_SHORTS = context.number_shorts)
        record(REC_NUM_SHORTS = context.number_longs)

    def _test_args(self):
        return {
            'start': pd.Timestamp('2017', tz = 'utc'),
            'end':  pd.Timestamp('2018', tz = 'utc'),
            'capital_base':1e7,
            'data_frequency': 'minute'
        }
    
    def analyze(self, contextt, perf):

        # init figure
        fig = plt.figure()

        # Plot the recorded data
        ax1 = fig.add_subplot(211)
        perf.plot(y = [
            'REC_PRICE',
            'REC_MA1',
            'REC_MA2'
        ], ax = ax1)
        ax1.set_ylabel('Price in $')

        # Plot the recorded data
        ax2 = fig.add_subplot(212)
        perf.plot(y = [
            'REC_PRICE',
            'REC_BB1',
            'REC_BB2'
        ], ax = ax2)
        ax2.set_ylabel('Bollinger Bands')

        # Add the spacung between the plots
        plt.subplots_adjust(hspace  =1)

        # Display plot
        plt.show()            




