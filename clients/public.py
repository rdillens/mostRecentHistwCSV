import cbpro
import helpful_methods as hm
from datetime import datetime as dt

start_time = dt.now().timestamp()
try:
    public_client = cbpro.PublicClient()
    products = public_client.get_products()
    currencies = public_client.get_currencies()
except Exception as inst:
    print(f'Error type: {type(inst)}\n{inst} \nError connecting public client')
    raise
finally:
    hm.fill_time(start_time, msg='slept')
