import os
from stuff.input import read_from_csv_single, read_from_csv_multiple, read_from_csv_dir_alpabetically


def _write_csv(filename, lines):
    with open(filename, 'w') as f:
        f.writelines('\n'.join(lines))

def test_read_csv_single(tmpdir):
    filename = tmpdir / 'my.csv'

    _write_csv(filename,
               [r'AT666666666666666666;Bezahlung Karte                              MC/000009231|POS          U354  K002 31.01. 22:05|FREIGEIST\\GRAZ\8010         0;02.02.2023;31.01.2023;-70,00;EUR',
                r'AT666666666666666666;BX/000009219|Entgelt für Nichtdurchführung von Aufträgen;25.01.2023;25.01.2023;-6,90;EUR',
                ])

    df = read_from_csv_single(filename)

    df['account'].iloc[0] == 'AT666666666666666666'
    df['account'].iloc[1] == 'AT666666666666666666'

    df['info'].iloc[0] == r'Bezahlung Karte                              MC/000009231|POS          U354  K002 31.01. 22:05|FREIGEIST\\GRAZ\8010         0'
    df['info'].iloc[1] == r'BX/000009219|Entgelt für Nichtdurchführung von Aufträgen'

def test_read_csv_multiple(tmpdir):
    filename1 = tmpdir / 'my1.csv'
    filename2 = tmpdir / 'my2.csv'

    _write_csv(filename1,
               [
                   r'AT666666666666666666;Bezahlung Karte                              MC/000009231|POS          U354  K002 31.01. 22:05|FREIGEIST\\GRAZ\8010         0;02.02.2023;31.01.2023;-70,00;EUR',
                   r'AT666666666666666666;BX/000009219|Entgelt für Nichtdurchführung von Aufträgen;25.01.2023;25.01.2023;-6,90;EUR',
               ])
    _write_csv(filename2,
               [
                   'AT666666666666666666;Bezahlung Karte                              MC/000009217|POS          2800  K002 23.01. 12:00|SPAR DANKT 3618\\WELS\4600;24.01.2023;23.01.2023;-3,84;EUR',
               ])

    df = read_from_csv_multiple([filename1, filename2])

    df['account'].iloc[0] == 'AT666666666666666666'
    df['account'].iloc[1] == 'AT666666666666666666'
    df['account'].iloc[2] == 'AT666666666666666666'

    df['info'].iloc[0] == r'Bezahlung Karte                              MC/000009231|POS          U354  K002 31.01. 22:05|FREIGEIST\\GRAZ\8010         0'
    df['info'].iloc[1] == r'BX/000009219|Entgelt für Nichtdurchführung von Aufträgen'
    df['info'].iloc[2] == r'Bezahlung Karte                              MC/000009217|POS          2800  K002 23.01. 12:00|SPAR DANKT 3618\\WELS\4600'

def test_read_csv_dir_alphabetically(tmpdir, monkeypatch):
    filename1 = tmpdir / '2023-01.csv'
    filename2 = tmpdir / '2023-02.csv'

    _write_csv(filename1,
               [
                   r'AT666666666666666666;Bezahlung Karte                              MC/000009231|POS          U354  K002 31.01. 22:05|FREIGEIST\\GRAZ\8010         0;02.02.2023;31.01.2023;-70,00;EUR',
                   r'AT666666666666666666;BX/000009219|Entgelt für Nichtdurchführung von Aufträgen;25.01.2023;25.01.2023;-6,90;EUR',
               ])
    _write_csv(filename2,
               [
                   r'AT666666666666666666;Bezahlung Karte                              MC/000009217|POS          2800  K002 23.01. 12:00|SPAR DANKT 3618\\WELS\4600;24.01.2023;23.01.2023;-3,84;EUR',
               ])

    def my_listdir(d):
        return [filename2, filename1]
    monkeypatch.setattr(os, 'listdir', my_listdir)

    df = read_from_csv_dir_alpabetically(tmpdir)

    assert df['account'].iloc[0] == 'AT666666666666666666'
    assert df['account'].iloc[1] == 'AT666666666666666666'
    assert df['account'].iloc[2] == 'AT666666666666666666'

    assert df['info'].iloc[0] == r'Bezahlung Karte                              MC/000009231|POS          U354  K002 31.01. 22:05|FREIGEIST\\GRAZ\8010         0'
    assert df['info'].iloc[1] == r'BX/000009219|Entgelt für Nichtdurchführung von Aufträgen'
    assert df['info'].iloc[2] == r'Bezahlung Karte                              MC/000009217|POS          2800  K002 23.01. 12:00|SPAR DANKT 3618\\WELS\4600'
