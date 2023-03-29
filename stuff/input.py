import pandas as pd
import re, os, typing, functools


def read_from_csv_single(filename):
    return pd.read_csv(
        filename, 
        sep=';',
        names=('account', 'info', 'time_booked', 'time_valuta', 'amount', 'unit'))

def read_from_csv_multiple(filenames):
    ret = pd.DataFrame()
    for fn in filenames:
        ret = pd.concat([ret, read_from_csv_single(fn)])
    return ret

def read_from_csv_dir_alpabetically(dirname):
    pattern = re.compile(r'\d\d\d\d-\d\d.csv')

    names = os.listdir(dirname)
    names.sort()
    names = map(functools.partial(os.path.join, dirname), names)
    return read_from_csv_multiple((n for n in names if os.path.isfile(n) and pattern.search(n)))
