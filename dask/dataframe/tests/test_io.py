import gzip
import pandas as pd
import pandas.util.testing as tm
import dask

import dask.dataframe as dd
from dask.dataframe.io import read_csv, file_size

from dask.utils import filetext

text = """
name,amount
Alice,100
Bob,-200
Charlie,300
Dennis,400
Edith,-500
Frank,600
""".strip()


def test_read_csv():
    with filetext(text) as fn:
        f = read_csv(fn, header=0, chunkbytes=30)
        assert list(f.columns) == ['name', 'amount']
        assert f.npartitions > 1
        result = f.compute(get=dask.get).sort('name')
        assert (result.values == pd.read_csv(fn).sort('name').values).all()


def test_filetext():
    with filetext(text) as fn:
        assert file_size(fn) == len(text)
    with filetext(text, open=gzip.open) as fn:
        assert file_size(fn, 'gzip') == len(text)
