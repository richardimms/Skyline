import pandas as pd
import backtester

class Controller:
    """
    Controls stuff.
    """

    def __init__(self, fileLocation):
        # Datetime is set once data is loaded
        self._dt = None
        self._fileLocation = fileLocation
        self._data = None

    def loadData(self):
        self._data = backtester.DataLoader(self._fileLocation).loadDataFromCSV()
        self._dt = self._data.index[0]
    
    def incrementTime(self):
        self._dt = self._dt + pd.Timedelta('1 hour')
    
    def returnDt(self):
        """
        Returns the current datetime.
        """
        return self._dt
    
    def returnClose(self):
        """
        Returns the current close price.
        """
        return self._data.loc[self._dt]['close']