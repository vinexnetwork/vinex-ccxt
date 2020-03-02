import ccxt
import config
import time
import utils.ccxt_utils as ccxt_utils
from pprint import pprint

# defaultType:
# - spot
# - margin
# - future

# Margin
api_key = config.api_key['binance-test']

api = ccxt.binance2({
    'apiKey': api_key['apiKey'],
    'secret': api_key['secret'],
    'options': {'defaultType': 'margin'},
})

# 1. Get Markets
# markets = api.fetch_markets()
# print(f'Markets: {len(markets)}\n{markets[0]}')

# print(api.fetch_ticker('BTC/USDT')['last'])


# 2. Get My Balances
# balance = api.fetch_balance()
# print(balance)
# print(balance['free'])
# print(balance['used'])

# pprint(ccxt_utils.fetch_balance(api, is_show_info=False))

# # 3. Get All Orders
# orders = api.fetch_orders('ETH/USDT')
# print(orders)

# # 4. Get Open Orders
# orders = api.fetch_open_orders('BNB/USDT')
# pprint(orders)

# print(len(api.fetch_orders('BNB/USDT')))
# print(len(api.fetch_open_orders('BNB/USDT')))
# print(len(api.fetch_closed_orders('BNB/USDT')))


# # 5. Get Order Detail
# order = api.fetch_order(id='351640418', symbol='BNB/USDT')
# print(order)


# 6. Get My Trades
# trades = api.fetch_my_trades(symbol='BNB/USDT')
# pprint(trades[-1])


# 7. Create Order
# Order Type: Limit
# order = api.create_order(symbol='BNB/USDT', type='limit', side='sell', amount=1, price=60)

# Order Type: Market
# order = api.create_order(symbol='BNB/USDT', type='market', side='sell', amount=1)

# Order Type: Stop Limit
# - STOP_LOSS_LIMIT
# - TAKE_PROFIT_LIMIT
# order = self.instance.create_order(symbol, type, side,  amount, limit_price, params)
# order = api.create_order(symbol='BNB/USDT', type='take_profit_limit', side='sell', amount=1, price=60, params={'stopPrice': 50})
# order = api.create_order(symbol='BNB/USDT', type='stop_loss_limit', side='sell', amount=1, price=10, params={'stopPrice': 11})

# TODO: Order Type: OCO

# print(order)


# # 8. Cancel Order
# result = api.cancel_order(id='352590726', symbol='BNB/USDT')
# print(result)


# TODO: OCO
# * OCO: Create Order: create_order
# * OCO: Cancel Order: cancel_order
#
# * OCO: Get Open Orders: fetch_open_orders
# * OCO: Get All Orders: fetch_orders
# * OCO: Get Order Detail: fetch_order


# -----------------------------
# Spot
# -----------------------------
# OCO: Get Open Orders: fetch_open_orders
# print(api.privateGetOpenOrderList())

# OCO: Get All Orders: fetch_orders
# print(api.privateGetAllOrderList({'symbol': 'BNB/USDT'}))

# OCO: Get Order Detail: fetch_order
# print(api.privateGetOrderList({'orderListId': 100}))




# In order to create an OCO order, the following parameters are required:
# - symbol
# - side
# - quantity
# - price
# - stopPrice
# - stopLimitPrice
# - stopLimitTimeInForce

# order = exchange.private_post_order_oco({ "symbol": "BTCUSDT", "side": "buy", "quantity": 0.002, "price": 7000, "stopPrice": 10000, "stopLimitPrice": 10000, "stopLimitTimeInForce": "GTC"})


# -----------------------------
# Margin
# -----------------------------
# OCO: Get Open Orders: fetch_open_orders
# print(api.sapiGetMarginOpenOrderList())

# OCO: Get All Orders: fetch_orders
# print(api.privateGetAllOrderList({'symbol': 'BNB/USDT'}))

# OCO: Get Order Detail: fetch_order
# print(api.privateGetOrderList({'orderListId': 100}))


# -----------------------------
# Margin: Transfer, Borrow, Repay
# -----------------------------

# Success: -> {'tranId': 6942691041}
# Error: -> Exception

# Transfer Params:
# - type: 1: transfer from main account to margin account 2: transfer from margin account to main account

# print(api.transfer(code='USDT', amount=1, type=2))
#
# print(api.borrow(code='USDT', amount=1))
#
# print(api.repay(code='USDT', amount=1))
