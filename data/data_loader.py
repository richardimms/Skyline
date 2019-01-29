import pandas as pd

class DataLoader():
    """
    Class used to load price data.
    """

    def __init__(self, fileLocation):
        self._fileLocation = fileLocation
    
    def loadDataFromCSV(self):
        data = pd.read_csv(self._fileLocation)
        data['time'] = pd.to_datetime(data['time'])
        data.set_index('time', inplace=True)
        return data
        