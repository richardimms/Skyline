import logging
import uuid
from tinydb import Query
from tinydb import TinyDB
import pandas as pd

class PosmaSim(object):
    """
    Pos(ition) ma(nager) is used for managing positions.
    """

    def __init__(self, owner):
        self.owner = owner
        self.db_filename = '{}_{}.json'.format('test', pd.datetime.now().strftime('%Y%b%d-%H%M%S'))
        self.db = TinyDB('{}'.format(self.db_filename))

    # def maintain(self):
    #     """
    #     Checks that local DB and broker are in sync (baselines if not) and monitors positions.
    #     :return: None
    #     """
    #     # logger_POSMA.debug('Running maintenance')
    #     # if not self.check_sync():
    #     #     self.baseline()
    #     self.monitor_positions()
    #     # logger_POSMA.debug('Maintenance complete')

    def close_positions(self):
        """
        Closes all open positions.
        :return: None
        """
        for position in self.get_open_positions():
            self.close_position(position['id'], msg='manual close')

    # def monitor_positions(self):
    #     """
    #     Check whether SL or TP has been hit for each open position. Closes it if so.
    #     :return: None
    #     """
    #     positions = self.get_open_positions()
    #     # logger_POSMA.debug('Monitoring positions')
    #     latest_price = self.owner.returnClose()
    #     # logger_POSMA.debug('Latest price is: {}'.format(latest_price))

    #     for position in positions:
    #         doc_id = position.doc_id
    #         # logger_POSMA.debug('Monitoring position {}'.format(position['id']))
    #         if position['sl'] is not None:
    #             if position['units'] > 0:
    #                 if latest_price < position['sl']:
    #                     # logger_POSMA.info('SL of {} for position of {} units hit at {}.'
    #                     #                   ' Closing position'.format(position['sl'],
    #                     #                                             position['units'],
    #                     #                                             latest_price))
    #                     self.close_position(position['id'], 'SL hit')

    #                 # Adjusting trailing SL
    #                 # # If profitable, set SL to half the profit (if higher)
    #                 # elif latest_price - position['open_price'] > 0:
    #                 #     curr_prof = latest_price - position['open_price']
    #                 #     potential_sl = position['open_price'] + (curr_prof * 0.1)
    #                 #     if potential_sl > position['sl']:
    #                 #         logger_POSMA.debug('Adjusting the SL for trailing - half profit')
    #                 #         self.update_position(doc_id, 'sl', potential_sl)

    #                 elif latest_price - self.owner.strategy.sl > position['sl']:
    #                     # logger_POSMA.debug('Adjusting the SL for trailing - normal trailing')
    #                     new_sl = latest_price - self.owner.strategy.sl
    #                     self.update_position(doc_id, 'sl', new_sl)

    #             else:
    #                 if latest_price > position['sl']:
    #                     # logger_POSMA.info('SL of {} for position of {} units hit at {}.'
    #                     #                   ' Closing position'.format(position['sl'],
    #                     #                                             position['units'],
    #                     #                                             latest_price))
    #                     self.close_position(position['id'], 'SL hit')

    #                 elif latest_price + self.owner.strategy.sl < position['sl']:
    #                     # logger_POSMA.debug('Adjusting the SL for trailing')
    #                     new_sl = latest_price + self.owner.strategy.sl
    #                     self.update_position(doc_id, 'sl', new_sl)

    #         if position['tp'] is not None:
    #             if position['units'] > 0:
    #                 if latest_price > position['tp']:
    #                     # logger_POSMA.info('TP of {} for position of {} units hit at {}.'
    #                     #                   ' Closing position'.format(position['tp'],
    #                     #                                             position['units'],
    #                     #                                             latest_price))
    #                     self.close_position(position['id'], 'TP hit')
    #             else:
    #                 if latest_price < position['tp']:
    #                     # logger_POSMA.info('TP of {} for position of {} units hit at {}.'
    #                     #                   ' Closing position'.format(position['tp'],
    #                     #                                             position['units'],
    #                     #                                             latest_price))
    #                     self.close_position(position['id'], 'TP hit')

    def send_order(self, units):
        """
        Sends transaction order through the owner's broker. Stores the transaction details in DB.
        :return: Transaction details if successful, False otherwise
        """

        transaction_dt = self.owner.returnDt()
        transaction_price = self.owner.returnClose()
        tx_details = {'datetime': transaction_dt.isoformat(),
                      'units': units,
                      'price': transaction_price,
                      'instrument': 'test',
                      'transaction_id': 'NA'}
        # logger_TRANSACTION.info('Transaction details: {}'.format(tx_details))

        self.add_transaction_to_db(tx_details)

        return tx_details

    def create_position(self, units, open_dt, open_price, sl=None, tp=None, open_msg=None):
        """
        Returns a dictionary representing a position.
        :param units: Integer of the number of units
        :param open_dt: ISO8061 string for the open datetime of the position
        :param open_price: Float for the open price of the position
        :param sl: Float for the stop loss set for the position
        :param tp: Float for the take profit set for the position
        :param open_msg: String describing why the position was opened
        :return: Dictionary
        """
        position = {'open_dt': open_dt,
                    'open_price': open_price,
                    'close_dt': None,
                    'close_price': None,
                    'units': units,
                    'sl': sl,
                    'tp': tp,
                    'id': str(uuid.uuid4()),
                    'status': 'open',
                    'open_msg': open_msg,
                    'close_msg': None}
        return position

    def add_position_to_db(self, position):
        """
        Adds a position to the postions table. Called automatically when opening a position.
        :param position: Dictionary representing the position
        :return: None
        """
        doc_id = self.db.table('positions').insert(position)
        # logger_POSITION.info('Successfully added position to DB. DOC_ID={}: {}'.format(doc_id, position))

    def open_position(self, units, sl=None, tp=None, msg=''):
        """
        Handles the opening of a position with sending of order to broker and adding transaction to DB.
        :param units: Integer, units to create position for
        :param sl: Float for SL, the value above/below the open price it will be set
        :param tp: Float for TP, the value above/below the open price it will be set
        :param msg: Optional string for open message to know why position was opened
        :return: None
        """
        # logger_POSITION.info('Creating position for {} units. Reason: {}'.format(units, msg))
        transaction = self.send_order(units)

        if transaction:
            # Set the TP and SL
            open_price = transaction['price']

            # Calibrate the SL and TP
            if sl is not None:
                if units > 0:
                    calculated_sl = open_price - sl
                else:
                    calculated_sl = open_price + sl
            else:
                calculated_sl = None

            if tp is not None:
                if units > 0:
                    calculated_tp = open_price + tp
                else:
                    calculated_tp = open_price - tp
            else:
                calculated_tp = None

            position = self.create_position(units=units,
                                            open_dt=transaction['datetime'],
                                            open_price=open_price,
                                            sl=calculated_sl,
                                            tp=calculated_tp,
                                            open_msg=msg,
                                            )
            position['open_id'] = transaction['transaction_id']
            self.add_position_to_db(position)
        else:
            pass
            # logger_POSITION.error('Unable to open position')

    def close_position(self, position_id, msg=''):
        """
        Closes a position, sending in order to the broker and updating the DB.
        :param position_id: uuid of the position
        :param msg: String for optional close message to know why position was closed
        :return: None
        """
        # logger_POSITION.info('Closing position {}. Reason: {}'.format(position_id, msg))
        position = self.get_position(position_id)
        doc_id = position.doc_id

        # Send in transaction order and get details
        transaction = self.send_order(-position['units'])

        if transaction:
            self.update_position(doc_id, 'status', 'closed')
            self.update_position(doc_id, 'close_dt', transaction['datetime'])
            self.update_position(doc_id, 'close_price', transaction['price'])
            self.update_position(doc_id, 'close_msg', msg)
            self.update_position(doc_id, 'close_id', transaction['transaction_id'])
            # logger_POSITION.info('Closed position {}'.format(position_id))
        else:
            # logger_POSITION.error('Unable to close position')
            pass

    def add_transaction_to_db(self, transaction):
        """
        Adds a transaction to the transactions table.
        :param transaction: Dictionary representing the transaction
        :return: None
        """
        doc_id = self.db.table('transactions').insert(transaction)
        # logger_TRANSACTION.info('Successfully added transaction to DB. DOC_ID={}: {}'.format(doc_id, transaction))

    def get_position(self, position_id):
        """
        Returns the position within the owner's positions table
        :param position_id: id of the position
        :return: position within the owner's positions table
        """
        matches = self.db.table('positions').search(Query().id == position_id)
        if len(matches) == 0:
            # logger_POSMA.warning('Unable to find position {}.'.format(position_id))
            return None

        elif len(matches) > 1:
            # logger_POSMA.warning('Multiple matches for position {} found.'.format(position_id))
            return None
        else:
            position = matches[0]
            doc_id = position.doc_id
            # logger_POSMA.debug('Position {} found, doc_id is: {}'.format(position_id, doc_id))
            return position

    def update_position(self, doc_id, field, new_value):
        """
        Updates a position in the positions table based on doc_id
        :param doc_id: doc_id
        :param field: String of which field to update
        :param new_value: New value for the field
        :return: None
        """
        try:
            self.db.table('positions').update({field: new_value}, doc_ids=[doc_id])
            # logger_POSITION.debug('Successfully updated {} field of doc_id {} with value {}'.format(field, doc_id, new_value))
        except Exception as e:
            # logger_POSITION.error('Unable to update {} field of doc_id {}'.format(field, doc_id))
            pass

    def get_open_positions(self):
        """
        Returns list of all open positions.
        :return: List of open positions
        """
        matches = self.db.table('positions').search(Query().status == 'open')
        return matches

