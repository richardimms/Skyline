import backtester
import strategy
import posma

c = backtester.Controller('data/EUR_USD_H1.csv')
s = strategy.MACStrategy(2,10)
c.loadData()
c.attachStrategy(s)

# for i in range(100):

#     c.getStrategySignal()
#     c.incrementTime()

pos = posma.PosmaSim(c)
pos.open_position(10, msg='test')
for i in range(100):
    c.incrementTime()
pos.close_positions()