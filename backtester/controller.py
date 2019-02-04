import pandas as pd
import backtester
import strategy
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
        self._strategy = None

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
    
    def returnCloseData(self):
        """
        Returns all the close data up to the current datetime.
        """
        return self._dataFromFile[self._dataFromFile.index <= self._dt]['close']

    def attachStrategy(self, strat):
        """
        Attaches a strategy to the controller.
        """
        self._strategy = strat
    
    def getStrategySignal(self):
        if self._strategy is None:
            print('Cannot run strategy as none is attached')
            return None
        print(self._strategy.generateSignal(self.returnCloseData()))