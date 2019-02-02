import backtester
import strategy

c = backtester.Controller('data/EUR_USD_H1.csv')
s = strategy.MACStrategy(2,10)
c.loadData()
c.attachStrategy(s)

for i in range(100):

    c.getStrategySignal()
    c.incrementTime()