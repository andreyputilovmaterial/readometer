
from pathlib import Path

err_import = None
try:
    import win32com.client
except ImportError as err:
    err_import = err

class Reader:

    def __init__(self,fname):
        if err_import:
            raise err_import
        self.fname_mdd = Path(fname).with_suffix('.mdd').resolve()
        if not self.fname_mdd.is_file():
            raise FileNotFoundError('MDD File not found: {f}'.format(f=self.fname_mdd))
        self.fname_data = Path(fname).with_suffix('.ddf').resolve()
        if not self.fname_data.is_file():
            raise FileNotFoundError('DDF File not found: {f}'.format(f=self.fname_data))
        # self.mdmdoc = win32com.client.Dispatch('MDM.Document')

    def __enter__(self):
        # self.mdmdoc.Open(self.fname_mdd)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # try:
        #     if self.mdmdoc:
        #         self.mdmdoc.Close()
        # except:
        #     pass
        pass

    def count_records(self):
        def sanitize_name(n):
            return '{n}'.format(n=n).replace('"','')
        sfilter = 'true'
        svariable_to_count = 'COMP'
        try:
            oconnection = win32com.client.Dispatch('ADODB.Connection')
            try:
                orecordset = win32com.client.Dispatch('ADODB.Recordset')
                oconnection.Open("Provider=mrOleDB.Provider.2;Data Source=mrDataFileDsc;Location="+sanitize_name(self.fname_data)+";Initial Catalog="+sanitize_name(self.fname_mdd)+";MR Init MDM Access=0;")
                orecordset.Open("SELECT COUNT("+sanitize_name(svariable_to_count)+") AS SQLCountFromR FROM VDATA WHERE " + sanitize_name(sfilter) , oconnection)
                if orecordset.BOF == False or orecordset.EOF == False:
                    return orecordset.Fields["SQLCountFromR"].Value
                else:
                    return 0
            finally:
                try:
                    orecordset.Close()
                except:
                    pass
        finally:
            try:
                oconnection.Close()
            except:
                pass


