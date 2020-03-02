import config

import ccxt

user = config.proxy_account['user']
password = config.proxy_account['password']

proxy_path = '196.240.249.5:13555'

http_proxy = f'http://{user}:{password}@{proxy_path}'

proxies = list()

proxies.append({
    "http": http_proxy,
    "https": http_proxy,
})

api = ccxt.vinex({'proxies': proxies})
# api.urls['api']  = 'https://dev-backend.vinex.network/api/v2'

api.fetch_ticker('BTC/USDT')
