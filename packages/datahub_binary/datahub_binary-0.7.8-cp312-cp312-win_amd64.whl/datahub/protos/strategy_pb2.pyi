import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ArbitrageStrategyStatEvent(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "reason", "signal_id", "status", "strategy_id", "strategy_name"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    reason: str
    signal_id: int
    status: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., signal_id: _Optional[int] = ..., status: _Optional[str] = ..., reason: _Optional[str] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class BookStatDetail(_message.Message):
    __slots__ = ["active_order_nums", "avail_qty", "buy_amount", "buy_qty", "contract_unit", "current_qty", "instrument_id", "last_px", "posi_amount", "posi_side", "sell_amount", "sell_qty", "sod_amount", "sod_qty", "status", "strategy_id", "strategy_name", "trade_date"]
    ACTIVE_ORDER_NUMS_FIELD_NUMBER: _ClassVar[int]
    AVAIL_QTY_FIELD_NUMBER: _ClassVar[int]
    BUY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    BUY_QTY_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    CURRENT_QTY_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_PX_FIELD_NUMBER: _ClassVar[int]
    POSI_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    POSI_SIDE_FIELD_NUMBER: _ClassVar[int]
    SELL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SELL_QTY_FIELD_NUMBER: _ClassVar[int]
    SOD_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SOD_QTY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TRADE_DATE_FIELD_NUMBER: _ClassVar[int]
    active_order_nums: int
    avail_qty: int
    buy_amount: float
    buy_qty: int
    contract_unit: float
    current_qty: int
    instrument_id: str
    last_px: float
    posi_amount: float
    posi_side: int
    sell_amount: float
    sell_qty: int
    sod_amount: float
    sod_qty: int
    status: str
    strategy_id: int
    strategy_name: str
    trade_date: str
    def __init__(self, strategy_name: _Optional[str] = ..., instrument_id: _Optional[str] = ..., sod_qty: _Optional[int] = ..., avail_qty: _Optional[int] = ..., trade_date: _Optional[str] = ..., strategy_id: _Optional[int] = ..., current_qty: _Optional[int] = ..., posi_amount: _Optional[float] = ..., last_px: _Optional[float] = ..., contract_unit: _Optional[float] = ..., posi_side: _Optional[int] = ..., buy_qty: _Optional[int] = ..., sell_qty: _Optional[int] = ..., buy_amount: _Optional[float] = ..., sell_amount: _Optional[float] = ..., active_order_nums: _Optional[int] = ..., sod_amount: _Optional[float] = ..., status: _Optional[str] = ...) -> None: ...

class BookStatEvent(_message.Message):
    __slots__ = ["auto_hedge_strategy_id", "book_id", "book_stat_details", "comments", "exposure", "is_auto_hedge", "mock_book", "msg_type", "settle_currency_id"]
    AUTO_HEDGE_STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    BOOK_ID_FIELD_NUMBER: _ClassVar[int]
    BOOK_STAT_DETAILS_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    EXPOSURE_FIELD_NUMBER: _ClassVar[int]
    IS_AUTO_HEDGE_FIELD_NUMBER: _ClassVar[int]
    MOCK_BOOK_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    SETTLE_CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
    auto_hedge_strategy_id: int
    book_id: str
    book_stat_details: _containers.RepeatedCompositeFieldContainer[BookStatDetail]
    comments: str
    exposure: float
    is_auto_hedge: int
    mock_book: str
    msg_type: int
    settle_currency_id: str
    def __init__(self, msg_type: _Optional[int] = ..., book_id: _Optional[str] = ..., comments: _Optional[str] = ..., settle_currency_id: _Optional[str] = ..., exposure: _Optional[float] = ..., mock_book: _Optional[str] = ..., is_auto_hedge: _Optional[int] = ..., auto_hedge_strategy_id: _Optional[int] = ..., book_stat_details: _Optional[_Iterable[_Union[BookStatDetail, _Mapping]]] = ...) -> None: ...

class LoginReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "request_id"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class LoginRsp(_message.Message):
    __slots__ = ["is_succ", "msg_type", "node_name", "node_type", "request_id", "text"]
    IS_SUCC_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    is_succ: bool
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., is_succ: bool = ..., text: _Optional[str] = ...) -> None: ...

class ManagerErrorMsg(_message.Message):
    __slots__ = ["error_msg", "last_timestamp", "msg_type", "request_id"]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    error_msg: str
    last_timestamp: int
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., error_msg: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class ManagerNotLogin(_message.Message):
    __slots__ = ["last_timestamp", "msg_type"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class MonitorEvent(_message.Message):
    __slots__ = ["labels", "last_timestamp", "metric_name", "msg_type", "node_name", "node_type", "value"]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    labels: str
    last_timestamp: int
    metric_name: str
    msg_type: int
    node_name: str
    node_type: int
    value: float
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., metric_name: _Optional[str] = ..., labels: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...

class Ping(_message.Message):
    __slots__ = ["msg_sequence", "msg_type"]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_sequence: int
    msg_type: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ...) -> None: ...

class Pong(_message.Message):
    __slots__ = ["msg_sequence", "msg_type"]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_sequence: int
    msg_type: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ...) -> None: ...

class QryBookStatReq(_message.Message):
    __slots__ = ["book_id", "msg_type", "request_id"]
    BOOK_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    book_id: str
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., book_id: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryBookStatRsp(_message.Message):
    __slots__ = ["books", "msg_type", "request_id", "status", "text"]
    class Book(_message.Message):
        __slots__ = ["auto_hedge_strategy_id", "book_id", "book_stat_details", "comments", "exposure", "is_auto_hedge", "mock_book", "settle_currency_id"]
        AUTO_HEDGE_STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
        BOOK_ID_FIELD_NUMBER: _ClassVar[int]
        BOOK_STAT_DETAILS_FIELD_NUMBER: _ClassVar[int]
        COMMENTS_FIELD_NUMBER: _ClassVar[int]
        EXPOSURE_FIELD_NUMBER: _ClassVar[int]
        IS_AUTO_HEDGE_FIELD_NUMBER: _ClassVar[int]
        MOCK_BOOK_FIELD_NUMBER: _ClassVar[int]
        SETTLE_CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
        auto_hedge_strategy_id: int
        book_id: str
        book_stat_details: _containers.RepeatedCompositeFieldContainer[BookStatDetail]
        comments: str
        exposure: float
        is_auto_hedge: int
        mock_book: str
        settle_currency_id: str
        def __init__(self, book_id: _Optional[str] = ..., comments: _Optional[str] = ..., settle_currency_id: _Optional[str] = ..., exposure: _Optional[float] = ..., mock_book: _Optional[str] = ..., is_auto_hedge: _Optional[int] = ..., auto_hedge_strategy_id: _Optional[int] = ..., book_stat_details: _Optional[_Iterable[_Union[BookStatDetail, _Mapping]]] = ...) -> None: ...
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    books: _containers.RepeatedCompositeFieldContainer[QryBookStatRsp.Book]
    msg_type: int
    request_id: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., books: _Optional[_Iterable[_Union[QryBookStatRsp.Book, _Mapping]]] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class QryStrategyStatReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "op_user", "request_id", "strategy_id", "strategy_name", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    request_id: str
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., text: _Optional[str] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ...) -> None: ...

class QryStrategyStatRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "request_id", "strategy_id", "strategy_name", "strategy_stat"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_STAT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    strategy_id: int
    strategy_name: str
    strategy_stat: _containers.RepeatedCompositeFieldContainer[StrategyStatDetail]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., strategy_stat: _Optional[_Iterable[_Union[StrategyStatDetail, _Mapping]]] = ...) -> None: ...

class StrategyControlReq(_message.Message):
    __slots__ = ["control_type", "last_timestamp", "msg_type", "node_name", "node_type", "op_user", "operate_type", "request_id", "strategy_id", "strategy_name"]
    class ControlType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CONTROL_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    control_type: StrategyControlReq.ControlType
    kClose: StrategyControlReq.ControlType
    kInit: StrategyControlReq.ControlType
    kPause: StrategyControlReq.ControlType
    kRun: StrategyControlReq.ControlType
    kStop: StrategyControlReq.ControlType
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    operate_type: int
    request_id: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[int] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., control_type: _Optional[_Union[StrategyControlReq.ControlType, str]] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ...) -> None: ...

class StrategyControlRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "request_id", "status", "strategy_id", "strategy_name", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    status: int
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., strategy_name: _Optional[str] = ..., strategy_id: _Optional[int] = ..., status: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class StrategyEvent(_message.Message):
    __slots__ = ["control_status", "last_timestamp", "msg_type", "node_name", "node_type", "text"]
    CONTROL_STATUS_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    control_status: int
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., control_status: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class StrategyLogEvent(_message.Message):
    __slots__ = ["file_name", "function_name", "last_timestamp", "line", "log_level", "msg_type", "node_name", "node_type", "occur_time", "strategy_id", "strategy_name", "text"]
    class LogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DEBUG: StrategyLogEvent.LogLevel
    ERROR: StrategyLogEvent.LogLevel
    FATAL: StrategyLogEvent.LogLevel
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    INFO: StrategyLogEvent.LogLevel
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OCCUR_TIME_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TRACE: StrategyLogEvent.LogLevel
    WARN: StrategyLogEvent.LogLevel
    file_name: str
    function_name: str
    last_timestamp: int
    line: int
    log_level: StrategyLogEvent.LogLevel
    msg_type: int
    node_name: str
    node_type: int
    occur_time: int
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., log_level: _Optional[_Union[StrategyLogEvent.LogLevel, str]] = ..., occur_time: _Optional[int] = ..., file_name: _Optional[str] = ..., function_name: _Optional[str] = ..., line: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class StrategyStatDetail(_message.Message):
    __slots__ = ["account_id", "active_order_nums", "active_order_qty", "ask_premium_rate", "ask_price", "avail_qty", "bid_premium_rate", "bid_price", "buy_amount", "buy_qty", "contract_unit", "cost_price", "current_qty", "depth_quote", "exposure", "float_pnl", "impact_factor", "instrument_id", "last_px", "original_price", "posi_adjust_rate", "posi_amount", "posi_side", "pre_close_price", "sell_amount", "sell_qty", "signal_id", "signal_name", "sod_amount", "sod_qty", "stat_fields", "stat_status", "status", "strategy_id", "strategy_name", "target_qty", "text", "theory_price", "total_cancel_nums", "total_order_nums", "total_order_qty"]
    class QuoteLevelData(_message.Message):
        __slots__ = ["ask_price", "ask_volume", "bid_price", "bid_volume"]
        ASK_PRICE_FIELD_NUMBER: _ClassVar[int]
        ASK_VOLUME_FIELD_NUMBER: _ClassVar[int]
        BID_PRICE_FIELD_NUMBER: _ClassVar[int]
        BID_VOLUME_FIELD_NUMBER: _ClassVar[int]
        ask_price: int
        ask_volume: int
        bid_price: int
        bid_volume: int
        def __init__(self, bid_price: _Optional[int] = ..., bid_volume: _Optional[int] = ..., ask_price: _Optional[int] = ..., ask_volume: _Optional[int] = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ORDER_NUMS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    ASK_PREMIUM_RATE_FIELD_NUMBER: _ClassVar[int]
    ASK_PRICE_FIELD_NUMBER: _ClassVar[int]
    AVAIL_QTY_FIELD_NUMBER: _ClassVar[int]
    BID_PREMIUM_RATE_FIELD_NUMBER: _ClassVar[int]
    BID_PRICE_FIELD_NUMBER: _ClassVar[int]
    BUY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    BUY_QTY_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    COST_PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_QTY_FIELD_NUMBER: _ClassVar[int]
    DEPTH_QUOTE_FIELD_NUMBER: _ClassVar[int]
    EXPOSURE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_PNL_FIELD_NUMBER: _ClassVar[int]
    IMPACT_FACTOR_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_PX_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_PRICE_FIELD_NUMBER: _ClassVar[int]
    POSI_ADJUST_RATE_FIELD_NUMBER: _ClassVar[int]
    POSI_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    POSI_SIDE_FIELD_NUMBER: _ClassVar[int]
    PRE_CLOSE_PRICE_FIELD_NUMBER: _ClassVar[int]
    SELL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SELL_QTY_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    SOD_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SOD_QTY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STAT_FIELDS_FIELD_NUMBER: _ClassVar[int]
    STAT_STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_QTY_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    THEORY_PRICE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CANCEL_NUMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ORDER_NUMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    active_order_nums: int
    active_order_qty: int
    ask_premium_rate: float
    ask_price: float
    avail_qty: int
    bid_premium_rate: float
    bid_price: float
    buy_amount: float
    buy_qty: int
    contract_unit: float
    cost_price: float
    current_qty: int
    depth_quote: _containers.RepeatedCompositeFieldContainer[StrategyStatDetail.QuoteLevelData]
    exposure: float
    float_pnl: float
    impact_factor: float
    instrument_id: str
    last_px: float
    original_price: float
    posi_adjust_rate: float
    posi_amount: float
    posi_side: int
    pre_close_price: float
    sell_amount: float
    sell_qty: int
    signal_id: int
    signal_name: str
    sod_amount: float
    sod_qty: int
    stat_fields: str
    stat_status: int
    status: str
    strategy_id: int
    strategy_name: str
    target_qty: int
    text: str
    theory_price: float
    total_cancel_nums: int
    total_order_nums: int
    total_order_qty: int
    def __init__(self, strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., status: _Optional[str] = ..., instrument_id: _Optional[str] = ..., sod_amount: _Optional[float] = ..., sod_qty: _Optional[int] = ..., current_qty: _Optional[int] = ..., posi_amount: _Optional[float] = ..., last_px: _Optional[float] = ..., buy_amount: _Optional[float] = ..., sell_amount: _Optional[float] = ..., buy_qty: _Optional[int] = ..., sell_qty: _Optional[int] = ..., exposure: _Optional[float] = ..., active_order_nums: _Optional[int] = ..., text: _Optional[str] = ..., avail_qty: _Optional[int] = ..., posi_side: _Optional[int] = ..., target_qty: _Optional[int] = ..., depth_quote: _Optional[_Iterable[_Union[StrategyStatDetail.QuoteLevelData, _Mapping]]] = ..., bid_premium_rate: _Optional[float] = ..., ask_premium_rate: _Optional[float] = ..., impact_factor: _Optional[float] = ..., theory_price: _Optional[float] = ..., original_price: _Optional[float] = ..., cost_price: _Optional[float] = ..., pre_close_price: _Optional[float] = ..., float_pnl: _Optional[float] = ..., contract_unit: _Optional[float] = ..., posi_adjust_rate: _Optional[float] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., active_order_qty: _Optional[int] = ..., total_order_qty: _Optional[int] = ..., bid_price: _Optional[float] = ..., ask_price: _Optional[float] = ..., stat_fields: _Optional[str] = ..., stat_status: _Optional[int] = ..., account_id: _Optional[str] = ..., total_order_nums: _Optional[int] = ..., total_cancel_nums: _Optional[int] = ...) -> None: ...

class StrategyStatEvent(_message.Message):
    __slots__ = ["last_timestamp", "msg_sequence", "msg_type", "node_name", "node_type", "strategy_id", "strategy_name", "strategy_stat"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_STAT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    strategy_id: int
    strategy_name: str
    strategy_stat: _containers.RepeatedCompositeFieldContainer[StrategyStatDetail]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., strategy_stat: _Optional[_Iterable[_Union[StrategyStatDetail, _Mapping]]] = ...) -> None: ...

class UpdateStrategyGlobalParamsReq(_message.Message):
    __slots__ = ["last_timestamp", "monitor_params", "msg_type", "node_name", "node_type", "op_user", "operate_type", "request_id", "strategy_params", "strategy_template_id", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MONITOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_PARAMS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    monitor_params: str
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    operate_type: int
    request_id: str
    strategy_params: str
    strategy_template_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[int] = ..., strategy_template_id: _Optional[str] = ..., text: _Optional[str] = ..., strategy_params: _Optional[str] = ..., monitor_params: _Optional[str] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ...) -> None: ...

class UpdateStrategyGlobalParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "monitor_params", "msg_type", "node_name", "node_type", "request_id", "status", "strategy_params", "strategy_template_id", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MONITOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_PARAMS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    monitor_params: str
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    status: int
    strategy_params: str
    strategy_template_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., strategy_template_id: _Optional[str] = ..., status: _Optional[int] = ..., request_id: _Optional[str] = ..., text: _Optional[str] = ..., strategy_params: _Optional[str] = ..., monitor_params: _Optional[str] = ...) -> None: ...

class UpdateStrategyParamsReq(_message.Message):
    __slots__ = ["last_timestamp", "monitor_params", "msg_type", "node_name", "node_type", "op_user", "operate_type", "request_id", "signal_id", "signal_name", "strategy_id", "strategy_instruments", "strategy_name", "strategy_params", "target_qty", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MONITOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_INSTRUMENTS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_PARAMS_FIELD_NUMBER: _ClassVar[int]
    TARGET_QTY_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    monitor_params: str
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    operate_type: int
    request_id: str
    signal_id: int
    signal_name: str
    strategy_id: int
    strategy_instruments: _containers.RepeatedCompositeFieldContainer[_common_pb2.StrategyInstrument]
    strategy_name: str
    strategy_params: str
    target_qty: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[int] = ..., strategy_name: _Optional[str] = ..., strategy_id: _Optional[int] = ..., text: _Optional[str] = ..., strategy_params: _Optional[str] = ..., monitor_params: _Optional[str] = ..., strategy_instruments: _Optional[_Iterable[_Union[_common_pb2.StrategyInstrument, _Mapping]]] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., target_qty: _Optional[int] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ...) -> None: ...

class UpdateStrategyParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "monitor_params", "msg_type", "node_name", "node_type", "request_id", "signal_id", "signal_name", "status", "strategy_id", "strategy_instruments", "strategy_name", "strategy_params", "target_qty", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MONITOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_INSTRUMENTS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_PARAMS_FIELD_NUMBER: _ClassVar[int]
    TARGET_QTY_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    monitor_params: str
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    signal_id: int
    signal_name: str
    status: int
    strategy_id: int
    strategy_instruments: _containers.RepeatedCompositeFieldContainer[_common_pb2.StrategyInstrument]
    strategy_name: str
    strategy_params: str
    target_qty: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., strategy_name: _Optional[str] = ..., strategy_id: _Optional[int] = ..., status: _Optional[int] = ..., request_id: _Optional[str] = ..., text: _Optional[str] = ..., strategy_params: _Optional[str] = ..., monitor_params: _Optional[str] = ..., strategy_instruments: _Optional[_Iterable[_Union[_common_pb2.StrategyInstrument, _Mapping]]] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., target_qty: _Optional[int] = ...) -> None: ...
