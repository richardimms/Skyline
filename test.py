import backtester

cont = backtester.Controller('data/EUR_USD_H1.csv')
cont.loadData()
print(cont.dt)
cont.incrementTime()
print(cont.dt)
print(cont.returnClose())