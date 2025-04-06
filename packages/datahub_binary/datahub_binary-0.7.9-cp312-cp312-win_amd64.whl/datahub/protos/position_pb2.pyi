import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
kCash: PosAccountType
kDelta: PosReqType
kFullQuery: PosReqType
kInit: PosReqType
kPosTypeApplyAvl: PosType
kPosTypeBuyIn: PosType
kPosTypeBuyinNodeal: PosType
kPosTypeEod: PosType
kPosTypeFrozen: PosType
kPosTypeIntraday: PosType
kPosTypeSellOut: PosType
kPosTypeSod: PosType
kPosTypeTransAvl: PosType
kPosTypeTransIn: PosType
kPosTypeTransOut: PosType
kPosTypeUndefined: PosType
kQuery: PosReqType
kReplace: PosReqType
kSec: PosAccountType
kTransIn: PosReqType
kTransOut: PosReqType

class FundQty(_message.Message):
    __slots__ = ["qty", "type"]
    QTY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    qty: float
    type: PosType
    def __init__(self, type: _Optional[_Union[PosType, str]] = ..., qty: _Optional[float] = ...) -> None: ...

class FundReport(_message.Message):
    __slots__ = ["account_id", "available", "balance", "currency_id", "fund_qty", "investor_id", "is_last", "is_support_trans", "msg_sequence", "msg_type", "node_name", "node_type", "pos_req_type", "report_id", "request_id", "status", "text", "version"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
    FUND_QTY_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    IS_SUPPORT_TRANS_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    POS_REQ_TYPE_FIELD_NUMBER: _ClassVar[int]
    REPORT_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    available: float
    balance: float
    currency_id: str
    fund_qty: _containers.RepeatedCompositeFieldContainer[FundQty]
    investor_id: str
    is_last: bool
    is_support_trans: bool
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    pos_req_type: PosReqType
    report_id: str
    request_id: str
    status: int
    text: str
    version: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., pos_req_type: _Optional[_Union[PosReqType, str]] = ..., report_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., is_last: bool = ..., version: _Optional[int] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., balance: _Optional[float] = ..., available: _Optional[float] = ..., currency_id: _Optional[str] = ..., is_support_trans: bool = ..., fund_qty: _Optional[_Iterable[_Union[FundQty, _Mapping]]] = ...) -> None: ...

class PosiEvent(_message.Message):
    __slots__ = ["msg_sequence", "msg_type", "node_name", "node_type", "position"]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    position: _common_pb2.Position
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., position: _Optional[_Union[_common_pb2.Position, _Mapping]] = ...) -> None: ...

class PositionQty(_message.Message):
    __slots__ = ["qty", "type"]
    QTY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    qty: int
    type: PosType
    def __init__(self, type: _Optional[_Union[PosType, str]] = ..., qty: _Optional[int] = ...) -> None: ...

class PositionReport(_message.Message):
    __slots__ = ["account_id", "available", "balance", "cost_amt", "cost_price", "instrument_id", "investor_id", "is_last", "is_support_trans", "market", "msg_sequence", "msg_type", "node_name", "node_type", "pos_account_type", "pos_qty", "pos_req_type", "pos_rpt_id", "posi_side", "realized_pnl", "request_id", "security_id", "security_type", "status", "symbol", "text", "version"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    COST_AMT_FIELD_NUMBER: _ClassVar[int]
    COST_PRICE_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    IS_SUPPORT_TRANS_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSI_SIDE_FIELD_NUMBER: _ClassVar[int]
    POS_ACCOUNT_TYPE_FIELD_NUMBER: _ClassVar[int]
    POS_QTY_FIELD_NUMBER: _ClassVar[int]
    POS_REQ_TYPE_FIELD_NUMBER: _ClassVar[int]
    POS_RPT_ID_FIELD_NUMBER: _ClassVar[int]
    REALIZED_PNL_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    available: int
    balance: int
    cost_amt: float
    cost_price: float
    instrument_id: str
    investor_id: str
    is_last: bool
    is_support_trans: bool
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    pos_account_type: PosAccountType
    pos_qty: _containers.RepeatedCompositeFieldContainer[PositionQty]
    pos_req_type: PosReqType
    pos_rpt_id: str
    posi_side: int
    realized_pnl: float
    request_id: str
    security_id: str
    security_type: str
    status: int
    symbol: str
    text: str
    version: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., pos_req_type: _Optional[_Union[PosReqType, str]] = ..., pos_account_type: _Optional[_Union[PosAccountType, str]] = ..., pos_rpt_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., is_last: bool = ..., version: _Optional[int] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., market: _Optional[str] = ..., security_id: _Optional[str] = ..., balance: _Optional[int] = ..., available: _Optional[int] = ..., cost_price: _Optional[float] = ..., realized_pnl: _Optional[float] = ..., cost_amt: _Optional[float] = ..., symbol: _Optional[str] = ..., security_type: _Optional[str] = ..., posi_side: _Optional[int] = ..., instrument_id: _Optional[str] = ..., is_support_trans: bool = ..., pos_qty: _Optional[_Iterable[_Union[PositionQty, _Mapping]]] = ...) -> None: ...

class QryBrokerFundReq(_message.Message):
    __slots__ = ["account_id", "msg_type", "node_name", "node_type", "page_size", "request_id", "start_row", "token"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    msg_type: int
    node_name: str
    node_type: int
    page_size: int
    request_id: str
    start_row: int
    token: str
    def __init__(self, msg_type: _Optional[int] = ..., node_type: _Optional[int] = ..., node_name: _Optional[str] = ..., account_id: _Optional[str] = ..., request_id: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...

class QryBrokerFundRsp(_message.Message):
    __slots__ = ["fund", "is_last", "msg_sequence", "msg_type", "node_name", "node_type", "page_size", "reason", "request_id", "start_row", "status", "total_row"]
    FUND_FIELD_NUMBER: _ClassVar[int]
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
    fund: _containers.RepeatedCompositeFieldContainer[_common_pb2.Fund]
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
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., fund: _Optional[_Iterable[_Union[_common_pb2.Fund, _Mapping]]] = ...) -> None: ...

class QryBrokerPosiReq(_message.Message):
    __slots__ = ["account_id", "market", "msg_type", "node_name", "node_type", "page_size", "query_index", "request_id", "security_id", "start_row", "token"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    QUERY_INDEX_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    market: str
    msg_type: int
    node_name: str
    node_type: int
    page_size: int
    query_index: str
    request_id: str
    security_id: str
    start_row: int
    token: str
    def __init__(self, msg_type: _Optional[int] = ..., node_type: _Optional[int] = ..., node_name: _Optional[str] = ..., request_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., account_id: _Optional[str] = ..., token: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., query_index: _Optional[str] = ...) -> None: ...

class QryBrokerPosiRsp(_message.Message):
    __slots__ = ["is_last", "msg_sequence", "msg_type", "node_name", "node_type", "page_size", "position", "reason", "request_id", "start_row", "status", "total_row"]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
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
    page_size: int
    position: _containers.RepeatedCompositeFieldContainer[_common_pb2.Position]
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., position: _Optional[_Iterable[_Union[_common_pb2.Position, _Mapping]]] = ...) -> None: ...

class QryFundReq(_message.Message):
    __slots__ = ["account_id", "msg_type", "node_name", "node_type", "page_size", "request_id", "start_row", "token"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    msg_type: int
    node_name: str
    node_type: int
    page_size: int
    request_id: str
    start_row: int
    token: str
    def __init__(self, msg_type: _Optional[int] = ..., node_type: _Optional[int] = ..., node_name: _Optional[str] = ..., account_id: _Optional[str] = ..., request_id: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., token: _Optional[str] = ...) -> None: ...

class QryFundRsp(_message.Message):
    __slots__ = ["fund", "is_last", "msg_sequence", "msg_type", "node_name", "node_type", "page_size", "reason", "request_id", "start_row", "status", "total_row"]
    FUND_FIELD_NUMBER: _ClassVar[int]
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
    fund: _containers.RepeatedCompositeFieldContainer[_common_pb2.Fund]
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
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., fund: _Optional[_Iterable[_Union[_common_pb2.Fund, _Mapping]]] = ...) -> None: ...

class QryPosiReq(_message.Message):
    __slots__ = ["account_id", "market", "msg_type", "node_name", "node_type", "page_size", "request_id", "security_id", "start_row", "token"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    market: str
    msg_type: int
    node_name: str
    node_type: int
    page_size: int
    request_id: str
    security_id: str
    start_row: int
    token: str
    def __init__(self, msg_type: _Optional[int] = ..., node_type: _Optional[int] = ..., node_name: _Optional[str] = ..., request_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., account_id: _Optional[str] = ..., token: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class QryPosiRsp(_message.Message):
    __slots__ = ["is_last", "msg_sequence", "msg_type", "node_name", "node_type", "page_size", "position", "reason", "request_id", "start_row", "status", "total_row"]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
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
    page_size: int
    position: _containers.RepeatedCompositeFieldContainer[_common_pb2.Position]
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., position: _Optional[_Iterable[_Union[_common_pb2.Position, _Mapping]]] = ...) -> None: ...

class RequestForPosition(_message.Message):
    __slots__ = ["account_id", "investor_id", "market", "msg_type", "node_name", "pos_qty", "pos_req_type", "posi_side", "request_id", "security_id", "version"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    POSI_SIDE_FIELD_NUMBER: _ClassVar[int]
    POS_QTY_FIELD_NUMBER: _ClassVar[int]
    POS_REQ_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    investor_id: str
    market: str
    msg_type: int
    node_name: str
    pos_qty: _containers.RepeatedCompositeFieldContainer[PositionQty]
    pos_req_type: PosReqType
    posi_side: int
    request_id: str
    security_id: str
    version: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., pos_req_type: _Optional[_Union[PosReqType, str]] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., node_name: _Optional[str] = ..., version: _Optional[int] = ..., market: _Optional[str] = ..., security_id: _Optional[str] = ..., posi_side: _Optional[int] = ..., pos_qty: _Optional[_Iterable[_Union[PositionQty, _Mapping]]] = ...) -> None: ...

class PosType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class PosReqType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class PosAccountType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
