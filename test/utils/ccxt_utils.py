def fetch_balance(api, hide_zero_amount=True):
    balance = api.fetch_balance()

    balance.pop('info')

    if hide_zero_amount:
        free = balance.pop('free')
        used = balance.pop('used')
        total = balance.pop('total')

        for dict_balance in [free, used, total]:
            for key in dict_balance.copy():
                if dict_balance[key] == 0:
                    dict_balance.pop(key)

        for key in balance.copy():
            if balance[key]['total'] == 0:
                balance.pop(key)

        balance['free'] = free
        balance['used'] = used
        balance['total'] = total

    return balance
