import pandas as pd
import backtester
import strategy
from data import data_loader
import json

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
        self._posma = None

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
        return self._dataFromFile[:self._dt].iloc[-1]['close']
    
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
    
    def attachPOSMA(self, posma):
        """
        Attaches a position manager to the controller
        """
        self._posma = posma
    
    def getStrategySignal(self):
        if self._strategy is None:
            print('Cannot run strategy as none is attached')
            return None
        return self._strategy.generateSignal(self.returnCloseData())
    
    def run(self):
        """
        Triggers the running of a strategy and executes any orders.
        """
        order = self.getStrategySignal()
        open_positions = self._posma.get_open_positions()

        if order is None:
            return None

        if order == 'Long':
            # Close any open short positions
            for position in open_positions:
                if position['units'] < 0:
                    self._posma.close_position(position['id'], msg='counter signal')
            # Only open new long position if there are no existing long positions
            for position in open_positions:
                if position['units'] > 0:
                    return None
            self._posma.open_position(100, msg='signal')

        elif order == 'Short':
            # Close any open long positions
            for position in open_positions:
                if position['units'] > 0:
                    self._posma.close_position(position['id'], msg='counter signal')
            # Only open new short position if there are no existing short positions
            for position in open_positions:
                if position['units'] < 0:
                    return None
            self._posma.open_position(-100, msg='signal')
