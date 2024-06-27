""" Parser file for Roche Cedex HiRes Instrument """
from __future__ import annotations

from decimal import Decimal
from typing import Any

import numpy as np
import pandas as pd

from allotropy.allotrope.converter import add_custom_information_document
from allotropy.allotrope.models.adm.cell_counting.benchling._2023._11.cell_counting import (
    CellCountingAggregateDocument,
    CellCountingDetectorDeviceControlAggregateDocument,
    CellCountingDetectorMeasurementDocumentItem,
    CellCountingDocumentItem,
    DataProcessingDocument,
    DataSystemDocument,
    DeviceControlDocumentItemModel,
    DeviceSystemDocument,
    MeasurementAggregateDocument,
    Model,
    ProcessedDataAggregateDocument1,
    ProcessedDataDocumentItem,
    SampleDocument,
)
from allotropy.allotrope.models.shared.definitions.custom import (
    TQuantityValueCell,
    TQuantityValueMicroliter,
    TQuantityValueMicrometer,
    TQuantityValueMillionCellsPerMilliliter,
    TQuantityValuePercent,
    TQuantityValueUnitless,
)
from allotropy.constants import ASM_CONVERTER_NAME, ASM_CONVERTER_VERSION
from allotropy.exceptions import AllotropeConversionError
from allotropy.named_file_contents import NamedFileContents
from allotropy.parsers.release_state import ReleaseState
from allotropy.parsers.roche_cedex_hires import constants
from allotropy.parsers.roche_cedex_hires.roche_cedex_hires_reader import (
    RocheCedexHiResReader,
)
from allotropy.parsers.utils.uuids import random_uuid_str
from allotropy.parsers.vendor_parser import VendorParser


def get_value(data_frame: pd.DataFrame, column: str, row: int) -> Any | None:
    if column not in data_frame.columns:
        return None
    value = data_frame[column][row]

    if isinstance(value, np.int64):
        return int(value)
    elif isinstance(value, np.float64):
        return float(value)
    return value


def get_value_not_none(dataframe: pd.DataFrame, column: str, row: int) -> Any:
    value = get_value(dataframe, column, row)
    if value is None or value == np.nan:
        msg = f"Unable to find value for column '{column}'."
        raise AllotropeConversionError(msg)
    return value


class RocheCedexHiResParser(VendorParser):
    @property
    def display_name(self) -> str:
        return "Roche Cedex HiRes"

    @property
    def release_state(self) -> ReleaseState:
        return ReleaseState.WORKING_DRAFT

    def to_allotrope(self, named_file_contents: NamedFileContents) -> Model:
        return self._get_model(
            data=RocheCedexHiResReader.read(named_file_contents),
            filename=named_file_contents.original_file_name,
        )

    def _get_model(self, data: pd.DataFrame, filename: str) -> Model:
        return Model(
            field_asm_manifest="http://purl.allotrope.org/manifests/cell-counting/BENCHLING/2023/11/cell-counting.manifest",
            cell_counting_aggregate_document=CellCountingAggregateDocument(
                device_system_document=self._get_device_system_document(data),
                data_system_document=DataSystemDocument(
                    file_name=filename,
                    software_name=constants.CEDEX_SOFTWARE,
                    ASM_converter_name=ASM_CONVERTER_NAME,
                    ASM_converter_version=ASM_CONVERTER_VERSION,
                ),
                cell_counting_document=self._get_cell_counting_document(data),
            ),
        )

    def _get_device_system_document(self, data: pd.DataFrame) -> DeviceSystemDocument:
        return DeviceSystemDocument(
            model_number=constants.MODEL_NUMBER,
            product_manufacturer=constants.PRODUCT_MANUFACTURER,
            asset_management_identifier=self._get_system_value(data, "System name"),
            description=self._get_system_value(data, "System description"),
            device_identifier=str(self._get_system_value(data, "Cedex ID")),
        )

    def _get_system_value(self, data: pd.DataFrame, column_name: str):
        if len(set(data[column_name])) != 1:
            raise AllotropeConversionError(
                constants.MULTIPLE_SYSTEM_ERROR + column_name
            )
        else:
            return next(iter(set(data[column_name])))

    def _get_cell_counting_document(
        self, data: pd.DataFrame
    ) -> list[CellCountingDocumentItem]:
        return [
            self._get_cell_counting_document_item(data, i)
            for i in range(len(data.index))
        ]

    def _get_cell_counting_document_item(
        self, data: pd.DataFrame, row: int
    ) -> CellCountingDocumentItem:
        sample_custom_document = {
            "group identifier": get_value(data, "Data set name", row),
            "sampling time": self._get_date_time(
                str(get_value(data, "Sample draw Time", row))
            ),
        }
        processed_data_custom_document = {
            "average compactness": {
                "value": get_value(data, "Avg Compactness", row),
                "unit": "(unitless)",
            },
            "average area": {
                "value": get_value(data, "Avg Area", row),
                "unit": "(unitless)",
            },
            "average perimeter": {
                "value": get_value(data, "Avg Perimeter", row),
                "unit": "μm",
            },
            "average segment area": {
                "value": get_value(data, "Avg Segm. Area", row),
                "unit": "(unitless)",
            },
            "total object count": {
                "value": get_value(data, "Total Object Count", row),
                "unit": "cell",
            },
            "standard deviation": {
                "value": get_value(data, "Std Dev.", row),
                "unit": "cell",
            },
            "aggregate rate": {
                "value": get_value(data, "Aggregate Rate", row),
                "unit": "%",
            },
        }
        return CellCountingDocumentItem(
            analyst=get_value(data, "Username", row),
            measurement_aggregate_document=MeasurementAggregateDocument(
                measurement_document=[
                    CellCountingDetectorMeasurementDocumentItem(
                        measurement_time=self._get_date_time(
                            str(get_value_not_none(data, "Date finished", row))
                        ),
                        measurement_identifier=random_uuid_str(),
                        sample_document=add_custom_information_document(
                            SampleDocument(
                                sample_identifier=get_value_not_none(
                                    data, "Sample identifer", row
                                ),
                                batch_identifier=get_value(
                                    data, "Reactor identifer", row
                                ),
                            ),
                            sample_custom_document,
                        ),
                        device_control_aggregate_document=CellCountingDetectorDeviceControlAggregateDocument(
                            device_control_document=[
                                DeviceControlDocumentItemModel(
                                    device_type=constants.DEVICE_TYPE,
                                    sample_volume_setting=TQuantityValueMicroliter(
                                        value=get_value(data, "Sample volume", row)
                                    ),
                                )
                            ]
                        ),
                        processed_data_aggregate_document=add_custom_information_document(
                            ProcessedDataAggregateDocument1(
                                processed_data_document=[
                                    ProcessedDataDocumentItem(
                                        data_processing_document=DataProcessingDocument(
                                            cell_type_processing_method=get_value(
                                                data, "Cell type name", row
                                            ),
                                            cell_density_dilution_factor=TQuantityValueUnitless(
                                                value=get_value(data, "Dilution", row)
                                            ),
                                        ),
                                        viability__cell_counter_=TQuantityValuePercent(
                                            value=get_value_not_none(
                                                data, "Viability", row
                                            )
                                        ),
                                        viable_cell_density__cell_counter_=TQuantityValueMillionCellsPerMilliliter(
                                            value=float(
                                                Decimal(
                                                    str(
                                                        get_value_not_none(
                                                            data,
                                                            "Viable Cell Conc.",
                                                            row,
                                                        )
                                                    )
                                                )
                                                / Decimal("1000000")
                                            )
                                        ),
                                        total_cell_density__cell_counter_=TQuantityValueMillionCellsPerMilliliter(
                                            value=float(
                                                Decimal(
                                                    str(
                                                        get_value(
                                                            data,
                                                            "Total Cell Conc.",
                                                            row,
                                                        )
                                                    )
                                                )
                                                / Decimal("1000000")
                                            )
                                        ),
                                        dead_cell_density__cell_counter_=TQuantityValueMillionCellsPerMilliliter(
                                            value=float(
                                                Decimal(
                                                    str(
                                                        get_value(
                                                            data, "Dead Cell Conc.", row
                                                        )
                                                    )
                                                )
                                                / Decimal("1000000")
                                            )
                                        ),
                                        total_cell_count=TQuantityValueCell(
                                            value=get_value(
                                                data, "Total Cell Count", row
                                            )
                                        ),
                                        viable_cell_count=TQuantityValueCell(
                                            value=get_value(
                                                data, "Viable Cell Count", row
                                            )
                                        ),
                                        dead_cell_count=TQuantityValueCell(
                                            value=get_value(
                                                data, "Dead Cell Count", row
                                            )
                                        ),
                                        average_live_cell_diameter__cell_counter_=TQuantityValueMicrometer(
                                            value=get_value(data, "Avg Diameter", row)
                                        ),
                                    )
                                ]
                            ),
                            processed_data_custom_document,
                        ),
                    )
                ],
            ),
        )
