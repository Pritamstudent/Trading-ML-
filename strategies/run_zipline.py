from importlib import import_module
import os
from toolz import merge
from zipline import run_algorithm
from datetime import datetime
# These are used by the test examples.py to discover the examples to run
from zipline.utils.calendar_utils import register_calendar, get_calendar
from strategies.buy_and_hold import BuyAndHold
from strategies.auto_correlation import AutoCorrelation
from os import environ
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

def run_strategy(strategy_name):
    mod = None
    if strategy_name == 'buy_and_hold':
        mod = BuyAndHold()

    elif strategy_name == 'auto_correlation':
        mod = AutoCorrelation()

    # Convert start_date and end_date to UTC
    register_calendar("YAHOO", get_calendar("NYSE"), force = True)



    return run_algorithm(
        initialize=getattr(mod, 'initialize', None),
        handle_data=getattr(mod, 'handle_data', None),
        before_trading_start=getattr(mod, 'before_trading_start', None),
        analyze=getattr(mod, 'analyze', None),
        bundle='quandl',
        environ=environ,
        **merge({'capital_base': 1e7}, mod._test_args())
    )


    
