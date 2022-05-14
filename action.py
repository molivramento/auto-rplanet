import asyncio
from aioeos import EosAccount, EosAction, EosJsonRpc, EosTransaction, exceptions
import setup


class Action:
    async def claim(self, name, data, acc):
        account = EosAccount(setup.user, private_key=setup.private_key)
        rpc = EosJsonRpc('https://' + setup.api)
        block = await rpc.get_head_block()
        action = EosAction(
            account=acc,
            name=name,
            authorization=[account.authorization(name)],
            data=data)
        try:
            transaction = EosTransaction(
                ref_block_num=block['block_num'] & 65535,
                ref_block_prefix=block['ref_block_prefix'],
                actions=[action]
            )
            try:
                ac = await rpc.sign_and_push_transaction(transaction, keys=[account.key])
                if name == 'claim':
                    print(
                        ac['processed']
                        ['action_traces'][0]
                        ['inline_traces'][0]
                        ['inline_traces'][1]
                        ['act']
                        ['data']
                        ['quantity']
                    )
                elif name == 'transfer':
                    print(ac)
            except Exception as e:
                print('Deu ruim...', e)
        except Exception as e:
            print(e)


# atc = Action()
# claim = atc.claim(acc='s.rplanet', name='claim', data={'to': 'molivramento'})
# asyncio.get_event_loop().run_until_complete(claim)
