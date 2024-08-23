from pathlib import PureWindowsPath

import numpy as np
import pandas as pd

from allotropy.exceptions import AllotropeConversionError
from allotropy.named_file_contents import NamedFileContents
from allotropy.parsers.utils.pandas import (
    assert_not_empty_df,
    df_to_series_data,
    parse_header_row,
    read_csv,
    read_excel,
    SeriesData,
    split_header_and_data,
)
from allotropy.types import IOType


class UnchainedLabsLunaticReader:
    data: pd.DataFrame
    header: SeriesData

    def __init__(self, named_file_contents: NamedFileContents) -> None:
        extension = PureWindowsPath(named_file_contents.original_file_name).suffix
        if extension == ".csv":
            self.header, self.data = self._parse_csv(named_file_contents.contents)
        elif extension == ".xlsx":
            self.header, self.data = self._parse_xlsx(named_file_contents.contents)
        else:
            msg = f"Unsupported file extension: '{extension}' expected one of 'csv' or 'xlsx'."
            raise AllotropeConversionError(msg)

    def _parse_csv(self, contents: IOType) -> tuple[SeriesData, pd.DataFrame]:
        data = read_csv(contents).replace(np.nan, None)
        assert_not_empty_df(data, "Unable to parse data from empty dataset.")
        # Use the first row in the data block for metadata, since it has all required columns.
        return df_to_series_data(data, index=0), data

    def _parse_xlsx(self, contents: IOType) -> tuple[SeriesData, pd.DataFrame]:
        data = read_excel(contents)
        header, data = split_header_and_data(data, lambda row: row.iloc[0] == "Table")
        data = parse_header_row(data)
        data.columns = data.columns.str.replace("\n", " ")
        return df_to_series_data(parse_header_row(header.T)), data
