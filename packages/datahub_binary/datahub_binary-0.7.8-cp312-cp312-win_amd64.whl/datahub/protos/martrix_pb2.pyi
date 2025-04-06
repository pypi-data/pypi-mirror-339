from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FinancialMatrix(_message.Message):
    __slots__ = ["cols", "data_matrix", "instrument_ids", "last_timestamp", "msg_sequence", "msg_type", "trade_time"]
    COLS_FIELD_NUMBER: _ClassVar[int]
    DATA_MATRIX_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRADE_TIME_FIELD_NUMBER: _ClassVar[int]
    cols: _containers.RepeatedScalarFieldContainer[str]
    data_matrix: _containers.RepeatedScalarFieldContainer[int]
    instrument_ids: _containers.RepeatedScalarFieldContainer[str]
    last_timestamp: int
    msg_sequence: int
    msg_type: int
    trade_time: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., trade_time: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., instrument_ids: _Optional[_Iterable[str]] = ..., cols: _Optional[_Iterable[str]] = ..., data_matrix: _Optional[_Iterable[int]] = ...) -> None: ...
