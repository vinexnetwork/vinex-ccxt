# -*- coding: utf-8 -*-

import math

import dateutil.parser

# from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ExchangeError, InvalidOrder
from ccxt.base.exchange import Exchange

# FIXME: Hard code market id map
MARKET_ID_MAP = {
    'MCC/USDT': 83
}


class coinhe(Exchange):

    def describe(self):
        return self.deep_extend(super(coinhe, self).describe(), {
            'id': 'coinhe',
            'name': 'coinhe',
            'countries': ['SG'],
            'rateLimit': 200,
            # 'has': {
            #     'fetchCurrencies': True,
            #     'fetchTickers': True,
            #     'fetchOpenOrders': True,
            #     'fetchMyTrades': True,
            # },
            'urls': {
                'api': 'https://api.coinhe.io/v1',
                'www': 'https://coinhe.io/',
                'doc': 'https://docs.coinhe.io/',
                'fees': 'https://coinhe.io/fees',
            },
            'api': {
                'public': {
                    'get': [
                        'assets',
                        'ticker',
                        'market-summary',
                        'orderbook/{market_id}',
                        'trades/{market_id}',
                        'candlestick-v2',
                    ],
                },
                'private': {
                    'get': [
                        'app-key-orders',
                        'app-key-orders/{order_id}',
                    ],
                    'post': [
                        'app-key-orders/',
                        'app-key-orders/cancel-all/',
                    ],
                }
            },
            'fees': {
                'trading': {
                    'maker': 0.004,
                    'taker': 0.004,
                },
            },
        })

    def fetch_markets(self, params={}):
        markets = self.publicGetMarketSummary()
        # markets = self.publicGetTicker()

        result = []

        for market in markets:
            id = next(iter(market))

            quoteId, baseId = id.split('_')

            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)

            symbol = base + '/' + quote
            active = not market[id]['isFrozen']

            precision = {
                'amount': 6,
                'price': 8,
            }

            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': math.pow(10, precision['amount']),
                    },
                    'price': {
                        'min': math.pow(10, -precision['price']),
                        'max': math.pow(10, precision['price']),
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        symbol = market['symbol']
        timestamp = ticker['date']
        ticker = ticker['ticker']

        last = self.safe_float(ticker, 'lastPrice')

        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high24h'),
            'low': self.safe_float(ticker, 'low24h'),
            'bid': self.safe_float(ticker, 'highestBid'),
            'ask': self.safe_float(ticker, 'lowestAsk'),
            'close': last,
            'last': last,
            'baseVolume': self.safe_float(ticker, 'baseVolume24h'),
            'quoteVolume': self.safe_float(ticker, 'quoteVolume24h'),
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        tickers = self.fetch_tickers()

        return tickers[symbol]

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        tickers = self.publicGetMarketSummary(params)
        result = {}

        for ticker in tickers:
            market_id = next(iter(ticker))
            market = self.markets_by_id[market_id]
            symbol = market['symbol']
            ticker = {
                'date': ticker[market_id]['lastUpdateTimestamp'] * 1000,
                'ticker': ticker[market_id],
            }
            result[symbol] = self.parse_ticker(ticker, market)

        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()

        timestamp = self.milliseconds()

        orderbook = self.publicGetOrderbookMarketId(self.extend({
            'market_id': self.market_id(symbol),
        }, params))

        return self.parse_order_book(orderbook, timestamp, 'bids', 'asks')

    def fetch_balance(self, params={}):
        # self.load_markets()

        # FIXME: Hard code: balance
        # balances = self.privateGetBalances(params)
        balances = [
            {
                'asset': 'MCC',
                'free': 50000,
                'locked': 0,
            },
            {
                'asset': 'USDT',
                'free': 100,
                'locked': 0,
            },
        ]

        result = {'info': balances}

        for balance in balances:
            currency = self.common_currency_code(balance['asset'])

            free_amount = float(balance['free'])
            used_amount = float(balance['locked'])

            account = {
                'free': free_amount,
                'used': used_amount,
                'total': free_amount + used_amount,
            }

            result[currency] = account

        return self.parse_balance(result)

    def parse_trade(self, trade, market=None):
        # Common fields
        timestamp = trade['trade_timestamp'] * 1000

        symbol = market['symbol']

        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'base_volume')

        # Result
        result = {
            'id': self.safe_string(trade, 'tradeID'),
            'symbol': symbol,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'type': 'limit',
            'side': trade['type'],
            'price': price,
            'amount': amount,
            'cost': self.safe_float(trade, 'quote_volume'),
            'info': trade.copy(),
        }

        return result

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)

        trades = self.publicGetTradesMarketId(self.extend({
            'market_id': market['id'],
        }, params))

        # trades = list()
        # for trade in data['recent_trades']:
        #     trade_obj = trade.copy()
        #     trade_obj['info'] = trade
        #
        #     trades.append(trade_obj)

        return self.parse_trades(trades, market, since, limit)

    def parse_order(self, order, market=None):
        order_id = self.safe_string(order, 'id')

        base_asset = order['currency_pair']['pair']['symbol']
        quote_asset = order['currency_pair']['base']['symbol']

        symbol = f'{base_asset}/{quote_asset}'

        timestamp = int(dateutil.parser.parse(order['date_added']).timestamp() * 1000)

        side = order['type']

        status = 'open'
        if order['status'] == 'pending':
            status = 'open'
        elif order['status'] == 'succeed':
            status = 'closed'
        elif order['status'] == 'canceled':
            status = 'canceled'

        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        remaining = self.safe_float(order, 'amount_left')

        filled = amount - remaining
        cost = filled * price

        return {
            'id': order_id,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'cost': cost,
            'info': order,
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        # market = self.market(symbol)

        market_id = MARKET_ID_MAP.get(symbol)
        if not market_id:
            raise InvalidOrder(symbol)

        request = dict()
        request['currency_pair_id'] = market_id
        request['type'] = side

        request['price'] = float(self.price_to_precision(symbol, price))
        request['amount'] = float(self.amount_to_precision(symbol, amount))

        data = self.privatePostAppKeyOrders(self.extend(request, params))

        order = self.parse_order(data)

        return order

    # def cancel_order(self, id, symbol=None, params={}):
    #     self.load_markets()
    #     market = self.market(symbol)
    #
    #     request = dict()
    #     request['market'] = market['id']
    #     request['uid'] = id
    #
    #     result = self.privatePostCancelOrder(self.extend(request, params))
    #
    #     return result

    def cancel_all_order(self, symbol=None, params={}):
        # self.load_markets()
        # market = self.market(symbol)

        request = dict()
        # request['market'] = market['id']

        result = self.privatePostAppKeyOrdersCancelAll(self.extend(request, params))

        return result

    # def fetch_order(self, id, symbol=None, params={}):
    #     self.load_markets()

    #     data = self.privateGetUserOrderOrderId(self.extend({
    #         'order_id': id
    #     }, params))['order']

    #     order_obj = data.copy()
    #     order_obj['info'] = data

    #     order = self.parse_order(order_obj)

    #     return order

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()

        request = dict()

        market = None
        if symbol:
            market = self.market(symbol)

        orders = self.privateGetAppKeyOrders(self.extend(request, params))['results']

        return self.parse_orders(orders, market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        total_orders = self.fetch_orders(symbol, since, limit, params)
        orders = self.filter_by(total_orders, 'status', 'open')

        return orders

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        total_orders = self.fetch_orders(symbol, since, limit, params)
        orders = self.filter_by(total_orders, 'status', 'closed')

        return orders

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api']
        query = self.omit(params, self.extract_params(path))

        url += '/' + self.implode_params(path, params)

        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()

            headers = dict()
            headers['Authorization'] = self.secret

            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            elif query:
                body = self.json(query)
                headers['Content-Type'] = 'application/json'

        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        try:
            response = self.fetch2(path, api, method, params, headers, body)
        except Exception as e:
            raise ExchangeError(e)

        if response:
            return response
