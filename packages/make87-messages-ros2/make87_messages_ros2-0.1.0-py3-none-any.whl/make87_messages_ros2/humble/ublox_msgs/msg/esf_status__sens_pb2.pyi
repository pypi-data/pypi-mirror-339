from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsfSTATUS_Sens(_message.Message):
    __slots__ = ("header", "sensStatus1", "sensStatus2", "freq", "faults")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SENSSTATUS1_FIELD_NUMBER: _ClassVar[int]
    SENSSTATUS2_FIELD_NUMBER: _ClassVar[int]
    FREQ_FIELD_NUMBER: _ClassVar[int]
    FAULTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sensStatus1: int
    sensStatus2: int
    freq: int
    faults: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sensStatus1: _Optional[int] = ..., sensStatus2: _Optional[int] = ..., freq: _Optional[int] = ..., faults: _Optional[int] = ...) -> None: ...
