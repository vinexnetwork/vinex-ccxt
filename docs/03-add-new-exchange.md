----------------------------------------
# Add New Exchange
----------------------------------------

## NOTE:

**Buy orderbook: sort by desc**
> Prices and amounts are floats. The bids array is sorted by price in descending order.


### Precision

### Minimum Order Amount

### Rate Limit
rateLimit: A request rate limit in milliseconds. Specifies the required minimal delay between two consequent HTTP requests to the same exchange. The built-in rate-limiter is disabled by default and is turned on by setting the enableRateLimit property to true.


----------------------------------------
# QTrade
----------------------------------------

### Precision
SNOW:
- price: 8
- amount: 6

### Minimum Order Amount

minimum order amount: 0.0001 BTC
{"errors":[{"code":"too_small","title":"Trade amount is below minimum. Total value must be greater than 0.0001 BTC."}]}


----------------------------------------
# Vinex
----------------------------------------

### Rate Limit
200


----------------------------------------
# Biki
----------------------------------------

### Rate Limit

- Public interface: We limit the invocation of public interface via IP: up to 6 requests every 2s.

- Private interface: We limit the invocation of private interface via user ID: up to 6 requests every 2s.

=> RateLimit: 400



----------------------------------------
# Merge new exchange from ccxt's pull request
----------------------------------------

```bash
# 1. Checkout new branch
feature/new-exchange

# 2. Add exchange js


# 3. Build
#npm run build-without-docs

npm run transpile

# 4. Merge python code to vinex-ccxt
meld ccxt/python/ccxt vinex-ccxt/ccxt

# 5. Build and publish to pypi

```

