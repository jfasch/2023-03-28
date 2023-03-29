import os
import re
import sys
import typing
import pandas as pd

from stuff.conversions import clean_data
from stuff.input import read_from_csv_dir


def write_to_csv(df, filename):
    df.to_csv(
        filename,
        sep=';', encoding='iso-8859-1',
        index=False,
    )
    
def categorize(df: pd.DataFrame) -> pd.DataFrame:
    def make_category(info):
        if info.startswith('Bezahlung Karte'):
            which, terminal, organization = info.split('|')
    
            if organization.startswith('ORPHEUM BAR'):
                return 'goingout'
            if organization.startswith('BILLA DANKT'):
                return 'living'
            if organization.startswith('HERVIS'):
                return 'sport'
            if organization.startswith('SHELL'):
                return 'car'
            return 'card-unknown'
        else:
            return 'unknown'
    
    df['category'] = df['info'].apply(make_category)    # polars!!
    return df

INPUTDIR = sys.argv[1]
OUTPUTFILE = sys.argv[2]

data = read_from_csv_dir(INPUTDIR)
data = clean_data(data)
data = categorize(data)
write_to_csv(data, OUTPUTFILE)
