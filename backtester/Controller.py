import pandas as pd
import backtester
from data import data_loader

class Controller:
    """
    Controls stuff.
    """

    def __init__(self, fileLocation):
        # Datetime is set once data is loaded
        self._dt = None
        self._fileLocation = fileLocation
        self._dataFromFile = None
        self._dataLoader = data_loader

    def loadData(self):
        self._dataFromFile = self._dataLoader.DataLoader(self._fileLocation).loadDataFromCSV()
        self._dt = self._dataFromFile.index[0]
    
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
        return self._dataFromFile.loc[self._dt]['close']