import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")
from strategies.run_zipline import run_strategy
def main():
    print("***  Hands-on Machine Learning for Algorithmic Trading Bots ***")
    print("*** Implement Scalping Strategy ***")
    perf = run_strategy("scalping")
    perf.to_csv("scalping.csv")

if __name__ == '__main__':

    main()