from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OUTPUT: _ClassVar[DataType]
    VIEW: _ClassVar[DataType]
    LOGS: _ClassVar[DataType]
    OTHER: _ClassVar[DataType]
OUTPUT: DataType
VIEW: DataType
LOGS: DataType
OTHER: DataType

class StorageRecord(_message.Message):
    __slots__ = ("data", "mission_id", "name", "creation_date", "update_date", "data_type")
    DATA_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATION_DATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DATE_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    data: _struct_pb2.Struct
    mission_id: str
    name: str
    creation_date: _timestamp_pb2.Timestamp
    update_date: _timestamp_pb2.Timestamp
    data_type: DataType
    def __init__(self, data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., mission_id: _Optional[str] = ..., name: _Optional[str] = ..., creation_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., data_type: _Optional[_Union[DataType, str]] = ...) -> None: ...

class StoreRecordRequest(_message.Message):
    __slots__ = ("data", "mission_id", "name", "data_type")
    DATA_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    data: _struct_pb2.Struct
    mission_id: str
    name: str
    data_type: DataType
    def __init__(self, data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., mission_id: _Optional[str] = ..., name: _Optional[str] = ..., data_type: _Optional[_Union[DataType, str]] = ...) -> None: ...

class StoreRecordResponse(_message.Message):
    __slots__ = ("success", "stored_data")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STORED_DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    stored_data: StorageRecord
    def __init__(self, success: bool = ..., stored_data: _Optional[_Union[StorageRecord, _Mapping]] = ...) -> None: ...

class ReadRecordRequest(_message.Message):
    __slots__ = ("mission_id", "name")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    name: str
    def __init__(self, mission_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ReadRecordResponse(_message.Message):
    __slots__ = ("success", "stored_data")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STORED_DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    stored_data: StorageRecord
    def __init__(self, success: bool = ..., stored_data: _Optional[_Union[StorageRecord, _Mapping]] = ...) -> None: ...

class ModifyRecordRequest(_message.Message):
    __slots__ = ("data", "mission_id", "name")
    DATA_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    data: _struct_pb2.Struct
    mission_id: str
    name: str
    def __init__(self, data: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., mission_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ModifyRecordResponse(_message.Message):
    __slots__ = ("success", "stored_data")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STORED_DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    stored_data: StorageRecord
    def __init__(self, success: bool = ..., stored_data: _Optional[_Union[StorageRecord, _Mapping]] = ...) -> None: ...

class RemoveRecordRequest(_message.Message):
    __slots__ = ("mission_id", "name")
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    mission_id: str
    name: str
    def __init__(self, mission_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class RemoveRecordResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
