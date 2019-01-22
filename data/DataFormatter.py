class DataFormatter():

    def __init__(self, data):
        self._data = data

    def formatData(self):
        _time = self._data['time']
        _open = self._data['open']
        _low = self._data['low']
        _close = self._data['close']
        _volume = self._data['volume']


