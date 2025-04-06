import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BizInstructions(_message.Message):
    __slots__ = ["instruction", "instruction_id", "instruction_type", "msg_sequence", "msg_type", "node_name", "node_type"]
    INSTRUCTION_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTION_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    instruction: str
    instruction_id: str
    instruction_type: int
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    def __init__(self, msg_type: _Optional[int] = ..., node_type: _Optional[int] = ..., node_name: _Optional[str] = ..., msg_sequence: _Optional[int] = ..., instruction_type: _Optional[int] = ..., instruction_id: _Optional[str] = ..., instruction: _Optional[str] = ...) -> None: ...

class BlankPoint(_message.Message):
    __slots__ = ["msg_sequence", "msg_type", "node_name", "node_type"]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    def __init__(self, msg_type: _Optional[int] = ..., node_type: _Optional[int] = ..., node_name: _Optional[str] = ..., msg_sequence: _Optional[int] = ...) -> None: ...

class Breakpoint(_message.Message):
    __slots__ = ["msg_sequence", "msg_type", "node_name", "node_type"]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    def __init__(self, msg_type: _Optional[int] = ..., node_type: _Optional[int] = ..., node_name: _Optional[str] = ..., msg_sequence: _Optional[int] = ...) -> None: ...

class CancelAllOrder(_message.Message):
    __slots__ = ["account_id", "cl_order_id", "instrument_id", "investor_id", "market", "msg_sequence", "msg_type", "node_name", "node_type", "op_user", "owner_type", "security_id", "strategy_id", "strategy_name"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    cl_order_id: str
    instrument_id: str
    investor_id: str
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    owner_type: int
    security_id: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ..., cl_order_id: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., owner_type: _Optional[int] = ...) -> None: ...

class CancelConfirm(_message.Message):
    __slots__ = ["account_id", "appl_id", "cancel_qty", "cl_order_id", "instrument_id", "investor_id", "market", "msg_sequence", "msg_type", "node_name", "node_type", "original_cl_order_id", "original_counter_order_id", "original_order_id", "reason", "security_id", "strategy_id", "strategy_name", "text"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CANCEL_QTY_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_COUNTER_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    appl_id: str
    cancel_qty: int
    cl_order_id: str
    instrument_id: str
    investor_id: str
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    original_cl_order_id: str
    original_counter_order_id: str
    original_order_id: str
    reason: int
    security_id: str
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., original_order_id: _Optional[str] = ..., original_cl_order_id: _Optional[str] = ..., original_counter_order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., cancel_qty: _Optional[int] = ..., reason: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class CancelOrder(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "instrument_id", "investor_id", "market", "msg_sequence", "msg_type", "node_name", "node_type", "op_user", "original_cl_order_id", "original_order_id", "owner_type", "parent_order_id", "security_id", "strategy_id", "strategy_name"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    appl_id: str
    cl_order_id: str
    instrument_id: str
    investor_id: str
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    original_cl_order_id: str
    original_order_id: str
    owner_type: int
    parent_order_id: str
    security_id: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., cl_order_id: _Optional[str] = ..., original_order_id: _Optional[str] = ..., original_cl_order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., owner_type: _Optional[int] = ..., parent_order_id: _Optional[str] = ...) -> None: ...

class CancelPendingConfirm(_message.Message):
    __slots__ = ["account_id", "appl_id", "cancel_qty", "cl_order_id", "instrument_id", "investor_id", "market", "msg_sequence", "msg_type", "node_name", "node_type", "original_cl_order_id", "original_counter_order_id", "original_order_id", "reason", "security_id", "strategy_id", "strategy_name", "text"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CANCEL_QTY_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_COUNTER_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    appl_id: str
    cancel_qty: int
    cl_order_id: str
    instrument_id: str
    investor_id: str
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    original_cl_order_id: str
    original_counter_order_id: str
    original_order_id: str
    reason: int
    security_id: str
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., original_order_id: _Optional[str] = ..., original_cl_order_id: _Optional[str] = ..., original_counter_order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., cancel_qty: _Optional[int] = ..., reason: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class CancelReject(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "instrument_id", "investor_id", "market", "msg_sequence", "msg_type", "node_name", "node_type", "original_cl_order_id", "original_counter_order_id", "original_order_id", "reject_reason", "security_id", "strategy_id", "strategy_name", "text"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_COUNTER_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    REJECT_REASON_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    appl_id: str
    cl_order_id: str
    instrument_id: str
    investor_id: str
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    original_cl_order_id: str
    original_counter_order_id: str
    original_order_id: str
    reject_reason: int
    security_id: str
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., original_order_id: _Optional[str] = ..., original_cl_order_id: _Optional[str] = ..., original_counter_order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., reject_reason: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class ExternalOrderEvent(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "instrument_id", "investor_id", "market", "msg_sequence", "msg_type", "node_name", "node_type", "order_date", "order_id", "order_price", "order_qty", "order_type", "owner_type", "position_effect", "purpose", "security_id", "security_type", "side", "stop_px", "strategy_id", "time_in_force"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_DATE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_PRICE_FIELD_NUMBER: _ClassVar[int]
    ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSITION_EFFECT_FIELD_NUMBER: _ClassVar[int]
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STOP_PX_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_IN_FORCE_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    appl_id: str
    cl_order_id: str
    instrument_id: str
    investor_id: str
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order_date: int
    order_id: str
    order_price: float
    order_qty: int
    order_type: int
    owner_type: int
    position_effect: int
    purpose: int
    security_id: str
    security_type: str
    side: int
    stop_px: float
    strategy_id: int
    time_in_force: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., order_date: _Optional[int] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., security_type: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., order_type: _Optional[int] = ..., side: _Optional[int] = ..., position_effect: _Optional[int] = ..., time_in_force: _Optional[int] = ..., purpose: _Optional[int] = ..., stop_px: _Optional[float] = ..., order_qty: _Optional[int] = ..., order_price: _Optional[float] = ..., owner_type: _Optional[int] = ...) -> None: ...

class Heartbeat(_message.Message):
    __slots__ = ["is_login", "msg_type", "node_name", "node_type", "request_id", "timestamp"]
    IS_LOGIN_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    is_login: int
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    timestamp: int
    def __init__(self, msg_type: _Optional[int] = ..., node_type: _Optional[int] = ..., node_name: _Optional[str] = ..., timestamp: _Optional[int] = ..., is_login: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class OrderConfirm(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "confirm_qty", "contract_unit", "counter_order_id", "instrument_id", "investor_id", "is_pass", "market", "msg_sequence", "msg_type", "node_name", "node_type", "order_id", "order_price", "position_effect", "reject_qty", "security_id", "strategy_id", "strategy_name"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_QTY_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    COUNTER_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PASS_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_PRICE_FIELD_NUMBER: _ClassVar[int]
    POSITION_EFFECT_FIELD_NUMBER: _ClassVar[int]
    REJECT_QTY_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    appl_id: str
    cl_order_id: str
    confirm_qty: int
    contract_unit: float
    counter_order_id: str
    instrument_id: str
    investor_id: str
    is_pass: int
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order_id: str
    order_price: float
    position_effect: int
    reject_qty: int
    security_id: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., counter_order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., confirm_qty: _Optional[int] = ..., reject_qty: _Optional[int] = ..., is_pass: _Optional[int] = ..., order_price: _Optional[float] = ..., contract_unit: _Optional[float] = ..., position_effect: _Optional[int] = ...) -> None: ...

class OrderEvent(_message.Message):
    __slots__ = ["msg_sequence", "msg_type", "node_name", "node_type", "order"]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order: _common_pb2.Order
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., order: _Optional[_Union[_common_pb2.Order, _Mapping]] = ...) -> None: ...

class OrderPendingConfirm(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "confirm_qty", "contract_unit", "instrument_id", "investor_id", "is_pass", "market", "msg_sequence", "msg_type", "node_name", "node_type", "order_id", "order_price", "position_effect", "reject_qty", "security_id", "strategy_id", "strategy_name"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_QTY_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PASS_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_PRICE_FIELD_NUMBER: _ClassVar[int]
    POSITION_EFFECT_FIELD_NUMBER: _ClassVar[int]
    REJECT_QTY_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    appl_id: str
    cl_order_id: str
    confirm_qty: int
    contract_unit: float
    instrument_id: str
    investor_id: str
    is_pass: int
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order_id: str
    order_price: float
    position_effect: int
    reject_qty: int
    security_id: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., confirm_qty: _Optional[int] = ..., reject_qty: _Optional[int] = ..., is_pass: _Optional[int] = ..., order_price: _Optional[float] = ..., contract_unit: _Optional[float] = ..., position_effect: _Optional[int] = ...) -> None: ...

class OrderReject(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "contract_unit", "exchange_reject_reason", "instrument_id", "investor_id", "is_pass", "market", "msg_sequence", "msg_type", "node_name", "node_type", "order_id", "order_price", "reject_qty", "reject_reason", "security_id", "strategy_id", "strategy_name", "text"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    EXCHANGE_REJECT_REASON_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PASS_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_PRICE_FIELD_NUMBER: _ClassVar[int]
    REJECT_QTY_FIELD_NUMBER: _ClassVar[int]
    REJECT_REASON_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    appl_id: str
    cl_order_id: str
    contract_unit: float
    exchange_reject_reason: int
    instrument_id: str
    investor_id: str
    is_pass: int
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order_id: str
    order_price: float
    reject_qty: int
    reject_reason: int
    security_id: str
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., reject_reason: _Optional[int] = ..., text: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., reject_qty: _Optional[int] = ..., is_pass: _Optional[int] = ..., order_price: _Optional[float] = ..., contract_unit: _Optional[float] = ..., exchange_reject_reason: _Optional[int] = ...) -> None: ...

class PlaceOrder(_message.Message):
    __slots__ = ["account_id", "algo_params", "algo_type", "appl_id", "attachment", "basket_id", "cl_order_id", "instrument_id", "investor_id", "is_pass", "is_pre_order", "market", "msg_sequence", "msg_type", "node_name", "node_type", "op_user", "order_price", "order_qty", "order_source", "order_type", "owner_type", "parent_order_id", "position_effect", "purpose", "security_id", "security_type", "side", "stop_px", "strategy_id", "strategy_name", "time_in_force", "trigger_time", "user_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALGO_PARAMS_FIELD_NUMBER: _ClassVar[int]
    ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    BASKET_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PASS_FIELD_NUMBER: _ClassVar[int]
    IS_PRE_ORDER_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    ORDER_PRICE_FIELD_NUMBER: _ClassVar[int]
    ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    ORDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_EFFECT_FIELD_NUMBER: _ClassVar[int]
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STOP_PX_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TIME_IN_FORCE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_TIME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    algo_params: _common_pb2.AlgoParams
    algo_type: int
    appl_id: str
    attachment: str
    basket_id: str
    cl_order_id: str
    instrument_id: str
    investor_id: str
    is_pass: int
    is_pre_order: int
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    order_price: float
    order_qty: int
    order_source: str
    order_type: int
    owner_type: int
    parent_order_id: str
    position_effect: int
    purpose: int
    security_id: str
    security_type: str
    side: int
    stop_px: float
    strategy_id: int
    strategy_name: str
    time_in_force: int
    trigger_time: int
    user_id: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., market: _Optional[str] = ..., security_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., security_type: _Optional[str] = ..., appl_id: _Optional[str] = ..., user_id: _Optional[str] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., is_pre_order: _Optional[int] = ..., trigger_time: _Optional[int] = ..., order_type: _Optional[int] = ..., side: _Optional[int] = ..., position_effect: _Optional[int] = ..., time_in_force: _Optional[int] = ..., purpose: _Optional[int] = ..., stop_px: _Optional[float] = ..., order_price: _Optional[float] = ..., order_qty: _Optional[int] = ..., is_pass: _Optional[int] = ..., owner_type: _Optional[int] = ..., algo_type: _Optional[int] = ..., algo_params: _Optional[_Union[_common_pb2.AlgoParams, _Mapping]] = ..., order_source: _Optional[str] = ..., attachment: _Optional[str] = ..., parent_order_id: _Optional[str] = ..., basket_id: _Optional[str] = ...) -> None: ...

class RiskEvent(_message.Message):
    __slots__ = ["msg_sequence", "msg_type", "node_name", "node_type", "risk_result", "timestamp"]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RISK_RESULT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    risk_result: _containers.RepeatedCompositeFieldContainer[RiskResult]
    timestamp: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., timestamp: _Optional[int] = ..., risk_result: _Optional[_Iterable[_Union[RiskResult, _Mapping]]] = ...) -> None: ...

class RiskResult(_message.Message):
    __slots__ = ["account_id", "instrument_id", "order_action", "order_id", "real_value", "risk_code", "risk_id", "risk_info", "risk_status", "set_value"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ACTION_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    REAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    RISK_CODE_FIELD_NUMBER: _ClassVar[int]
    RISK_ID_FIELD_NUMBER: _ClassVar[int]
    RISK_INFO_FIELD_NUMBER: _ClassVar[int]
    RISK_STATUS_FIELD_NUMBER: _ClassVar[int]
    SET_VALUE_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    instrument_id: str
    order_action: int
    order_id: str
    real_value: float
    risk_code: str
    risk_id: int
    risk_info: str
    risk_status: int
    set_value: float
    def __init__(self, risk_code: _Optional[str] = ..., risk_info: _Optional[str] = ..., risk_status: _Optional[int] = ..., order_action: _Optional[int] = ..., order_id: _Optional[str] = ..., account_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., risk_id: _Optional[int] = ..., set_value: _Optional[float] = ..., real_value: _Optional[float] = ...) -> None: ...

class TradeConfirm(_message.Message):
    __slots__ = ["account_id", "algo_type", "appl_id", "attachment", "basket_id", "business_type", "cl_order_id", "contract_unit", "counter_cl_order_id", "counter_order_id", "counterparty_id", "instrument_id", "investor_id", "is_maker", "last_px", "last_qty", "market", "match_place", "msg_sequence", "msg_type", "node_name", "node_type", "order_id", "order_price", "order_qty", "order_source", "order_type", "owner_type", "parent_order_id", "position_effect", "security_id", "side", "strategy_id", "strategy_name", "symbol", "trade_amt", "trade_id", "trade_time", "user_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    BASKET_ID_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    COUNTERPARTY_ID_FIELD_NUMBER: _ClassVar[int]
    COUNTER_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    COUNTER_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_MAKER_FIELD_NUMBER: _ClassVar[int]
    LAST_PX_FIELD_NUMBER: _ClassVar[int]
    LAST_QTY_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MATCH_PLACE_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_PRICE_FIELD_NUMBER: _ClassVar[int]
    ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    ORDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_EFFECT_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TRADE_AMT_FIELD_NUMBER: _ClassVar[int]
    TRADE_ID_FIELD_NUMBER: _ClassVar[int]
    TRADE_TIME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    algo_type: int
    appl_id: str
    attachment: str
    basket_id: str
    business_type: str
    cl_order_id: str
    contract_unit: float
    counter_cl_order_id: str
    counter_order_id: str
    counterparty_id: str
    instrument_id: str
    investor_id: str
    is_maker: int
    last_px: float
    last_qty: int
    market: str
    match_place: int
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    order_id: str
    order_price: float
    order_qty: int
    order_source: str
    order_type: int
    owner_type: int
    parent_order_id: str
    position_effect: int
    security_id: str
    side: int
    strategy_id: int
    strategy_name: str
    symbol: str
    trade_amt: float
    trade_id: str
    trade_time: int
    user_id: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., counter_order_id: _Optional[str] = ..., trade_id: _Optional[str] = ..., trade_time: _Optional[int] = ..., last_px: _Optional[float] = ..., last_qty: _Optional[int] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., match_place: _Optional[int] = ..., counterparty_id: _Optional[str] = ..., is_maker: _Optional[int] = ..., side: _Optional[int] = ..., position_effect: _Optional[int] = ..., trade_amt: _Optional[float] = ..., order_qty: _Optional[int] = ..., order_price: _Optional[float] = ..., contract_unit: _Optional[float] = ..., order_type: _Optional[int] = ..., order_source: _Optional[str] = ..., user_id: _Optional[str] = ..., counter_cl_order_id: _Optional[str] = ..., owner_type: _Optional[int] = ..., business_type: _Optional[str] = ..., symbol: _Optional[str] = ..., parent_order_id: _Optional[str] = ..., algo_type: _Optional[int] = ..., attachment: _Optional[str] = ..., basket_id: _Optional[str] = ...) -> None: ...

class UpdateNodeConfigReq(_message.Message):
    __slots__ = ["counter_account", "last_timestamp", "msg_type", "node_name", "node_type", "op_user", "operate_type", "request_id", "trading_session"]
    COUNTER_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TRADING_SESSION_FIELD_NUMBER: _ClassVar[int]
    counter_account: _containers.RepeatedCompositeFieldContainer[_common_pb2.CounterAccount]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    operate_type: str
    request_id: str
    trading_session: _containers.RepeatedCompositeFieldContainer[_common_pb2.TradingSession]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[str] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ..., trading_session: _Optional[_Iterable[_Union[_common_pb2.TradingSession, _Mapping]]] = ..., counter_account: _Optional[_Iterable[_Union[_common_pb2.CounterAccount, _Mapping]]] = ...) -> None: ...

class UpdateNodeConfigRsp(_message.Message):
    __slots__ = ["counter_account", "last_timestamp", "msg_type", "node_name", "node_type", "operate_type", "request_id", "status", "text", "trading_session"]
    COUNTER_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TRADING_SESSION_FIELD_NUMBER: _ClassVar[int]
    counter_account: _containers.RepeatedCompositeFieldContainer[_common_pb2.CounterAccount]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    operate_type: str
    request_id: str
    status: int
    text: str
    trading_session: _containers.RepeatedCompositeFieldContainer[_common_pb2.TradingSession]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., trading_session: _Optional[_Iterable[_Union[_common_pb2.TradingSession, _Mapping]]] = ..., counter_account: _Optional[_Iterable[_Union[_common_pb2.CounterAccount, _Mapping]]] = ...) -> None: ...

class UpdateOrderReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "op_user", "order", "order_action", "request_id", "trade"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    ORDER_ACTION_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TRADE_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    order: _common_pb2.Order
    order_action: str
    request_id: str
    trade: _containers.RepeatedCompositeFieldContainer[_common_pb2.Trade]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ..., order_action: _Optional[str] = ..., order: _Optional[_Union[_common_pb2.Order, _Mapping]] = ..., trade: _Optional[_Iterable[_Union[_common_pb2.Trade, _Mapping]]] = ...) -> None: ...

class UpdateOrderRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "request_id", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class UpdateRiskMarketParamsReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "op_user", "operate_type", "request_id", "risk_params"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RISK_PARAMS_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    operate_type: str
    request_id: str
    risk_params: _containers.RepeatedCompositeFieldContainer[_common_pb2.RiskMarketParams]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[str] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ..., risk_params: _Optional[_Iterable[_Union[_common_pb2.RiskMarketParams, _Mapping]]] = ...) -> None: ...

class UpdateRiskMarketParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "operate_type", "request_id", "risk_params", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RISK_PARAMS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    operate_type: str
    request_id: str
    risk_params: _containers.RepeatedCompositeFieldContainer[_common_pb2.RiskMarketParams]
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., risk_params: _Optional[_Iterable[_Union[_common_pb2.RiskMarketParams, _Mapping]]] = ...) -> None: ...

class UpdateRiskParamsReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "op_user", "operate_type", "request_id", "risk_item"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RISK_ITEM_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    operate_type: str
    request_id: str
    risk_item: _containers.RepeatedCompositeFieldContainer[_common_pb2.RiskItem]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[str] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ..., risk_item: _Optional[_Iterable[_Union[_common_pb2.RiskItem, _Mapping]]] = ...) -> None: ...

class UpdateRiskParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "operate_type", "request_id", "risk_item", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RISK_ITEM_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    operate_type: str
    request_id: str
    risk_item: _containers.RepeatedCompositeFieldContainer[_common_pb2.RiskItem]
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., risk_item: _Optional[_Iterable[_Union[_common_pb2.RiskItem, _Mapping]]] = ...) -> None: ...

class UpdateRiskStatReq(_message.Message):
    __slots__ = ["account_id", "instrument_id", "last_timestamp", "msg_type", "node_name", "node_type", "op_user", "request_id", "risk_code", "risk_stat_value"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RISK_CODE_FIELD_NUMBER: _ClassVar[int]
    RISK_STAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    instrument_id: str
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    request_id: str
    risk_code: str
    risk_stat_value: float
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ..., account_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., risk_code: _Optional[str] = ..., risk_stat_value: _Optional[float] = ...) -> None: ...

class UpdateRiskStatRsp(_message.Message):
    __slots__ = ["account_id", "instrument_id", "last_timestamp", "msg_type", "node_name", "node_type", "request_id", "risk_code", "risk_stat_value", "status", "text"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RISK_CODE_FIELD_NUMBER: _ClassVar[int]
    RISK_STAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    instrument_id: str
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    risk_code: str
    risk_stat_value: float
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., account_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., risk_code: _Optional[str] = ..., risk_stat_value: _Optional[float] = ...) -> None: ...

class UserMockRequest(_message.Message):
    __slots__ = ["account_id", "cancel_qty", "exec_type", "msg_type", "orig_cl_order_id", "reject_qty", "sequence", "trade_id", "trade_price", "trade_qty"]
    class ExecType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CANCEL_QTY_FIELD_NUMBER: _ClassVar[int]
    EXEC_TYPE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORIG_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    REJECT_QTY_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    TRADE_ID_FIELD_NUMBER: _ClassVar[int]
    TRADE_PRICE_FIELD_NUMBER: _ClassVar[int]
    TRADE_QTY_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    cancel_qty: int
    exec_type: UserMockRequest.ExecType
    kCancelRejected: UserMockRequest.ExecType
    kCanceled: UserMockRequest.ExecType
    kNew: UserMockRequest.ExecType
    kPendingCancel: UserMockRequest.ExecType
    kPendingNew: UserMockRequest.ExecType
    kRejected: UserMockRequest.ExecType
    kTrade: UserMockRequest.ExecType
    kUnknown: UserMockRequest.ExecType
    msg_type: int
    orig_cl_order_id: str
    reject_qty: int
    sequence: int
    trade_id: str
    trade_price: float
    trade_qty: int
    def __init__(self, msg_type: _Optional[int] = ..., sequence: _Optional[int] = ..., orig_cl_order_id: _Optional[str] = ..., exec_type: _Optional[_Union[UserMockRequest.ExecType, str]] = ..., trade_id: _Optional[str] = ..., trade_price: _Optional[float] = ..., trade_qty: _Optional[int] = ..., cancel_qty: _Optional[int] = ..., reject_qty: _Optional[int] = ..., account_id: _Optional[str] = ...) -> None: ...
