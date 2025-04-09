from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BatteryState(_message.Message):
    __slots__ = ("timestamp", "voltage", "current_amps", "temperature_celsius", "state_of_charge_percentage", "is_charging")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_AMPS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_CELSIUS_FIELD_NUMBER: _ClassVar[int]
    STATE_OF_CHARGE_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    IS_CHARGING_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    voltage: float
    current_amps: float
    temperature_celsius: float
    state_of_charge_percentage: float
    is_charging: bool
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., voltage: _Optional[float] = ..., current_amps: _Optional[float] = ..., temperature_celsius: _Optional[float] = ..., state_of_charge_percentage: _Optional[float] = ..., is_charging: bool = ...) -> None: ...

class BatteryInformation(_message.Message):
    __slots__ = ("timestamp", "capacity_ah", "voltage_nominal", "voltage_min", "voltage_max", "current_max_amps", "battery_type", "serial_number", "manufacturer")
    class BatteryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[BatteryInformation.BatteryType]
        LIPO: _ClassVar[BatteryInformation.BatteryType]
        LIION: _ClassVar[BatteryInformation.BatteryType]
        NIMH: _ClassVar[BatteryInformation.BatteryType]
        PB: _ClassVar[BatteryInformation.BatteryType]
    UNKNOWN: BatteryInformation.BatteryType
    LIPO: BatteryInformation.BatteryType
    LIION: BatteryInformation.BatteryType
    NIMH: BatteryInformation.BatteryType
    PB: BatteryInformation.BatteryType
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_AH_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_NOMINAL_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_MIN_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_MAX_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MAX_AMPS_FIELD_NUMBER: _ClassVar[int]
    BATTERY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    capacity_ah: float
    voltage_nominal: float
    voltage_min: float
    voltage_max: float
    current_max_amps: float
    battery_type: BatteryInformation.BatteryType
    serial_number: str
    manufacturer: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., capacity_ah: _Optional[float] = ..., voltage_nominal: _Optional[float] = ..., voltage_min: _Optional[float] = ..., voltage_max: _Optional[float] = ..., current_max_amps: _Optional[float] = ..., battery_type: _Optional[_Union[BatteryInformation.BatteryType, str]] = ..., serial_number: _Optional[str] = ..., manufacturer: _Optional[str] = ...) -> None: ...
