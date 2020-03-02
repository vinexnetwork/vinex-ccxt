- [API](#api)
- [Public](#public)
  - [Exchange Structure](#exchange-structure)
  - [Market Structure](#market-structure)
  - [Order Book Structure](#order-book-structure)
  - [Ticker structure](#ticker-structure)
  - [OHLCV Structure](#ohlcv-structure)
- [Private](#private)
  - [Balance Structure](#balance-structure)
  - [Order Structure](#order-structure)
  - [Trade Structure](#trade-structure)
  - [Address Structure](#address-structure)
  - [Transaction Structure](#transaction-structure)
  - [Fee Structure](#fee-structure)
  - [Ledger Entry Structure](#ledger-entry-structure)


# API

    +-------------------------------------------------------------+
    |                            CCXT                             |
    +------------------------------+------------------------------+
    |            Public            |           Private            |
    +=============================================================+
    │                              .                              |
    │                    The Unified CCXT API                     |
    │                              .                              |
    |       loadMarkets            .           fetchBalance       |
    |       fetchMarkets           .            createOrder       |
    |       fetchCurrencies        .            cancelOrder       |
    |       fetchTicker            .             fetchOrder       |
    |       fetchTickers           .            fetchOrders       |
    |       fetchOrderBook         .        fetchOpenOrders       |
    |       fetchOHLCV             .      fetchClosedOrders       |
    |       fetchTrades            .          fetchMyTrades       |
    |                              .                deposit       |
    |                              .               withdraw       |
    │                              .                              |
    +=============================================================+
    │                              .                              |
    |                     Custom Exchange API                     |
    |         (Derived Classes And Their Implicit Methods)        |
    │                              .                              |
    |       publicGet...           .          privateGet...       |
    |       publicPost...          .         privatePost...       |
    |                              .          privatePut...       |
    |                              .       privateDelete...       |
    |                              .                   sign       |
    │                              .                              |
    +=============================================================+
    │                              .                              |
    |                      Base Exchange Class                    |
    │                              .                              |
    +=============================================================+




# Public

## Exchange Structure

```python
{
    'id':   'exchange'                  # lowercase string exchange id
    'name': 'Exchange'                  # human-readable string
    'countries': [ 'US', 'CN', 'EU' ],  # array of ISO country codes
    'urls': {
        'api': 'https:#api.example.com/data',  # string or dictionary of base API URLs
        'www': 'https:#www.example.com'        # string website URL
        'doc': 'https:#docs.example.com/api',  # string URL or array of URLs
    },
    'version':         'v1',            # string ending with digits
    'api':             { ... },         # dictionary of api endpoints
    'has': {                            # exchange capabilities
        'CORS': false,
        'publicAPI': true,
        'privateAPI': true,
        'cancelOrder': true,
        'createDepositAddress': false,
        'createOrder': true,
        'deposit': false,
        'fetchBalance': true,
        'fetchClosedOrders': false,
        'fetchCurrencies': false,
        'fetchDepositAddress': false,
        'fetchMarkets': true,
        'fetchMyTrades': false,
        'fetchOHLCV': false,
        'fetchOpenOrders': false,
        'fetchOrder': false,
        'fetchOrderBook': true,
        'fetchOrders': false,
        'fetchTicker': true,
        'fetchTickers': false,
        'fetchBidsAsks': false,
        'fetchTrades': true,
        'withdraw': false,
    },
    'timeframes': {                     # empty if the exchange !has.fetchOHLCV
        '1m': '1minute',
        '1h': '1hour',
        '1d': '1day',
        '1M': '1month',
        '1y': '1year',
    },
    'timeout':          10000,          # number in milliseconds
    'rateLimit':        2000,           # number in milliseconds
    'userAgent':       'ccxt/1.1.1 ...' # string, HTTP User-Agent header
    'verbose':          false,          # boolean, output error details
    'markets':         { ... }          # dictionary of markets/pairs by symbol
    'symbols':         [ ... ]          # sorted list of string symbols (traded pairs)
    'currencies':      { ... }          # dictionary of currencies by currency code
    'markets_by_id':   { ... },         # dictionary of dictionaries (markets) by id
    'proxy': 'https:#crossorigin.me/', # string URL
    'apiKey':   '92560ffae9b8a0421...', # string public apiKey (ASCII, hex, Base64, ...)
    'secret':   '9aHjPmW+EtRRKN/Oi...'  # string private secret key
    'password': '6kszf4aci8r',          # string password
    'uid':      '123456',               # string user id
}
```


## Market Structure

```python
{
    'id':     'btcusd',   # string literal for referencing within an exchange
    'symbol': 'BTC/USD',  # uppercase string literal of a pair of currencies
    'base':   'BTC',      # uppercase string, base currency, 3 or more letters
    'quote':  'USD',      # uppercase string, quote currency, 3 or more letters
    'active': true,       # boolean, market status
    'precision': {        # number of decimal digits "after the dot"
        'price': 8,       # integer, might be missing if not supplied by the exchange
        'amount': 8,      # integer, might be missing if not supplied by the exchange
        'cost': 8,        # integer, very few exchanges actually have it
    },
    'limits': {           # value limits when placing orders on this market
        'amount': {
            'min': 0.01,  # order amount should be > min
            'max': 1000,  # order amount should be < max
        },
        'price': { ... }, # same min/max limits for the price of the order
        'cost':  { ... }, # same limits for order cost = price * amount
    },
    'info':      { ... }, # the original unparsed market info from the exchange
}
```


## Order Book Structure

```python
{
    'bids': [
        [ price, amount ], # [ float, float ]
        [ price, amount ],
        ...
    ],
    'asks': [
        [ price, amount ],
        [ price, amount ],
        ...
    ],
    'timestamp': 1499280391811, # Unix Timestamp in milliseconds (seconds * 1000)
    'datetime': '2017-07-05T18:47:14.692Z', # ISO8601 datetime string with milliseconds
}
```


## Ticker structure

```python
{
    'symbol':        string symbol of the market ('BTC/USD', 'ETH/BTC', ...)
    'info':        { the original non-modified unparsed reply from exchange API },
    'timestamp':     int (64-bit Unix Timestamp in milliseconds since Epoch 1 Jan 1970)
    'datetime':      ISO8601 datetime string with milliseconds
    'high':          float, # highest price
    'low':           float, # lowest price
    'bid':           float, # current best bid (buy) price
    'bidVolume':     float, # current best bid (buy) amount (may be missing or undefined)
    'ask':           float, # current best ask (sell) price
    'askVolume':     float, # current best ask (sell) amount (may be missing or undefined)
    'vwap':          float, # volume weighed average price
    'open':          float, # opening price
    'close':         float, # price of last trade (closing price for current period)
    'last':          float, # same as `close`, duplicated for convenience
    'previousClose': float, # closing price for the previous period
    'change':        float, # absolute change, `last - open`
    'percentage':    float, # relative change, `(change/open) * 100`
    'average':       float, # average price, `(last + open) / 2`
    'baseVolume':    float, # volume of base currency traded for last 24 hours
    'quoteVolume':   float, # volume of quote currency traded for last 24 hours
}
```


## OHLCV Structure

```python
[
    [
        1504541580000, # UTC timestamp in milliseconds, integer
        4235.4,        # (O)pen price, float
        4240.6,        # (H)ighest price, float
        4230.0,        # (L)owest price, float
        4230.7,        # (C)losing price, float
        37.72941911    # (V)olume (in terms of the base currency), float
    ],
    ...
]
```


# Private

## Balance Structure

```python
{
    'info':  { ... },    # the original untouched non-parsed reply with details

    //-------------------------------------------------------------------------
    # indexed by availability of funds first, then by currency

    'free':  {           # money, available for trading, by currency
        'BTC': 321.00,   # floats...
        'USD': 123.00,
        ...
    },

    'used':  { ... },    # money on hold, locked, frozen, or pending, by currency

    'total': { ... },    # total (free + used), by currency

    //-------------------------------------------------------------------------
    # indexed by currency first, then by availability of funds

    'BTC':   {           # string, three-letter currency code, uppercase
        'free': 321.00   # float, money available for trading
        'used': 234.00,  # float, money on hold, locked, frozen or pending
        'total': 555.00, # float, total balance (free + used)
    },

    'USD':   {           # ...
        'free': 123.00   # ...
        'used': 456.00,
        'total': 579.00,
    },

    ...
}
```


## Order Structure

```python
{
    'id':                '12345-67890:09876/54321', # string
    'datetime':          '2017-08-17 12:42:48.000', # ISO8601 datetime of 'timestamp' with milliseconds
    'timestamp':          1502962946216, # order placing/opening Unix timestamp in milliseconds
    'lastTradeTimestamp': 1502962956216, # Unix timestamp of the most recent trade on this order
    'status':     'open',         # 'open', 'closed', 'canceled'
    'symbol':     'ETH/BTC',      # symbol
    'type':       'limit',        # 'market', 'limit'
    'side':       'buy',          # 'buy', 'sell'
    'price':       0.06917684,    # float price in quote currency
    'amount':      1.5,           # ordered amount of base currency
    'filled':      1.1,           # filled amount of base currency
    'remaining':   0.4,           # remaining amount to fill
    'cost':        0.076094524,   # 'filled' * 'price' (filling price used where available)
    'trades':    [ ... ],         # a list of order trades/executions
    'fee': {                      # fee info, if available
        'currency': 'BTC',        # which currency the fee is (usually quote)
        'cost': 0.0009,           # the fee amount in that currency
        'rate': 0.002,            # the fee rate (if available)
    },
    'info': { ... },              # the original unparsed order structure as is
}
```


## Trade Structure

```python
{
    'info':         { ... },                    # the original decoded JSON as is
    'id':           '12345-67890:09876/54321',  # string trade id
    'timestamp':    1502962946216,              # Unix timestamp in milliseconds
    'datetime':     '2017-08-17 12:42:48.000',  # ISO8601 datetime with milliseconds
    'symbol':       'ETH/BTC',                  # symbol
    'order':        '12345-67890:09876/54321',  # string order id or undefined/None/null
    'type':         'limit',                    # order type, 'market', 'limit' or undefined/None/null
    'side':         'buy',                      # direction of the trade, 'buy' or 'sell'
    'takerOrMaker': 'taker'                     # string, 'taker' or 'maker'
    'price':        0.06917684,                 # float price in quote currency
    'amount':       1.5,                        # amount of base currency
    'cost':         0.10376526,                 # total cost (including fees), `price * amount`
    'fee':          {                           # provided by exchange or calculated by ccxt
        'cost':  0.0015,                        # float
        'currency': 'ETH',                      # usually base currency for buys, quote currency for sells
        'rate': 0.002,                          # the fee rate (if available)
    },
}
```


## Address Structure

```python
{
    'currency': currency, # currency code
    'address': address,   # address in terms of requested currency
    'tag': tag,           # tag / memo / paymentId for particular currencies (XRP, XMR, ...)
    'info': response,     # raw unparsed data as returned from the exchange
}
```


## Transaction Structure

```python
{
    'info':      { ... },    # the JSON response from the exchange as is
    'id':       '123456',    # exchange-specific transaction id, string
    'txid':     '0x68bfb29821c50ca35ef3762f887fd3211e4405aba1a94e448a4f218b850358f0',
    'timestamp': 1534081184515,             # timestamp in milliseconds
    'datetime': '2018-08-12T13:39:44.515Z', # ISO8601 string of the timestamp
    'addressFrom': '0x38b1F8644ED1Dbd5DcAedb3610301Bf5fa640D6f', # sender
    'address':  '0x02b0a9b7b4cDe774af0f8e47cb4f1c2ccdEa0806', # "from" or "to"
    'addressTo': '0x304C68D441EF7EB0E2c056E836E8293BD28F8129', # receiver
    'tagFrom', '0xabcdef', # "tag" or "memo" or "payment_id" associated with the sender
    'tag':      '0xabcdef' # "tag" or "memo" or "payment_id" associated with the address
    'tagTo': '0xhijgklmn', # "tag" or "memo" or "payment_id" associated with the receiver
    'type':     'deposit',   # or 'withdrawal', string
    'amount':    1.2345,     # float (does not include the fee)
    'currency': 'ETH',       # a common unified currency code, string
    'status':   'pending',   # 'ok', 'failed', 'canceled', string
    'updated':   undefined,  # UTC timestamp of most recent status change in ms
    'comment':  'a comment or message defined by the user if any',
    'fee': {                 # the entire fee structure may be undefined
        'currency': 'ETH',   # a unified fee currency code
        'cost': 0.1234,      # float
        'rate': undefined,   # approximately, fee['cost'] / amount, float
    },
}
```


## Fee Structure

```python
{
    'type': takerOrMaker,
    'currency': 'BTC', # the unified fee currency code
    'rate': percentage, # the fee rate, 0.05% = 0.0005, 1% = 0.01, ...
    'cost': feePaid, # the fee cost (amount * fee rate)
}
```


## Ledger Entry Structure

```python
{
    'id': 'string-id',                      # id of the ledger entry, a string
    'direction': 'out',                     # or 'in'
    'account': '06d4ab58-dfcd-468a',        # string id of the account if any
    'referenceId': 'bf7a-d4441fb3fd31',     # string id of the trade, transaction, etc...
    'referenceAccount': '3146-4286-bb71',   # string id of the opposite account (if any)
    'type': 'trade',                        # string, reference type, see below
    'currency': 'BTC',                      # string, unified currency code, 'ETH', 'USDT'...
    'amount': 123.45,                       # absolute number, float (does not include the fee)
    'timestamp': 1544582941735,             # milliseconds since epoch time in UTC
    'datetime': "2018-12-12T02:49:01.735Z", # string of timestamp, ISO8601
    'before': 0,                            # amount of currency on balance before
    'after': 0,                             # amount of currency on balance after
    'fee': {                                # object or or undefined
        'cost': 54.321,                     # absolute number on top of the amount
        'currency': 'ETH',                  # string, unified currency code, 'ETH', 'USDT'...
    },
    'info': { ... },                        # raw ledger entry as is from the exchange
}
```

