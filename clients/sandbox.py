import cbpro
from clients.keys.sandbox_keys import key, b64secret, passphrase
import helpful_methods as hm
from datetime import datetime as dt

start_time = dt.now().timestamp()
url_str = "https://api-public.sandbox.pro.coinbase.com"
try:
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase, api_url=url_str)
    accounts = auth_client.get_accounts()
    products = auth_client.get_products()
    currencies = auth_client.get_currencies()
except Exception as inst:
    print(f'Error type: {type(inst)}\n{inst} \nError connecting sandbox client')
    raise
else:
    print(f'Sandbox authenticated! {len(accounts)} accounts, {len(products)} products, {len(currencies)} currencies\n')
    hm.fill_time(start_time, msg='slept')
