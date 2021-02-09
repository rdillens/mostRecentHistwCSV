import cbpro as cb
from clients.keys.api_keys import key, b64secret, passphrase
import helpful_methods as hm
from datetime import datetime as dt
import pprint

start_time = dt.now().timestamp()
try:
    auth_client = cb.AuthenticatedClient(key, b64secret, passphrase)
    accounts = auth_client.get_accounts()
    products = auth_client.get_products()
    currencies = auth_client.get_currencies()
except Exception as inst:
    print(f'Error type: {type(inst)}\n{inst} \nError connecting sandbox client')
    raise
else:
    print(f'API authenticated! {len(accounts)} accounts, {len(products)} products, {len(currencies)} currencies\n')
    hm.fill_time(start_time)
