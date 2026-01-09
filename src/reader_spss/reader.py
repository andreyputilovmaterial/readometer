
from pathlib import Path


pyreadstat = None
err_import = None
try:
    import pyreadstat
except ImportError as err:
    err_import = err


class Reader:

    def __init__(self,fname):
        if err_import:
            raise err_import
        self.fname = Path(fname).resolve()
        if not self.fname.is_file():
            raise FileNotFoundError('File not found: {f}'.format(f=self.fname))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def count_records(self):
        count = 0
        for df, _ in pyreadstat.read_file_in_chunks(pyreadstat.read_sav,self.fname,chunksize=10000):
            count += len(df)
        return count


