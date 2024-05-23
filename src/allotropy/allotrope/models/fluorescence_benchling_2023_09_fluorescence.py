# generated by datamodel-codegen:
#   filename:  fluorescence.json
#   timestamp: 2024-05-23T13:20:48+00:00

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from allotropy.allotrope.models.shared.components.plate_reader import (
    ProcessedDataAggregateDocument,
    SampleDocument,
)
from allotropy.allotrope.models.shared.definitions.custom import (
    TQuantityValueDegreeCelsius,
    TQuantityValueMicroliter,
    TQuantityValueMillimeter,
    TQuantityValueNanometer,
    TQuantityValueNumber,
    TQuantityValuePicogramPerMilliliter,
    TQuantityValueSecondTime,
)
from allotropy.allotrope.models.shared.definitions.definitions import (
    TDatacube,
    TDateTimeValue,
    TStringValue,
)


class ContainerType(Enum):
    reactor = "reactor"
    controlled_lab_reactor = "controlled lab reactor"
    tube = "tube"
    well_plate = "well plate"
    differential_scanning_calorimetry_pan = "differential scanning calorimetry pan"
    qPCR_reaction_block = "qPCR reaction block"
    vial_rack = "vial rack"
    pan = "pan"
    reservoir = "reservoir"
    array_card_block = "array card block"
    capillary = "capillary"
    disintegration_apparatus_basket = "disintegration apparatus basket"
    jar = "jar"
    container = "container"
    tray = "tray"
    basket = "basket"
    cell_holder = "cell holder"


class ScanPositionSettingPlateReader(Enum):
    bottom_scan_position__plate_reader_ = "bottom scan position (plate reader)"
    scan_position_configuration__plate_reader_ = (
        "scan position configuration (plate reader)"
    )
    top_scan_position__plate_reader_ = "top scan position (plate reader)"


@dataclass(kw_only=True)
class DeviceSystemDocument:
    device_identifier: TStringValue
    model_number: TStringValue


@dataclass(kw_only=True)
class DeviceControlDocumentItem:
    device_type: TStringValue | None = None
    shaking_configuration_description: TStringValue | None = None
    detector_distance_setting__plate_reader_: TQuantityValueMillimeter | None = None
    integration_time: TQuantityValueSecondTime | None = None
    number_of_averages: TQuantityValueNumber | None = None
    detector_gain_setting: TStringValue | None = None
    scan_position_setting__plate_reader_: ScanPositionSettingPlateReader | None = None
    detector_carriage_speed_setting: TStringValue | None = None
    detector_wavelength_setting: TQuantityValueNanometer | None = None
    detector_bandwidth_setting: TQuantityValueNanometer | None = None
    excitation_bandwidth_setting: TQuantityValueNanometer | None = None
    excitation_wavelength_setting: TQuantityValueNanometer | None = None
    wavelength_filter_cutoff_setting: TQuantityValueNanometer | None = None
    field_index: int | None = None


@dataclass(kw_only=True)
class DeviceControlAggregateDocument:
    device_control_document: list[DeviceControlDocumentItem] | None = None


@dataclass(kw_only=True)
class MeasurementDocumentItem:
    device_control_aggregate_document: DeviceControlAggregateDocument
    sample_document: SampleDocument
    data_cube: TDatacube | None = None
    compartment_temperature: TQuantityValueDegreeCelsius | None = None
    processed_data_aggregate_document: ProcessedDataAggregateDocument | None = None
    mass_concentration: TQuantityValuePicogramPerMilliliter | None = None


@dataclass(kw_only=True)
class MeasurementAggregateDocument:
    measurement_identifier: TStringValue
    plate_well_count: TQuantityValueNumber
    measurement_document: list[MeasurementDocumentItem]
    measurement_time: TDateTimeValue | None = None
    analyst: TStringValue | None = None
    analytical_method_identifier: TStringValue | None = None
    experimental_data_identifier: TStringValue | None = None
    experiment_type: TStringValue | None = None
    container_type: ContainerType | None = None
    well_volume: TQuantityValueMicroliter | None = None
    device_system_document: DeviceSystemDocument | None = None


@dataclass(kw_only=True)
class Model:
    manifest: str = "http://purl.allotrope.org/manifests/fluorescence/BENCHLING/2023/09/fluorescence.manifest"
    measurement_aggregate_document: MeasurementAggregateDocument | None = None
