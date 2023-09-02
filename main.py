import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")
from strategies.run_zipline import run_strategy
def main():
    print("*** Algorithm trading bots ***")
    print(" BUY and HOLD strategy ")
    perf = run_strategy('auto_correlation')
    perf.to_csv("auto_correlation.csv")

if __name__ == '__main__':

    main()