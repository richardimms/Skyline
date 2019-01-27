import pandas as pd
import backtester

class Controller:
    """
    Controls stuff.
    """

    def __init__(self, fileLocation):
        # Datetime is set once data is loaded
        self.dt = None
        self.fileLocation = fileLocation
        self.data = None

    def loadData(self):
        self.data = backtester.DataLoader(self.fileLocation).loadDataFromCSV()
        self.dt = self.data.index[0]
    
    def incrementTime(self):
        self.dt = self.dt + pd.Timedelta('1 hour')
    
    def returnClose(self):
        """
        Returns the current close price.
        """
        return self.data.loc[self.dt]['close']