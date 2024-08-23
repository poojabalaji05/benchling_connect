from io import StringIO

import pandas as pd

from allotropy.exceptions import AllotropeConversionError
from allotropy.named_file_contents import NamedFileContents
from allotropy.parsers.lines_reader import LinesReader, read_to_lines
from allotropy.parsers.thermo_fisher_genesys30 import constants
from allotropy.parsers.utils.pandas import df_to_series_data, read_csv, SeriesData


class ThermoFisherGenesys30Reader:
    header: SeriesData
    data: pd.DataFrame

    def __init__(self, named_file_contents: NamedFileContents) -> None:
        filename = named_file_contents.original_file_name

        reader = LinesReader(read_to_lines(named_file_contents))

        if filename.endswith(".csv"):
            metadata_list = [line for line in reader.pop_until("^,,") if line]
            reader.drop_until_inclusive(",,")
            delimiter = ","
        elif filename.endswith(".tsv"):
            metadata_list = list(reader.pop_until_empty())
            reader.drop_until_inclusive("")
            delimiter = "\t"
        else:
            message = f"{constants.UNSUPPORTED_FILE_FORMAT_ERROR} {filename}"
            raise AllotropeConversionError(message)

        rawdata_list = list(reader.pop_until_empty())
        rawdata_string = StringIO("\n".join(rawdata_list))
        self.data = read_csv(rawdata_string, header=0, delimiter=delimiter)
        self.data.columns = self.data.columns.astype(str).str.strip()

        metadata_string = StringIO("\n".join(metadata_list))
        metadata_dataframe = (
            read_csv(
                metadata_string,
                header=None,
                delimiter=delimiter,
                keep_default_na=False,
                index_col=0,
            )
            .astype(str)
            .T
        )
        metadata_dataframe.columns = metadata_dataframe.columns.str.strip()
        metadata_dataframe = metadata_dataframe.head(1)

        self.header = df_to_series_data(metadata_dataframe)
