from zipline.api import order, symbol, record
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np
from joblib import load
# from zipline.api import set_timezone, order_target_percent
class BuyAndHold:

    stocks = ['AAPL', 'MSFT', 'TSLA']
    lag = 33
    forecast = 8

    def initialize(self, context):
        # set_timezone('UTC')
        context.has_ordered = False
        context.stocks = self.stocks
        context.asset = symbol('AAPL')
        context.regressor = load('./strategies/models/rf_regressor.joblib')

    def handle_data(self, context, data):

            # We go for the long stocks
        for stock in context.stocks:
            timeseries = data.history(
                symbol(stock),
                'price',
                bar_count = self.lag,
                frequency = '1d'

            )  # Use context.asset here
            np_timeseries = np.array(timeseries.values).reshape(1,-1)
            preds = context.regressor.predict(np_timeseries)
            max_price = np.max(preds)
            historical_mean = np.mean(np_timeseries)

            if max_price > historical_mean:
                order(symbol(stock), 1000)

            if max_price < historical_mean:
                order(symbol(stock), -1000)

        record(AAPI=data.current(context.asset, 'price'))

    def _test_args(self):
        return {
            'start': pd.Timestamp('2017', tz = 'utc'),
            'end': pd.Timestamp('2018', tz = 'utc'),
            'capital_base': 1e7
        }

    def analyze(self, context, perf):
        # Plot the portfolio values into the charts
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        perf.portfolio_value.plot(ax=ax1)
        ax1.set_ylabel('Portfolio value in $')

        ax2 = fig.add_subplot(212)
        print(perf.columns)
        perf['AAPI'].plot(ax=ax2)

        ax2.set_ylabel('price in $')
        plt.legend(loc=0)
        plt.show()
