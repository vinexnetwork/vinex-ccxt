def fetch_balance(api, is_show_zero_amount=False, is_show_info=False):
    """

    {
        asset1,
        asset2,

        free,
        used,
        total,
        info,
    }
    """
    balance = api.fetch_balance()

    free = balance.pop('free')
    used = balance.pop('used')
    total = balance.pop('total')
    info = balance.pop('info')

    refine_balance = dict()

    if is_show_zero_amount:
        refine_balance = balance.copy()
        refine_balance['free'] = free
        refine_balance['used'] = used
        refine_balance['total'] = total
    else:
        showed_assets = list()

        for asset, asset_info in balance.items():
            for key, value in asset_info.items():
                if value and abs(value) > 0:
                    showed_assets.append(asset)
                    break

        refine_balance['free'] = dict()
        refine_balance['used'] = dict()
        refine_balance['total'] = dict()

        for asset in showed_assets:
            refine_balance[asset] = balance[asset]
            refine_balance['free'][asset] = free[asset]
            refine_balance['used'][asset] = used[asset]
            refine_balance['total'][asset] = total[asset]

    if is_show_info:
        refine_balance['info'] = info

    return refine_balance
