from importlib import import_module
import os
from toolz import merge
import xarray as xr
from zipline import run_algorithm
from datetime import datetime
# These are used by the test examples.py to discover the examples to run
from zipline.utils.calendar_utils import register_calendar, get_calendar
from strategies.buy_and_hold import BuyAndHold
from strategies.auto_correlation import AutoCorrelation
from strategies.scalping import ScalpBollingerBand
from os import environ
from toolz import merge 
#from zipline import run_algorithm
# from zipline.utils.calendars import register_calendar, get_calendar
from strategies.buy_and_hold import BuyAndHold
from strategies.auto_correlation import AutoCorrelation
from os import environ
from strategies.scalping import ScalpBollingerBand
import pandas as pd
import os
import pytz
from collections import OrderedDict
from strategies.calender import CryptoCalendar
import pandas as pd
_cols_to_check = {
    'algo_volatility',
    'algorithm_period_return',
    'alpha',
    'benchmark_period_return',
    'beta',
    'capital_used',
    'ending_cash',
    'ending_exposure',
    'ending_value',
    'long_value',
    'longs_count',
    'max_drawdown',
    'max_leverage',
    'net_leverage',
    'period_close',
    'period_label',
    'period_open',
    'pnl',
    'portfolio_value',
    'positions',
    'returns',
    'short_exposure',
    'short_value',
    'shorts_count',
    'sorting',
    'starting_cash',
    'starting_exposure',
    'starting_value',
    'trading_days',
    'treasury_period_return',
}

from pytz import timezone, UTC  # Import UTC timezone

def prepareCSV(csv_pth):
    files = os.listdir(csv_pth)
    start = end = None
    
    dd = OrderedDict()
    for f in files:
        fp = os.path.join(csv_pth, f)
        n1 = os.path.splitext(fp)[0]
        if '\\' in n1:
            key_parts = n1.split('\\')
            if len(key_parts) >= 2:
                key = key_parts[1]
            else:
                # Handle the case where there is only one part after splitting
                # You can choose to assign the entire string or raise an exception, depending on your requirements
                key = n1  # Assign the entire string
                # Alternatively, raise an exception
                # raise ValueError("Expected at least two parts after splitting, but got:", n1)
        else:
        # Handle the case where '/' is not found in n1
            print("Error: '/' not found in:", n1)

        df = pd.read_csv(fp)
        print(df['date'])
        print(df.head())

        df.index = pd.DatetimeIndex(df.date)
        df = df.sort_index()
        dd[key] = df.drop(columns=['date'])
        start = df.index.values[0]
        end = df.index.values[10*24*60]
    
    data_vars = {}
    coords = {'date': pd.date_range(start=start, end=end, freq='H')}
    for key, value in dd.items():
        data_vars[key] = (('date',), value.values)
    
    ds = xr.Dataset(data_vars, coords=coords)
    ds = ds.assign_coords({'asset': list(dd.keys())})
    
    return ds, start, end
    
'''
 panel = pd.Panel(dd)

    panel.major_axis = panel.major_axis.tz_localize(pytz.utc)

    return panel, pd.to_datetime(start).tz_localize(pytz.utc), pd.to_datetime(end).tz_localize(pytz.utc)
'''   


def run_strategy(strategy_name):
    mod = None
    if strategy_name == 'buy_and_hold':
        mod = BuyAndHold()

    elif strategy_name == 'auto_correlation':
        mod = AutoCorrelation()
    elif strategy_name == 'scalping':
        mod = ScalpBollingerBand()

    # Convert start_date and end_date to UTC
    # register_calendar("YAHOO", get_calendar("NYSE"), force = True)
    data_panel, start, end = prepareCSV('csv')
    print(data_panel, type(start))



    return run_algorithm(
        initialize=getattr(mod, 'initialize', None),
        handle_data=getattr(mod, 'handle_data', None),
        before_trading_start=getattr(mod, 'before_trading_start', None),
        analyze=getattr(mod, 'analyze', None),
        bundle='quandl',
        environ=environ,
        **merge({'capital_base': 1e7}, mod._test_args())
    )


    
