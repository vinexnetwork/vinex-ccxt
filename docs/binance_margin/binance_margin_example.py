import ccxt
import config

# Public
# * Get Markets: fetch_markets
# * Get Ticker: fetch_ticker
# * Get Orderbook: fetch_order_book
# * Get Market Trades: fetch_trades
# * Get Candlestick (OHLV) (Optional): fetch_ohlcv
#
# Private
# * Get my balances: fetch_balance
#
# * Create Order: create_order
# * Cancel Order: cancel_order
#
# * Get Open Orders: fetch_open_orders
# * Get All Orders: fetch_orders
# * Get Order Detail: fetch_order
# * Get My Trades: fetch_my_trades
#
# Full docs: https://github.com/ccxt/ccxt/wiki/Manual#overview
#

# Margin
api_key = config.api_key['binance-test']

api = ccxt.binance2({
    'apiKey': api_key['apiKey'],
    'secret': api_key['secret'],
    'options': {'defaultType': 'margin'},
})


print('Markets:', api.fetch_markets())
print('Ticker:', api.fetch_ticker(symbol='BTC/USDT'))
print('Orderbook:', api.fetch_order_book(symbol='BTC/USDT'))
print('Trades:', api.fetch_trades(symbol='BTC/USDT'))
print('Candlestick:', api.fetch_ohlcv(symbol='BTC/USDT'))

print('My Balance:', api.fetch_balance())

print('My Open Orders:', api.fetch_open_orders(symbol='BTC/USDT'))
print('My Trades:', api.fetch_my_trades(symbol='BTC/USDT'))

# Create Order
# Order Type: Limit
order = api.create_order(symbol='BNB/USDT', type='limit', side='sell', amount=1, price=60)

# Order Type: Market
order = api.create_order(symbol='BNB/USDT', type='market', side='sell', amount=1)

# Order Type: Stop Limit
# - STOP_LOSS_LIMIT
# - TAKE_PROFIT_LIMIT
# order = api.create_order(symbol, type, side,  amount, limit_price, params)
order = api.create_order(symbol='BNB/USDT', type='take_profit_limit', side='sell', amount=1, price=60, params={'stopPrice': 50})
order = api.create_order(symbol='BNB/USDT', type='stop_loss_limit', side='sell', amount=1, price=10, params={'stopPrice': 11})
