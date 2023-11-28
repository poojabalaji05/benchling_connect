import pytest

from allotropy.parser_factory import Vendor
from allotropy.parsers.perkin_elmer_envision.perkin_elmer_envision_parser import (
    PerkinElmerEnvisionParser,
)
from allotropy.parsers.utils.timestamp_parser import TimestampParser
from tests.parsers.perkin_elmer_envision.perkin_elmer_envision_data import (
    get_data,
    get_model,
)
from tests.parsers.test_utils import from_file, validate_contents, validate_schema

output_files = (
    "PE_Envision_absorbance_example01",
    "PE_Envision_fluorescence_example01",
    "PE_Envision_fluorescence_example02",
    "PE_Envision_fluorescence_example03",
    "PE_Envision_fluorescence_example04",
    "PE_Envision_luminescence_example01",
)

VENDOR_TYPE = Vendor.PERKIN_ELMER_ENVISION


@pytest.mark.parametrize("output_file", output_files)
def test_parse_perkin_elmer_envision_to_asm(output_file: str) -> None:
    test_filepath = f"tests/parsers/perkin_elmer_envision/testdata/{output_file}.csv"
    expected_filepath = (
        f"tests/parsers/perkin_elmer_envision/testdata/{output_file}.json"
    )
    allotrope_dict = from_file(test_filepath, VENDOR_TYPE)
    validate_schema(allotrope_dict, "plate-reader/BENCHLING/2023/09/plate-reader.json")
    validate_contents(allotrope_dict, expected_filepath)


@pytest.mark.short
def test_get_model() -> None:
    parser = PerkinElmerEnvisionParser(TimestampParser())
    model = parser._get_model(get_data(), "file.txt")

    # remove all random UUIDs
    if agg_doc := model.plate_reader_aggregate_document:
        for i in range(len(plate_doc := agg_doc.plate_reader_document)):
            for j in range(
                len(
                    measurement_doc := plate_doc[
                        i
                    ].measurement_aggregate_document.measurement_document
                )
            ):
                measurement_doc[j].measurement_identifier = ""

    assert model == get_model()
