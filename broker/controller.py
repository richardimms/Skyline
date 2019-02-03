import v20
import pandas as pd
import time

class PositionController():

    def __init__(self, account_id, access_token, instrument):
        self._account_id = account_id
        self._access_token = access_token
        self._instrument = instrument
        self._api = None

    def setTraining(self):
        self._api = v20.Context("api-fxpractice.oanda.com", 443,token=self._access_token)
    
    def setProduction(self):
        #Change the URL to be the production URL
        self._api = v20.Context("api-fxpractice.oanda.com", 443,token=self._access_token)
        
    def getPendingOrders(self):
        """Returns the pending orders for the account."""
        getPendingOrdersResponse = self._api.order.list_pending(self._account_id)
        return getPendingOrdersResponse.get("orders", "200")

    def getOrder(self, order_id):
        """Returns details of an order."""
        getOrderResonse = self._api.order.get(self._account_id, order_id)
        return getOrderResonse

    def get_orders(self):
        """Returns the orders for the account."""
        getOrdersResponse = self._api.order.list(self._account_id)
        return getOrdersResponse.get("orders", "200")
    
    def getTrade(self, trade_id):
        """Returns details of a trade."""
        getTradeResponse = self._api.trade.get(self._account_id, trade_id)
        return getTradeResponse

    def getTransaction(self, transaction_id):
        """Returns details of a trade."""
        getTransactionResponse = self._api.transaction.get(self._account_id, transaction_id)
        return getTransactionResponse

    def getSummary(self):
        """Prints a summary of the account details."""
        getSummaryResponse = self._api.account.get(self._account_id)
        return getSummaryResponse.get("account", "200")

    def placeOrder(self, units):
        """Sends a market order."""
        placeOrderResponse = self._api.order.market(self._account_id, instrument=self._instrument, units=units)
        return placeOrderResponse  # Returns 201 if successful, 400 if not

    def getAllPositions(self):
        """Returns a list of positions."""
        summary = self.getSummary()
        position_list = summary.positions
        return position_list

    def getPriceData(self, granularity, from_dt=None, to_dt=None):
        """
        Returns the raw price data for the instrument.
        Valid granularity values:
            S5, S10, S15, S30, M1, M2,
            M4, M5, M10, M15, M30, H1,
            H2, H3, H4, H6, H8, H12, D, W, M
        """
        #I wonder if you can send a NONE to the API and it will ignore those two fields.
        getPriceDataResponse = self._api.instrument.candles(self._instrument, granularity=granularity,
                                                    fromTime=from_dt, toTime=to_dt)
        candles = getPriceDataResponse.body['candles']
        return candles

    def getPrices(self, granularity, from_dt=None, to_dt=None):
        """
        Returns the prices for the instrument.
        Valid granularity values:
            S5, S10, S15, S30, M1, M2,
            M4, M5, M10, M15, M30, H1,
            H2, H3, H4, H6, H8, H12, D, W, M
        """

        # Get the prices in dict format
        #I wonder if you can send a NONE to the API and it will ignore those two fields.
        candles = self.getPriceData(granularity, from_dt, to_dt)

        if candles is None:
            return None

        prices_df = self.formatCandlePriceData(candles)
        
        return prices_df

    def getLatestPrice(self):
        """
        Returns the prices for the instrument.
        Valid granularity values:
            S5, S10, S15, S30, M1, M2,
            M4, M5, M10, M15, M30, H1,
            H2, H3, H4, H6, H8, H12, D, W, M
        """

        # Get the prices in dict format
        candles = self.getPriceData('S5')

        if candles is None:
            return None

        prices_df = self.formatCandlePriceData(candles)

        return prices_df['close'][-1]

    def formatCandlePriceData(self, candles):

        columns = ['time', 'open', 'high', 'low', 'close', 'volume']
        prices_df = pd.DataFrame(columns=columns)

        for candle in candles:
            candle_time = candle.time
            candle_open = candle.mid.o
            candle_close = candle.mid.c
            candle_high = candle.mid.h
            candle_low = candle.mid.l
            candle_volume = candle.volume

            if candle.complete:
                prices_df.loc[len(prices_df)] = [candle_time,
                                                 candle_open,
                                                 candle_high,
                                                 candle_low,
                                                 candle_close,
                                                 candle_volume]
        
        prices_df['time'] = pd.to_datetime(prices_df['time'])
        prices_df.set_index('time', inplace=True)
        prices_df.sort_index(inplace=True)

        return prices_df