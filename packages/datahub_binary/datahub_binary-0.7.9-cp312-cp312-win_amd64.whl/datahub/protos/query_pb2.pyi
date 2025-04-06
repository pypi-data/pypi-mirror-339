import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QryBrokerInstrumentReq(_message.Message):
    __slots__ = ["instrument_id", "market", "msg_sequence", "msg_type", "node_name", "node_type", "page_size", "request_id", "security_id", "start_row", "token"]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    instrument_id: str
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    page_size: int
    request_id: str
    security_id: str
    start_row: int
    token: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., token: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., request_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ...) -> None: ...

class QryBrokerInstrumentRsp(_message.Message):
    __slots__ = ["instrument", "is_last", "msg_sequence", "msg_type", "node_name", "node_type", "page_size", "reason", "request_id", "start_row", "status", "total_row"]
    INSTRUMENT_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ROW_FIELD_NUMBER: _ClassVar[int]
    instrument: _containers.RepeatedCompositeFieldContainer[_common_pb2.Instrument]
    is_last: bool
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    page_size: int
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., instrument: _Optional[_Iterable[_Union[_common_pb2.Instrument, _Mapping]]] = ...) -> None: ...

class QryBrokerOrdersReq(_message.Message):
    __slots__ = ["account_id", "cl_order_id", "instrument_id", "is_active", "msg_sequence", "msg_type", "node_name", "node_type", "order_id", "page_size", "request_id", "start_row", "strategy_id", "token"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    cl_order_id: str
    instrument_id: str
    is_active: int
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order_id: str
    page_size: int
    request_id: str
    start_row: int
    strategy_id: int
    token: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., token: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., request_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., account_id: _Optional[str] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., is_active: _Optional[int] = ...) -> None: ...

class QryBrokerOrdersRsp(_message.Message):
    __slots__ = ["is_last", "msg_sequence", "msg_type", "node_name", "node_type", "order", "page_size", "reason", "request_id", "start_row", "status", "total_row"]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ROW_FIELD_NUMBER: _ClassVar[int]
    is_last: bool
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order: _containers.RepeatedCompositeFieldContainer[_common_pb2.Order]
    page_size: int
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., order: _Optional[_Iterable[_Union[_common_pb2.Order, _Mapping]]] = ...) -> None: ...

class QryBrokerTradesReq(_message.Message):
    __slots__ = ["account_id", "cl_order_id", "instrument_id", "msg_sequence", "msg_type", "node_name", "node_type", "order_id", "page_size", "request_id", "start_row", "strategy_id", "token"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    cl_order_id: str
    instrument_id: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order_id: str
    page_size: int
    request_id: str
    start_row: int
    strategy_id: int
    token: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., token: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., request_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., account_id: _Optional[str] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ...) -> None: ...

class QryBrokerTradesRsp(_message.Message):
    __slots__ = ["is_last", "msg_sequence", "msg_type", "node_name", "node_type", "page_size", "reason", "request_id", "start_row", "status", "total_row", "trade"]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ROW_FIELD_NUMBER: _ClassVar[int]
    TRADE_FIELD_NUMBER: _ClassVar[int]
    is_last: bool
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    page_size: int
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    trade: _containers.RepeatedCompositeFieldContainer[_common_pb2.Trade]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., trade: _Optional[_Iterable[_Union[_common_pb2.Trade, _Mapping]]] = ...) -> None: ...

class QryOrdersReq(_message.Message):
    __slots__ = ["account_id", "cl_order_id", "instrument_id", "is_active", "msg_sequence", "msg_type", "node_name", "node_type", "order_id", "owner_type", "page_size", "request_id", "start_row", "strategy_id", "token"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    cl_order_id: str
    instrument_id: str
    is_active: int
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order_id: str
    owner_type: int
    page_size: int
    request_id: str
    start_row: int
    strategy_id: int
    token: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., token: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., request_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., account_id: _Optional[str] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., is_active: _Optional[int] = ..., owner_type: _Optional[int] = ...) -> None: ...

class QryOrdersRsp(_message.Message):
    __slots__ = ["is_last", "msg_sequence", "msg_type", "node_name", "node_type", "order", "page_size", "reason", "request_id", "start_row", "status", "total_row"]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ROW_FIELD_NUMBER: _ClassVar[int]
    is_last: bool
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order: _containers.RepeatedCompositeFieldContainer[_common_pb2.Order]
    page_size: int
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., order: _Optional[_Iterable[_Union[_common_pb2.Order, _Mapping]]] = ...) -> None: ...

class QryTradesReq(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "instrument_id", "is_active", "market", "msg_sequence", "msg_type", "node_name", "node_type", "order_id", "page_size", "request_id", "security_id", "start_row", "strategy_id", "strategy_name", "token"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    appl_id: str
    cl_order_id: str
    instrument_id: str
    is_active: int
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order_id: str
    page_size: int
    request_id: str
    security_id: str
    start_row: int
    strategy_id: int
    strategy_name: str
    token: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., token: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., request_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., is_active: _Optional[int] = ...) -> None: ...

class QryTradesRsp(_message.Message):
    __slots__ = ["is_last", "msg_sequence", "msg_type", "node_name", "node_type", "page_size", "reason", "request_id", "start_row", "status", "total_row", "trade"]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ROW_FIELD_NUMBER: _ClassVar[int]
    TRADE_FIELD_NUMBER: _ClassVar[int]
    is_last: bool
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    page_size: int
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    trade: _containers.RepeatedCompositeFieldContainer[_common_pb2.Trade]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., trade: _Optional[_Iterable[_Union[_common_pb2.Trade, _Mapping]]] = ...) -> None: ...
