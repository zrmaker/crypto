import numpy as np
import pandas as pd

class technical_indicators():
    def __init__(self):
        self.close=0

    def MA(self, adj_close, window_length):
        result = pd.Series(adj_close).rolling(window= window_length).mean()
        return result

    def STOCH(self):
        self.close=0