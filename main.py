import clients.api as cl
import history as hi
import helpful_methods as hm
import main_functions as mf

# Generate / update shelf files
mf.gen_shelf(cl.currencies, 'name', 'currencies', f_path='../backup')
mf.gen_shelf(cl.products, 'id', 'products', f_path='../backup')

# Build / load data into dictionary object
data_dict = mf.build_dictionary(cl.currencies, cl.products)

gr = hi.gran[:]
prods = sorted([p['id'] for p in cl.products])

for j, g in enumerate(reversed(gr)):
    for i, p in enumerate(prods):
        prod_str = f'\r({i+1+(j*len(prods)):3d}/{len(gr)*len(prods):3d}) {g:5d}-{p:9s}'
        print(prod_str, end=' ')
        f_name = p + str(g)
        f = hm.gen_f(f_name, p, ext='.csv', base_path='products')
        df = hi.csv_to_df(f, p, g)
        if not df.empty:
            df = hi.update_to_present(f, df, p, g)
