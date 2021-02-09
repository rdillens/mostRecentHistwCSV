from pathlib import Path
import shelve
import history as hi
import helpful_methods as hm
import csv
import pprint


def gen_shelf(obj, key, f_name, f_path=None):
    if f_path is not None:
        f_name = f_path + '/' + f_name
        f_path = Path(f_path)
        if not f_path.exists():
            f_path.mkdir()
    # outFile = shelve.open(f_name)
    with shelve.open(f_name) as outFile:
        for o in obj:
            try:
                if outFile[o[key]] != o:
                    outFile[o[key]] = o
            except KeyError:
                outFile[o[key]] = o
    # outFile.close()
    return


def build_dictionary(currencies, products):
    df = {}
    for i, c in enumerate(currencies):
        if c['details']['type'] == 'crypto':
            c_dict = {}
            c_prods = {}
            g_dict = {}
            prods = sorted([p['id'] for p in products if p['base_currency'] == c['id']])
            for j, p in enumerate(prods):
                for g in reversed(sorted(hi.gran)):
                    print(f'\r{i}. {c["name"]} {p}', end='')
                    f_name = p + str(g)
                    f = hm.gen_f(f_name, p, ext='.csv', base_path='products')
                    with open(f) as csv_file:
                        data = csv.reader(csv_file)
                        g_dict[g] = [list(row) for row in data]
                c_prods[p] = g_dict
                # Store data dictionary into pformat shelf file
                f_name = '../backup/' + p
                with shelve.open(f_name) as dd:
                    dd = pprint.pformat(g_dict)
            c_dict['products'] = c_prods
            df[c['name']] = c_dict
            # pprint.pprint(df[c['name']], compact=True)
            print(f'\r{i}. {c["name"]} Done', end='. ')
    print('Loaded dictionary')
    return df


def smooth_data(currencies, products, df):
    for i, c in enumerate(currencies):
        if c['details']['type'] == 'crypto':
            prods = sorted([p['id'] for p in products if p['base_currency'] == c['id']])
            for j, p in enumerate(prods):
                for g in reversed(sorted(hi.gran)):
                    print(f'\r{i}. {c["name"]} {p}', end='')
                    pprint.pprint(df[c][p][g])
    return df


def validate_data():
    return


def interpolate_data():
    return
