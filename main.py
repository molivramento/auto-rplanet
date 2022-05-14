import setup
import time
import schedule
import asyncio
from action import Action
from analysis import Request

r = Request(setup.api, 's.rplanet')
action = Action()


def claim_limit():
    table = 'claimlimits'
    key_type = 'name'
    user = 'molivramento'
    response = r.fetch(table=table, user=user, key_type=key_type)['rows']
    return response


def verify_claim():
    time_now = time.time()
    amount_claim = float(r.rplanet()['result'].split()[0])
    time_diff = int((time_now - claim_limit()[0]["extended_at"]) / 60 / 60)
    base_limit = 50796
    n_limit = base_limit

    for i in range(time_diff):
        n_limit = n_limit - (n_limit * 0.01)

    if n_limit < amount_claim:
        quantity = base_limit - n_limit
        data = {
            'from': setup.user,
            'to': 's.rplanet',
            'quantity': f'{quantity}:.4f AETHER',
            'memo': 'extend claim limit'
        }
        name = 'transfer'
        account = 'e.planet'
        act = action.claim(name=name, acc=account, data=data)
        print(f'Limite atual: {n_limit} é necessário recarregar!')
        asyncio.get_event_loop().run_until_complete(act)

    data_claim = {
        'to': setup.user,
    }
    name_claim = 'claim'
    account_s = 's.rplanet'
    act_claim = action.claim(name=name_claim, acc=account_s, data=data_claim)
    asyncio.get_event_loop().run_until_complete(act_claim)


schedule.every().hour.at(':25').do(verify_claim)

while True:
    schedule.run_pending()
    time.sleep(1)
