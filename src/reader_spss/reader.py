
from pathlib import Path


class Reader:

    def __init__(self,fname):
        self.fname = Path(fname).resolve()
        if not self.fname.is_file():
            raise FileNotFoundError('File not found: {f}'.format(f=self.fname))
        raise NotImplementedError('Reading SPSS is not implemented yet')

    def count_records(self):
        return None


