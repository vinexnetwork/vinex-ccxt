# Binance API

## Binance Margin

```python
# -----------------------------
# Margin: Balance
# -----------------------------

api.fetch_balance()

# result:
# {
#     'USDT': {
#         'free': 8.9105,
#         'total': 8.9105,
#         'used': 0.0,
#         'borrowed': 0.0,          # borrowed
#         'net': 8.9105,            # net asset
#     },
#     'free': {'USDT': 8.9105},
#     'total': {'USDT': 8.9105},
#     'used': {'USDT': 0.0}
# }
```


```python
# -----------------------------
# Margin: Transfer, Borrow, Repay
# -----------------------------

# Success: -> {'tranId': 6942691041}
# Error: -> Exception

# Transfer Params:
# - type: 1: transfer from main account to margin account 2: transfer from margin account to main account

api.transfer(code='USDT', amount=1, type=2)

api.borrow(code='USDT', amount=1)

api.repay(code='USDT', amount=1)

```

