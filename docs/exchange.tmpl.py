# -*- coding: utf-8 -*-

from ccxt.base.exchange import Exchange
# import hashlib
# import math
# from ccxt.base.errors import ExchangeError
# from ccxt.base.errors import AuthenticationError
# from ccxt.base.errors import InvalidOrder


class qtrade (Exchange):

    def describe(self):
        return self.deep_extend(super(qtrade, self).describe(), {
            'id': 'qtrade',
            'name': 'qTrade',
            'countries': ['US'],
            'rateLimit': 500,
            # 'has': {
            #     'fetchCurrencies': True,
            #     'fetchTickers': True,
            #     'fetchOpenOrders': True,
            #     'fetchMyTrades': True,
            #     'fetchDepositAddress': True,
            # },
            'urls': {
                'logo': 'hhttps://qtrade.io/images/logo.png',
                'api': 'https://api.qtrade.io/v1',
                'www': 'https://qtrade.io/',
                'doc': 'https://qtrade-exchange.github.io/qtrade-docs/',
                'fees': 'https://qtrade.io/fees',
                'referral': 'https://qtrade.io/?ref=AZCXUQ6P5KCG',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'market/{market}',
                        'currencies',
                        'tickers',
                        'ticker/{market}',
                        # 'ticker_by_id/{market_id}',            # NOTE: dont implement
                        'orderbook/{market}',
                        # 'orderbook_by_id/{market_id}',         # NOTE: dont implement
                        'market/{market_id}/ohlcv/{interval}',
                    ],
                },
                'private': {
                    'get': [
                        # 'user/me',                             # NOTE: dont implement
                        'user/balances',
                        # 'user/market/:market_id',              # NOTE: dont implement
                        'user/orders',
                        'user/order/{order_id}',
                        'user/withdraws',
                        'user/withdraw/{withdraw_id}',
                        'user/deposits',
                        # 'user/deposit/{deposit_id}',           # NOTE: This endpoint currently non-functional
                        'user/transfers'                         # NOTE: Returns a list of the user's Transfers and metadata.
                    ],
                    'post': [
                        'user/cancel_order',
                        # 'user/deposit_address/{currency}'       # NOTE: dont implement

                        'user/sell_limit',
                        'user/buy_limit',
                    ],
                },
            },
            'commonCurrencies': {
                'EPC': 'Epacoin',
                'ABC': 'Anti Bureaucracy Coin',
            },
            'fees': {
                'trading': {
                    'maker': 0.005,
                    'taker': 0.005,
                },
            },
            'precision': {
                'amount': 8,
                'price': 8,
            },
        })

    ####################################
    # Public:
    ####################################
    # TODO: fetch_markets()
    def fetch_markets(self, params={}):
        pass

    # TODO: fetch_ticker()
    #       - parse_ticker()
    def parse_ticker(self, ticker, market=None):
        pass

    def fetch_ticker(self, symbol, params={}):
        pass

    # TODO: fetch_tickers()
    def fetch_tickers(self, symbols=None, params={}):
        pass

    # TODO: fetch_order_book()
    # call: parse_order_book(self, orderbook, timestamp=None, bids_key='bids', asks_key='asks', price_key=0, amount_key=1)
    def fetch_order_book(self, symbol, limit=None, params={}):
        pass

    # NOTE: fetch_fees()            <- Don't need

    # TODO: parse_trade()
    def parse_trade(self, trade, market=None):
        pass

    # TODO: fetch_trades()
    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        pass

    ####################################
    # Private:
    ####################################
    # TODO: fetch_balance()
    def fetch_balance(self, params={}):
        pass

    # TODO: parse_order()
    def parse_order(self, order, market=None):
        pass

    # TODO: create_order()
    def create_order(self, symbol, type, side, amount, price=None, params={}):
        pass

    # TODO: cancel_order()
    def cancel_order(self, id, symbol=None, params={}):
        pass

    # TODO: fetch_order()
    def fetch_order(self, id, symbol=None, params={}):
        pass

    # TODO: fetch_orders()
    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        pass

    # TODO: fetch_open_orders()
    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        pass

    # TODO: fetch_my_trades()
    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        pass

    ####################################
    # Base:
    ####################################
    # TODO: sign()
    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        pass

    # Use default:
    # - market()
    # - parse_orders()
