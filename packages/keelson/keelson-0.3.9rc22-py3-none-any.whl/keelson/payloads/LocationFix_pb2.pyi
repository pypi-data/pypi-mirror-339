from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LocationFix(_message.Message):
    __slots__ = ("timestamp", "frame_id", "latitude", "longitude", "altitude", "position_covariance", "position_covariance_type")
    class PositionCovarianceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[LocationFix.PositionCovarianceType]
        APPROXIMATED: _ClassVar[LocationFix.PositionCovarianceType]
        DIAGONAL_KNOWN: _ClassVar[LocationFix.PositionCovarianceType]
        KNOWN: _ClassVar[LocationFix.PositionCovarianceType]
    UNKNOWN: LocationFix.PositionCovarianceType
    APPROXIMATED: LocationFix.PositionCovarianceType
    DIAGONAL_KNOWN: LocationFix.PositionCovarianceType
    KNOWN: LocationFix.PositionCovarianceType
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    POSITION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    POSITION_COVARIANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    frame_id: str
    latitude: float
    longitude: float
    altitude: float
    position_covariance: _containers.RepeatedScalarFieldContainer[float]
    position_covariance_type: LocationFix.PositionCovarianceType
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., frame_id: _Optional[str] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., position_covariance: _Optional[_Iterable[float]] = ..., position_covariance_type: _Optional[_Union[LocationFix.PositionCovarianceType, str]] = ...) -> None: ...

class PositionFix(_message.Message):
    __slots__ = ("timestamp", "latitude_degrees", "longitude_degrees", "altitude_meters", "horizontal_accuracy_meters", "vertical_accuracy_meters", "accuracy_meters", "geodetic_datum")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_DEGREES_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_DEGREES_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_METERS_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_ACCURACY_METERS_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_ACCURACY_METERS_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_METERS_FIELD_NUMBER: _ClassVar[int]
    GEODETIC_DATUM_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    latitude_degrees: float
    longitude_degrees: float
    altitude_meters: float
    horizontal_accuracy_meters: float
    vertical_accuracy_meters: float
    accuracy_meters: float
    geodetic_datum: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., latitude_degrees: _Optional[float] = ..., longitude_degrees: _Optional[float] = ..., altitude_meters: _Optional[float] = ..., horizontal_accuracy_meters: _Optional[float] = ..., vertical_accuracy_meters: _Optional[float] = ..., accuracy_meters: _Optional[float] = ..., geodetic_datum: _Optional[str] = ...) -> None: ...

class PositionSourceSatellites(_message.Message):
    __slots__ = ("timestamp", "source", "correction_source", "satellites_used", "hdop", "vdop", "pdop")
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[PositionSourceSatellites.Source]
        GPS: _ClassVar[PositionSourceSatellites.Source]
        GLONASS: _ClassVar[PositionSourceSatellites.Source]
        GALILEO: _ClassVar[PositionSourceSatellites.Source]
        BEIDOU: _ClassVar[PositionSourceSatellites.Source]
        SBAS: _ClassVar[PositionSourceSatellites.Source]
        QZSS: _ClassVar[PositionSourceSatellites.Source]
        IRNSS: _ClassVar[PositionSourceSatellites.Source]
        NAVIC: _ClassVar[PositionSourceSatellites.Source]
        OTHER: _ClassVar[PositionSourceSatellites.Source]
    UNKNOWN: PositionSourceSatellites.Source
    GPS: PositionSourceSatellites.Source
    GLONASS: PositionSourceSatellites.Source
    GALILEO: PositionSourceSatellites.Source
    BEIDOU: PositionSourceSatellites.Source
    SBAS: PositionSourceSatellites.Source
    QZSS: PositionSourceSatellites.Source
    IRNSS: PositionSourceSatellites.Source
    NAVIC: PositionSourceSatellites.Source
    OTHER: PositionSourceSatellites.Source
    class CorrectionSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NONE: _ClassVar[PositionSourceSatellites.CorrectionSource]
        DGPS: _ClassVar[PositionSourceSatellites.CorrectionSource]
        RTK: _ClassVar[PositionSourceSatellites.CorrectionSource]
    NONE: PositionSourceSatellites.CorrectionSource
    DGPS: PositionSourceSatellites.CorrectionSource
    RTK: PositionSourceSatellites.CorrectionSource
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    CORRECTION_SOURCE_FIELD_NUMBER: _ClassVar[int]
    SATELLITES_USED_FIELD_NUMBER: _ClassVar[int]
    HDOP_FIELD_NUMBER: _ClassVar[int]
    VDOP_FIELD_NUMBER: _ClassVar[int]
    PDOP_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    source: _containers.RepeatedScalarFieldContainer[PositionSourceSatellites.Source]
    correction_source: PositionSourceSatellites.CorrectionSource
    satellites_used: int
    hdop: float
    vdop: float
    pdop: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., source: _Optional[_Iterable[_Union[PositionSourceSatellites.Source, str]]] = ..., correction_source: _Optional[_Union[PositionSourceSatellites.CorrectionSource, str]] = ..., satellites_used: _Optional[int] = ..., hdop: _Optional[float] = ..., vdop: _Optional[float] = ..., pdop: _Optional[float] = ...) -> None: ...

class TraveledDistance(_message.Message):
    __slots__ = ("timestamp", "distance_meters")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_METERS_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    distance_meters: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., distance_meters: _Optional[float] = ...) -> None: ...
