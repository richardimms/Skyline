import backtester

cont = backtester.Controller('data/EUR_USD_H1.csv')
cont.loadData()
print(cont.returnDt())
cont.incrementTime()
print(cont.returnDt())
print(cont.returnClose())