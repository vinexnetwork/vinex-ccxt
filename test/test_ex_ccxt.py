import config

import ccxt

exchange_ids = [
    'whitebit',
    # 'vinex',
]


def test_public_api():
    print('>>>>>>>>>>>> Test public API <<<<<<<<<<<<')

    for exchange_id in exchange_ids:
        exchange_class = getattr(ccxt, exchange_id)

        api = exchange_class()

        print(f'>>> Test exchange: {exchange_id}')

        # 1. Markets
        # print(f"- Markets: {api.fetch_markets()}")

        # 2. Ticker
        # print(f"- Ticker: {api.fetch_ticker('BTC/USDT')}")

        # 3. Order book
        # order_book = api.fetch_order_book('BTC/USDT')
        # print(f"- Order Book: len={len(order_book)}, order_book={order_book}")

        # 4. Trades
        # trades = api.fetch_trades('BTC/USDT')
        # print(f"- Trades: len={len(trades)}, trades={trades}")


def test_private_api():
    print('>>>>>>>>>>>> Test private API <<<<<<<<<<<<')

    for exchange_id in exchange_ids:
        exchange_class = getattr(ccxt, exchange_id)

        # api = exchange_class()

        api_key = config.api_key['whitebit-dev']

        api = exchange_class({
            'apiKey': api_key['apiKey'],
            'secret': api_key['secret'],
        })

        print(f'>>> Test exchange: {exchange_id}')

        # symbol = 'BTC/USDT'
        symbol = 'XST/BTC'

        # 1. Balances
        # balances = api.fetch_balance()['XST']
        # print(f'- Balances: {balances}')

        # 2. List Orders
        # open_orders = api.fetch_open_orders(symbol)
        # print(f'- Open Orders: len={len(open_orders)}, orders={open_orders}')

        # # closed_orders = api.fetch_closed_orders(symbol, since=int(time.time() * 1000))
        # # closed_orders = api.fetch_closed_orders(symbol, limit=1)
        # closed_orders = api.fetch_closed_orders(symbol)
        # print(f'- Open Orders: len={len(closed_orders)}, orders={closed_orders}')

        # # orders = api.fetch_orders()         # Some exchange don't support get orders for all markets
        # orders = api.fetch_orders(symbol)
        # print(f'- Orders: len={len(orders)}, orders={orders}')

        # 2. Create Order
        # order = api.create_order(symbol, 'limit', 'sell', 1, 100)
        # print(f'- Order: {order}')

        # 3. Cancel Order
        order = api.cancel_order(id=193106610, symbol=symbol)
        print(f'- Order: {order}')


if __name__ == '__main__':
    # test_public_api()

    test_private_api()
