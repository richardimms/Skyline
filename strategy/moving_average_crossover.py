import pandas as pd

class MACStrategy:
    """
    Simple moving average crossover strategy.
    """

    def __init__(self, shortPeriod, longPeriod):
        self._shortPeriod = shortPeriod
        self._longPeriod = longPeriod

    def generateSignal(self, data):
        """
        Returns 'Long' if the short moving average is larger than the
        long moving average, 'Short' otherwise.

        The data is expected to be a pandas series.
        """
    
        shortMA = data.rolling(window=self._shortPeriod).mean()
        longMA = data.rolling(window=self._longPeriod).mean()
        # print(round(shortMA.iloc[-1],5), round(longMA.iloc[-1],5))
        if shortMA.iloc[-1] > longMA.iloc[-1]:
            return 'Long'
        else:
            return 'Short'
