import backtester
import strategy
import posma

c = backtester.Controller('data/EUR_USD_H1.csv')
s = strategy.MACStrategy(2,10)
c.loadData()
c.attachStrategy(s)
pos = posma.PosmaSim(c)
c.attachPOSMA(pos)

# for i in range(100):

#     c.getStrategySignal()
#     c.incrementTime()

for i in range(100):
    c.incrementTime()
    c.run()
print(pos.get_open_positions())
pos.close_positions()
