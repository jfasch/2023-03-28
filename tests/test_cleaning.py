from stuff.conversions import make_float, clean_data
from datetime import datetime

import pandas
import pytest

def test_currency():
    crap = '1,234.567,70'
    assert make_float(crap) == pytest.approx(1_234_567.7)

def test_full_clean():
    df = pandas.DataFrame({
        'account': ['AT666666666666666666'],
        'info': [r'Bezahlung Karte                              MC/000009231|POS          '
                 r'U354  K002 31.01. 22:05|FREIGEIST\\GRAZ\8010         0'],
        'time_booked': ['02.02.2023'],
        'time_valuta': ['31.01.2023'],
        'amount': ['-70,00'],
        'unit': ['EUR'],
    })

    df = clean_data(df)

    assert df['amount'].iloc[0] == pytest.approx(-70)
    assert df['time_booked'].iloc[0] == datetime(year=2023, month=2, day=2)
