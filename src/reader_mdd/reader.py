
from pathlib import Path


class Reader:

    def __init__(self,fname):
        self.fname = Path(fname).resolve()
        if not self.fname.is_file():
            raise FileNotFoundError('File not found: {f}'.format(f=self.fname))
        raise NotImplementedError('Reading MDD is not implemented yet')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def count_records(self):
        return None


