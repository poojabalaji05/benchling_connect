"""Reader file for Roche Cedex HiRes Instrument"""

import pandas as pd

from allotropy.allotrope.pandas_util import read_csv, read_excel
from allotropy.named_file_contents import NamedFileContents
from allotropy.exceptions import AllotropeConversionError
from allotropy.parsers.roche_cedex_hires import constants



class RocheCedexHiResReader:
    @classmethod
    def read(cls, named_file_contents: NamedFileContents) -> pd.DataFrame:
        if named_file_contents.original_file_name.endswith(".csv"):
            return read_csv(
                named_file_contents.contents,
                index_col=False,
                encoding=named_file_contents.encoding,
            )
        elif named_file_contents.original_file_name.endswith(".xlsx"):
            return read_excel(named_file_contents.contents.name)
        else:
            message = f"{constants.UNSUPPORTED_FILE_FORMAT_ERROR} '{named_file_contents.original_file_name}'"
            raise AllotropeConversionError(message)
