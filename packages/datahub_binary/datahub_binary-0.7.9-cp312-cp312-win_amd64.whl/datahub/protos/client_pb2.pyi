from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
kCash: PosAccountType
kDelta: PosReqType
kInit: PosReqType
kPosTypeApplyAvl: PosType
kPosTypeBuyIn: PosType
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

class AlgoParams(_message.Message):
    __slots__ = ["algo_name", "begin_time", "custom_param", "duration_seconds", "end_time", "expire_time", "interval_seconds", "max_active_order_nums", "order_price_level", "price_cage", "price_limit", "shift_price_tick"]
    ALGO_NAME_FIELD_NUMBER: _ClassVar[int]
    BEGIN_TIME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_PARAM_FIELD_NUMBER: _ClassVar[int]
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    MAX_ACTIVE_ORDER_NUMS_FIELD_NUMBER: _ClassVar[int]
    ORDER_PRICE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    PRICE_CAGE_FIELD_NUMBER: _ClassVar[int]
    PRICE_LIMIT_FIELD_NUMBER: _ClassVar[int]
    SHIFT_PRICE_TICK_FIELD_NUMBER: _ClassVar[int]
    algo_name: str
    begin_time: int
    custom_param: str
    duration_seconds: int
    end_time: int
    expire_time: int
    interval_seconds: int
    max_active_order_nums: int
    order_price_level: int
    price_cage: float
    price_limit: float
    shift_price_tick: int
    def __init__(self, algo_name: _Optional[str] = ..., begin_time: _Optional[int] = ..., end_time: _Optional[int] = ..., duration_seconds: _Optional[int] = ..., interval_seconds: _Optional[int] = ..., order_price_level: _Optional[int] = ..., shift_price_tick: _Optional[int] = ..., price_limit: _Optional[float] = ..., max_active_order_nums: _Optional[int] = ..., price_cage: _Optional[float] = ..., custom_param: _Optional[str] = ..., expire_time: _Optional[int] = ...) -> None: ...

class AppendBasketOrder(_message.Message):
    __slots__ = ["algo_params", "algo_type", "basket_cl_order_id", "msg_type", "request_id"]
    ALGO_PARAMS_FIELD_NUMBER: _ClassVar[int]
    ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
    BASKET_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    algo_params: AlgoParams
    algo_type: int
    basket_cl_order_id: str
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., basket_cl_order_id: _Optional[str] = ..., algo_type: _Optional[int] = ..., algo_params: _Optional[_Union[AlgoParams, _Mapping]] = ..., request_id: _Optional[str] = ...) -> None: ...

class AppendBasketOrderRsp(_message.Message):
    __slots__ = ["basket_cl_order_id", "msg_type", "reason", "request_id", "status"]
    BASKET_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    basket_cl_order_id: str
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., basket_cl_order_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class ApplyDefaultStrategyParamsReq(_message.Message):
    __slots__ = ["msg_type", "request_id", "strategy_id_list"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    request_id: str
    strategy_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., strategy_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class ApplyDefaultStrategyParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "request_id", "status", "strategy_id_list", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    request_id: str
    status: int
    strategy_id_list: _containers.RepeatedScalarFieldContainer[int]
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., strategy_id_list: _Optional[_Iterable[int]] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class ArbitrageOrder(_message.Message):
    __slots__ = ["algo_params", "algo_type", "arbitrage_cl_order_id", "arbitrage_order_id", "arbitrage_type", "attachment", "leg_cl_order_id", "leg_exec_seq", "leg_id", "leg_order_amt", "leg_type", "order_qty", "order_source", "order_time", "process_amt", "process_qty", "reason", "side", "status", "strategy_id", "strategy_name", "user_id"]
    ALGO_PARAMS_FIELD_NUMBER: _ClassVar[int]
    ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
    ARBITRAGE_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ARBITRAGE_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ARBITRAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    LEG_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    LEG_EXEC_SEQ_FIELD_NUMBER: _ClassVar[int]
    LEG_ID_FIELD_NUMBER: _ClassVar[int]
    LEG_ORDER_AMT_FIELD_NUMBER: _ClassVar[int]
    LEG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    ORDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ORDER_TIME_FIELD_NUMBER: _ClassVar[int]
    PROCESS_AMT_FIELD_NUMBER: _ClassVar[int]
    PROCESS_QTY_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    algo_params: AlgoParams
    algo_type: int
    arbitrage_cl_order_id: str
    arbitrage_order_id: str
    arbitrage_type: str
    attachment: str
    leg_cl_order_id: str
    leg_exec_seq: str
    leg_id: str
    leg_order_amt: float
    leg_type: str
    order_qty: int
    order_source: str
    order_time: int
    process_amt: float
    process_qty: float
    reason: str
    side: int
    status: int
    strategy_id: int
    strategy_name: str
    user_id: str
    def __init__(self, arbitrage_order_id: _Optional[str] = ..., arbitrage_cl_order_id: _Optional[str] = ..., arbitrage_type: _Optional[str] = ..., order_source: _Optional[str] = ..., attachment: _Optional[str] = ..., process_qty: _Optional[float] = ..., process_amt: _Optional[float] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., strategy_id: _Optional[int] = ..., leg_exec_seq: _Optional[str] = ..., user_id: _Optional[str] = ..., order_time: _Optional[int] = ..., strategy_name: _Optional[str] = ..., leg_id: _Optional[str] = ..., leg_type: _Optional[str] = ..., order_qty: _Optional[int] = ..., side: _Optional[int] = ..., leg_order_amt: _Optional[float] = ..., leg_cl_order_id: _Optional[str] = ..., algo_type: _Optional[int] = ..., algo_params: _Optional[_Union[AlgoParams, _Mapping]] = ...) -> None: ...

class ArbitrageOrderEvent(_message.Message):
    __slots__ = ["msg_type", "order"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    order: ArbitrageOrder
    def __init__(self, msg_type: _Optional[int] = ..., order: _Optional[_Union[ArbitrageOrder, _Mapping]] = ...) -> None: ...

class ArbitrageStrategyStatEvent(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "reason", "signal_id", "status", "strategy_id", "strategy_name"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    reason: str
    signal_id: int
    status: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., signal_id: _Optional[int] = ..., status: _Optional[str] = ..., reason: _Optional[str] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class BasketInfo(_message.Message):
    __slots__ = ["basket_info_details", "comments", "etf_instrument_id", "etf_unit", "strategy_id", "strategy_name", "template_id", "template_type"]
    BASKET_INFO_DETAILS_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    ETF_INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ETF_UNIT_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    basket_info_details: _containers.RepeatedCompositeFieldContainer[BasketInfoDetail]
    comments: str
    etf_instrument_id: str
    etf_unit: int
    strategy_id: int
    strategy_name: str
    template_id: str
    template_type: str
    def __init__(self, template_id: _Optional[str] = ..., basket_info_details: _Optional[_Iterable[_Union[BasketInfoDetail, _Mapping]]] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., etf_instrument_id: _Optional[str] = ..., etf_unit: _Optional[int] = ..., template_type: _Optional[str] = ..., comments: _Optional[str] = ...) -> None: ...

class BasketInfoDetail(_message.Message):
    __slots__ = ["comments", "component_instrument_id", "component_qty", "side"]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_QTY_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    comments: str
    component_instrument_id: str
    component_qty: int
    side: int
    def __init__(self, component_instrument_id: _Optional[str] = ..., component_qty: _Optional[int] = ..., side: _Optional[int] = ..., comments: _Optional[str] = ...) -> None: ...

class BasketOrderEvent(_message.Message):
    __slots__ = ["algo_params", "algo_type", "basket_amt", "basket_cl_order_id", "basket_id", "basket_qty", "cancel_qty", "create_time", "msg_type", "order_qty", "process_amt", "process_qty", "reason", "reject_qty", "side", "status", "strategy_id", "strategy_name", "template_id", "trade_amt", "trade_qty", "user_id"]
    ALGO_PARAMS_FIELD_NUMBER: _ClassVar[int]
    ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
    BASKET_AMT_FIELD_NUMBER: _ClassVar[int]
    BASKET_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    BASKET_ID_FIELD_NUMBER: _ClassVar[int]
    BASKET_QTY_FIELD_NUMBER: _ClassVar[int]
    CANCEL_QTY_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    PROCESS_AMT_FIELD_NUMBER: _ClassVar[int]
    PROCESS_QTY_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REJECT_QTY_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TRADE_AMT_FIELD_NUMBER: _ClassVar[int]
    TRADE_QTY_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    algo_params: AlgoParams
    algo_type: int
    basket_amt: float
    basket_cl_order_id: str
    basket_id: str
    basket_qty: int
    cancel_qty: int
    create_time: int
    msg_type: int
    order_qty: int
    process_amt: float
    process_qty: float
    reason: str
    reject_qty: int
    side: int
    status: int
    strategy_id: int
    strategy_name: str
    template_id: str
    trade_amt: float
    trade_qty: int
    user_id: str
    def __init__(self, msg_type: _Optional[int] = ..., basket_cl_order_id: _Optional[str] = ..., basket_id: _Optional[str] = ..., template_id: _Optional[str] = ..., status: _Optional[int] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., side: _Optional[int] = ..., basket_amt: _Optional[float] = ..., trade_amt: _Optional[float] = ..., basket_qty: _Optional[int] = ..., process_qty: _Optional[float] = ..., process_amt: _Optional[float] = ..., create_time: _Optional[int] = ..., algo_type: _Optional[int] = ..., algo_params: _Optional[_Union[AlgoParams, _Mapping]] = ..., reason: _Optional[str] = ..., user_id: _Optional[str] = ..., order_qty: _Optional[int] = ..., trade_qty: _Optional[int] = ..., reject_qty: _Optional[int] = ..., cancel_qty: _Optional[int] = ...) -> None: ...

class BasketOrderStat(_message.Message):
    __slots__ = ["active_qty", "cancel_qty", "component_instrument_id", "cost_price", "fill_amt", "fill_qty", "order_amt", "order_qty", "order_stat_details", "order_status", "process_amt", "process_qty", "reject_qty", "side"]
    ACTIVE_QTY_FIELD_NUMBER: _ClassVar[int]
    CANCEL_QTY_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    COST_PRICE_FIELD_NUMBER: _ClassVar[int]
    FILL_AMT_FIELD_NUMBER: _ClassVar[int]
    FILL_QTY_FIELD_NUMBER: _ClassVar[int]
    ORDER_AMT_FIELD_NUMBER: _ClassVar[int]
    ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    ORDER_STATUS_FIELD_NUMBER: _ClassVar[int]
    ORDER_STAT_DETAILS_FIELD_NUMBER: _ClassVar[int]
    PROCESS_AMT_FIELD_NUMBER: _ClassVar[int]
    PROCESS_QTY_FIELD_NUMBER: _ClassVar[int]
    REJECT_QTY_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    active_qty: int
    cancel_qty: int
    component_instrument_id: str
    cost_price: float
    fill_amt: float
    fill_qty: int
    order_amt: float
    order_qty: int
    order_stat_details: _containers.RepeatedCompositeFieldContainer[BasketOrderStatDetail]
    order_status: int
    process_amt: float
    process_qty: float
    reject_qty: int
    side: int
    def __init__(self, component_instrument_id: _Optional[str] = ..., order_qty: _Optional[int] = ..., fill_qty: _Optional[int] = ..., active_qty: _Optional[int] = ..., reject_qty: _Optional[int] = ..., cancel_qty: _Optional[int] = ..., order_status: _Optional[int] = ..., process_qty: _Optional[float] = ..., process_amt: _Optional[float] = ..., cost_price: _Optional[float] = ..., fill_amt: _Optional[float] = ..., order_amt: _Optional[float] = ..., order_stat_details: _Optional[_Iterable[_Union[BasketOrderStatDetail, _Mapping]]] = ..., side: _Optional[int] = ...) -> None: ...

class BasketOrderStatDetail(_message.Message):
    __slots__ = ["active_qty", "cost_price", "fill_amt", "fill_qty", "instrument_id", "order_amt", "order_id", "order_msg", "order_qty", "order_status", "order_time", "reject_qty", "side"]
    ACTIVE_QTY_FIELD_NUMBER: _ClassVar[int]
    COST_PRICE_FIELD_NUMBER: _ClassVar[int]
    FILL_AMT_FIELD_NUMBER: _ClassVar[int]
    FILL_QTY_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_AMT_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_MSG_FIELD_NUMBER: _ClassVar[int]
    ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    ORDER_STATUS_FIELD_NUMBER: _ClassVar[int]
    ORDER_TIME_FIELD_NUMBER: _ClassVar[int]
    REJECT_QTY_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    active_qty: int
    cost_price: float
    fill_amt: float
    fill_qty: int
    instrument_id: str
    order_amt: float
    order_id: str
    order_msg: str
    order_qty: int
    order_status: int
    order_time: int
    reject_qty: int
    side: int
    def __init__(self, instrument_id: _Optional[str] = ..., order_qty: _Optional[int] = ..., fill_qty: _Optional[int] = ..., active_qty: _Optional[int] = ..., order_status: _Optional[int] = ..., order_msg: _Optional[str] = ..., cost_price: _Optional[float] = ..., fill_amt: _Optional[float] = ..., order_amt: _Optional[float] = ..., order_id: _Optional[str] = ..., reject_qty: _Optional[int] = ..., order_time: _Optional[int] = ..., side: _Optional[int] = ...) -> None: ...

class Book(_message.Message):
    __slots__ = ["auto_hedge_strategy_id", "auto_hedge_strategy_name", "book_id", "book_type", "comments", "exposure", "is_auto_hedge", "last_timestamp", "long_exposure", "settle_currency_id", "short_exposure", "sod_pnl", "strategy_summaries", "total_pnl", "trade_pnl"]
    AUTO_HEDGE_STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    AUTO_HEDGE_STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    BOOK_ID_FIELD_NUMBER: _ClassVar[int]
    BOOK_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    EXPOSURE_FIELD_NUMBER: _ClassVar[int]
    IS_AUTO_HEDGE_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LONG_EXPOSURE_FIELD_NUMBER: _ClassVar[int]
    SETTLE_CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
    SHORT_EXPOSURE_FIELD_NUMBER: _ClassVar[int]
    SOD_PNL_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PNL_FIELD_NUMBER: _ClassVar[int]
    TRADE_PNL_FIELD_NUMBER: _ClassVar[int]
    auto_hedge_strategy_id: int
    auto_hedge_strategy_name: str
    book_id: str
    book_type: str
    comments: str
    exposure: float
    is_auto_hedge: int
    last_timestamp: int
    long_exposure: float
    settle_currency_id: str
    short_exposure: float
    sod_pnl: float
    strategy_summaries: _containers.RepeatedCompositeFieldContainer[StrategySummary]
    total_pnl: float
    trade_pnl: float
    def __init__(self, book_id: _Optional[str] = ..., comments: _Optional[str] = ..., settle_currency_id: _Optional[str] = ..., exposure: _Optional[float] = ..., trade_pnl: _Optional[float] = ..., total_pnl: _Optional[float] = ..., book_type: _Optional[str] = ..., is_auto_hedge: _Optional[int] = ..., auto_hedge_strategy_id: _Optional[int] = ..., auto_hedge_strategy_name: _Optional[str] = ..., strategy_summaries: _Optional[_Iterable[_Union[StrategySummary, _Mapping]]] = ..., last_timestamp: _Optional[int] = ..., long_exposure: _Optional[float] = ..., short_exposure: _Optional[float] = ..., sod_pnl: _Optional[float] = ...) -> None: ...

class BookStatEvent(_message.Message):
    __slots__ = ["book", "msg_type"]
    BOOK_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    book: Book
    msg_type: int
    def __init__(self, msg_type: _Optional[int] = ..., book: _Optional[_Union[Book, _Mapping]] = ...) -> None: ...

class BookTradeReq(_message.Message):
    __slots__ = ["business_type", "cl_order_id", "instrument_id", "msg_type", "operate_type", "order_price", "order_qty", "order_source", "order_type", "position_effect", "purpose", "request_id", "strategy_id", "strategy_name"]
    BUSINESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_PRICE_FIELD_NUMBER: _ClassVar[int]
    ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    ORDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSITION_EFFECT_FIELD_NUMBER: _ClassVar[int]
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    business_type: str
    cl_order_id: str
    instrument_id: str
    msg_type: int
    operate_type: str
    order_price: float
    order_qty: int
    order_source: str
    order_type: int
    position_effect: int
    purpose: int
    request_id: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., operate_type: _Optional[str] = ..., cl_order_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., order_type: _Optional[int] = ..., position_effect: _Optional[int] = ..., purpose: _Optional[int] = ..., order_price: _Optional[float] = ..., order_qty: _Optional[int] = ..., order_source: _Optional[str] = ..., request_id: _Optional[str] = ..., business_type: _Optional[str] = ...) -> None: ...

class BookTradeRsp(_message.Message):
    __slots__ = ["cl_order_id", "last_timestamp", "msg_type", "operate_type", "reason", "request_id", "status"]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    cl_order_id: str
    last_timestamp: int
    msg_type: int
    operate_type: str
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., operate_type: _Optional[str] = ...) -> None: ...

class CancelAllOrder(_message.Message):
    __slots__ = ["account_id", "cl_order_id", "instrument_id", "investor_id", "market", "msg_sequence", "msg_type", "owner_type", "security_id", "strategy_id", "strategy_name"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    owner_type: int
    security_id: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., owner_type: _Optional[int] = ...) -> None: ...

class CancelArbitrageOrder(_message.Message):
    __slots__ = ["cl_order_id", "msg_type", "request_id"]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    cl_order_id: str
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class CancelArbitrageOrderRsp(_message.Message):
    __slots__ = ["cl_order_id", "msg_type", "reason", "request_id", "status"]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    cl_order_id: str
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class CancelBasketOrder(_message.Message):
    __slots__ = ["basket_cl_order_id", "msg_type", "request_id"]
    BASKET_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    basket_cl_order_id: str
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., basket_cl_order_id: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class CancelBasketOrderRsp(_message.Message):
    __slots__ = ["basket_cl_order_id", "msg_type", "reason", "request_id", "status"]
    BASKET_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    basket_cl_order_id: str
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., basket_cl_order_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class CancelConfirm(_message.Message):
    __slots__ = ["account_id", "appl_id", "cancel_qty", "cl_order_id", "instrument_id", "investor_id", "market", "msg_sequence", "msg_type", "original_cl_order_id", "original_counter_order_id", "original_order_id", "reason", "security_id", "strategy_id", "strategy_name", "text"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CANCEL_QTY_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    original_cl_order_id: str
    original_counter_order_id: str
    original_order_id: str
    reason: int
    security_id: str
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., original_order_id: _Optional[str] = ..., original_cl_order_id: _Optional[str] = ..., original_counter_order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., cancel_qty: _Optional[int] = ..., reason: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class CancelOrder(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "instrument_id", "investor_id", "market", "msg_sequence", "msg_type", "original_cl_order_id", "original_order_id", "owner_type", "security_id", "strategy_id", "strategy_name"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    original_cl_order_id: str
    original_order_id: str
    owner_type: int
    security_id: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., cl_order_id: _Optional[str] = ..., original_order_id: _Optional[str] = ..., original_cl_order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., owner_type: _Optional[int] = ...) -> None: ...

class CancelPendingConfirm(_message.Message):
    __slots__ = ["account_id", "appl_id", "cancel_qty", "cl_order_id", "instrument_id", "investor_id", "market", "msg_sequence", "msg_type", "original_cl_order_id", "original_counter_order_id", "original_order_id", "reason", "security_id", "strategy_id", "strategy_name", "text"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CANCEL_QTY_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    original_cl_order_id: str
    original_counter_order_id: str
    original_order_id: str
    reason: int
    security_id: str
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., original_order_id: _Optional[str] = ..., original_cl_order_id: _Optional[str] = ..., original_counter_order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., cancel_qty: _Optional[int] = ..., reason: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class CancelReject(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "instrument_id", "investor_id", "market", "msg_sequence", "msg_type", "original_cl_order_id", "original_counter_order_id", "original_order_id", "reject_reason", "security_id", "strategy_id", "strategy_name", "text"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    original_cl_order_id: str
    original_counter_order_id: str
    original_order_id: str
    reject_reason: int
    security_id: str
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., original_order_id: _Optional[str] = ..., original_cl_order_id: _Optional[str] = ..., original_counter_order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., reject_reason: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class Currency(_message.Message):
    __slots__ = ["comments", "currency_id", "fx_rate_cny", "update_time"]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
    FX_RATE_CNY_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    comments: str
    currency_id: str
    fx_rate_cny: float
    update_time: str
    def __init__(self, currency_id: _Optional[str] = ..., fx_rate_cny: _Optional[float] = ..., comments: _Optional[str] = ..., update_time: _Optional[str] = ...) -> None: ...

class ETFQuoteSnapshot(_message.Message):
    __slots__ = ["ask_iopv", "bid_iopv", "constituent_nums", "currency_id", "down_limit_nums", "etf_ask_premium_rate", "etf_ask_price", "etf_bid_premium_rate", "etf_bid_price", "etf_deviation", "etf_last_price", "etf_pct_change", "etf_pre_close_price", "etf_premium_rate", "index_deviation", "index_last_price", "index_pct_change", "index_pre_close_price", "instrument_id", "iopv", "iopv_pct_change", "last_timestamp", "market", "md_date", "md_time", "msg_sequence", "msg_type", "pre_close_iopv", "security_id", "security_type", "suspension_nums", "symbol", "up_limit_nums"]
    ASK_IOPV_FIELD_NUMBER: _ClassVar[int]
    BID_IOPV_FIELD_NUMBER: _ClassVar[int]
    CONSTITUENT_NUMS_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
    DOWN_LIMIT_NUMS_FIELD_NUMBER: _ClassVar[int]
    ETF_ASK_PREMIUM_RATE_FIELD_NUMBER: _ClassVar[int]
    ETF_ASK_PRICE_FIELD_NUMBER: _ClassVar[int]
    ETF_BID_PREMIUM_RATE_FIELD_NUMBER: _ClassVar[int]
    ETF_BID_PRICE_FIELD_NUMBER: _ClassVar[int]
    ETF_DEVIATION_FIELD_NUMBER: _ClassVar[int]
    ETF_LAST_PRICE_FIELD_NUMBER: _ClassVar[int]
    ETF_PCT_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ETF_PREMIUM_RATE_FIELD_NUMBER: _ClassVar[int]
    ETF_PRE_CLOSE_PRICE_FIELD_NUMBER: _ClassVar[int]
    INDEX_DEVIATION_FIELD_NUMBER: _ClassVar[int]
    INDEX_LAST_PRICE_FIELD_NUMBER: _ClassVar[int]
    INDEX_PCT_CHANGE_FIELD_NUMBER: _ClassVar[int]
    INDEX_PRE_CLOSE_PRICE_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    IOPV_FIELD_NUMBER: _ClassVar[int]
    IOPV_PCT_CHANGE_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MD_DATE_FIELD_NUMBER: _ClassVar[int]
    MD_TIME_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PRE_CLOSE_IOPV_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUSPENSION_NUMS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    UP_LIMIT_NUMS_FIELD_NUMBER: _ClassVar[int]
    ask_iopv: int
    bid_iopv: int
    constituent_nums: int
    currency_id: str
    down_limit_nums: int
    etf_ask_premium_rate: float
    etf_ask_price: int
    etf_bid_premium_rate: float
    etf_bid_price: int
    etf_deviation: float
    etf_last_price: int
    etf_pct_change: float
    etf_pre_close_price: int
    etf_premium_rate: float
    index_deviation: float
    index_last_price: int
    index_pct_change: float
    index_pre_close_price: int
    instrument_id: str
    iopv: int
    iopv_pct_change: float
    last_timestamp: int
    market: str
    md_date: int
    md_time: int
    msg_sequence: int
    msg_type: int
    pre_close_iopv: int
    security_id: str
    security_type: str
    suspension_nums: int
    symbol: str
    up_limit_nums: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., instrument_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., currency_id: _Optional[str] = ..., security_type: _Optional[str] = ..., symbol: _Optional[str] = ..., constituent_nums: _Optional[int] = ..., suspension_nums: _Optional[int] = ..., up_limit_nums: _Optional[int] = ..., down_limit_nums: _Optional[int] = ..., bid_iopv: _Optional[int] = ..., ask_iopv: _Optional[int] = ..., iopv: _Optional[int] = ..., pre_close_iopv: _Optional[int] = ..., iopv_pct_change: _Optional[float] = ..., etf_last_price: _Optional[int] = ..., etf_bid_price: _Optional[int] = ..., etf_ask_price: _Optional[int] = ..., etf_pre_close_price: _Optional[int] = ..., etf_pct_change: _Optional[float] = ..., index_last_price: _Optional[int] = ..., index_pre_close_price: _Optional[int] = ..., index_pct_change: _Optional[float] = ..., index_deviation: _Optional[float] = ..., etf_deviation: _Optional[float] = ..., etf_bid_premium_rate: _Optional[float] = ..., etf_ask_premium_rate: _Optional[float] = ..., etf_premium_rate: _Optional[float] = ..., md_date: _Optional[int] = ..., md_time: _Optional[int] = ...) -> None: ...

class ETFQuoteTick(_message.Message):
    __slots__ = ["constituent_nums", "down_limit_nums", "etf_ask_price", "etf_bid_price", "etf_last_price", "etf_pct_change", "etf_pre_close_price", "etf_premium_rate", "instrument_id", "iopv", "last_timestamp", "market", "md_date", "md_time", "msg_sequence", "msg_type", "security_id", "security_type", "suspension_nums", "symbol", "up_limit_nums"]
    CONSTITUENT_NUMS_FIELD_NUMBER: _ClassVar[int]
    DOWN_LIMIT_NUMS_FIELD_NUMBER: _ClassVar[int]
    ETF_ASK_PRICE_FIELD_NUMBER: _ClassVar[int]
    ETF_BID_PRICE_FIELD_NUMBER: _ClassVar[int]
    ETF_LAST_PRICE_FIELD_NUMBER: _ClassVar[int]
    ETF_PCT_CHANGE_FIELD_NUMBER: _ClassVar[int]
    ETF_PREMIUM_RATE_FIELD_NUMBER: _ClassVar[int]
    ETF_PRE_CLOSE_PRICE_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    IOPV_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MD_DATE_FIELD_NUMBER: _ClassVar[int]
    MD_TIME_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUSPENSION_NUMS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    UP_LIMIT_NUMS_FIELD_NUMBER: _ClassVar[int]
    constituent_nums: int
    down_limit_nums: int
    etf_ask_price: int
    etf_bid_price: int
    etf_last_price: int
    etf_pct_change: float
    etf_pre_close_price: int
    etf_premium_rate: float
    instrument_id: str
    iopv: int
    last_timestamp: int
    market: str
    md_date: int
    md_time: int
    msg_sequence: int
    msg_type: int
    security_id: str
    security_type: str
    suspension_nums: int
    symbol: str
    up_limit_nums: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., instrument_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., security_type: _Optional[str] = ..., symbol: _Optional[str] = ..., constituent_nums: _Optional[int] = ..., suspension_nums: _Optional[int] = ..., up_limit_nums: _Optional[int] = ..., down_limit_nums: _Optional[int] = ..., iopv: _Optional[int] = ..., etf_premium_rate: _Optional[float] = ..., md_date: _Optional[int] = ..., md_time: _Optional[int] = ..., etf_last_price: _Optional[int] = ..., etf_bid_price: _Optional[int] = ..., etf_ask_price: _Optional[int] = ..., etf_pre_close_price: _Optional[int] = ..., etf_pct_change: _Optional[float] = ...) -> None: ...

class Fund(_message.Message):
    __slots__ = ["account_id", "available", "balance", "currency_id", "frozen", "intraday", "investor_id", "sod", "trans_in", "trans_out", "version"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
    FROZEN_FIELD_NUMBER: _ClassVar[int]
    INTRADAY_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    SOD_FIELD_NUMBER: _ClassVar[int]
    TRANS_IN_FIELD_NUMBER: _ClassVar[int]
    TRANS_OUT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    available: float
    balance: float
    currency_id: str
    frozen: float
    intraday: float
    investor_id: str
    sod: float
    trans_in: float
    trans_out: float
    version: int
    def __init__(self, account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., currency_id: _Optional[str] = ..., sod: _Optional[float] = ..., balance: _Optional[float] = ..., frozen: _Optional[float] = ..., available: _Optional[float] = ..., intraday: _Optional[float] = ..., trans_in: _Optional[float] = ..., trans_out: _Optional[float] = ..., version: _Optional[int] = ...) -> None: ...

class Instrument(_message.Message):
    __slots__ = ["chain_codes", "comments", "contract_unit", "delist_date", "fund_etfpr_estcash", "fund_etfpr_minnav", "instrument_id", "instrument_sub_type", "instrument_type", "intraday_open_limit", "intraday_trading", "is_replace_price", "is_sub", "is_withdraw", "list_date", "long_posi_limit", "lot_size", "market", "max_down", "max_size", "max_up", "min_size", "price_tick", "quote_currency_id", "replace_price", "security_id", "security_type", "settle_currency_id", "settle_date", "short_posi_limit", "symbol", "total_share", "underlying_instrument_id", "wind_market", "withdraw_basket_volume"]
    CHAIN_CODES_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    DELIST_DATE_FIELD_NUMBER: _ClassVar[int]
    FUND_ETFPR_ESTCASH_FIELD_NUMBER: _ClassVar[int]
    FUND_ETFPR_MINNAV_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_SUB_TYPE_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    INTRADAY_OPEN_LIMIT_FIELD_NUMBER: _ClassVar[int]
    INTRADAY_TRADING_FIELD_NUMBER: _ClassVar[int]
    IS_REPLACE_PRICE_FIELD_NUMBER: _ClassVar[int]
    IS_SUB_FIELD_NUMBER: _ClassVar[int]
    IS_WITHDRAW_FIELD_NUMBER: _ClassVar[int]
    LIST_DATE_FIELD_NUMBER: _ClassVar[int]
    LONG_POSI_LIMIT_FIELD_NUMBER: _ClassVar[int]
    LOT_SIZE_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MAX_DOWN_FIELD_NUMBER: _ClassVar[int]
    MAX_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_UP_FIELD_NUMBER: _ClassVar[int]
    MIN_SIZE_FIELD_NUMBER: _ClassVar[int]
    PRICE_TICK_FIELD_NUMBER: _ClassVar[int]
    QUOTE_CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
    REPLACE_PRICE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SETTLE_CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
    SETTLE_DATE_FIELD_NUMBER: _ClassVar[int]
    SHORT_POSI_LIMIT_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SHARE_FIELD_NUMBER: _ClassVar[int]
    UNDERLYING_INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    WIND_MARKET_FIELD_NUMBER: _ClassVar[int]
    WITHDRAW_BASKET_VOLUME_FIELD_NUMBER: _ClassVar[int]
    chain_codes: _containers.RepeatedScalarFieldContainer[str]
    comments: str
    contract_unit: float
    delist_date: str
    fund_etfpr_estcash: float
    fund_etfpr_minnav: int
    instrument_id: str
    instrument_sub_type: str
    instrument_type: str
    intraday_open_limit: int
    intraday_trading: int
    is_replace_price: int
    is_sub: int
    is_withdraw: int
    list_date: str
    long_posi_limit: int
    lot_size: int
    market: str
    max_down: float
    max_size: int
    max_up: float
    min_size: int
    price_tick: float
    quote_currency_id: str
    replace_price: float
    security_id: str
    security_type: str
    settle_currency_id: str
    settle_date: str
    short_posi_limit: int
    symbol: str
    total_share: int
    underlying_instrument_id: str
    wind_market: str
    withdraw_basket_volume: int
    def __init__(self, instrument_id: _Optional[str] = ..., market: _Optional[str] = ..., security_id: _Optional[str] = ..., symbol: _Optional[str] = ..., instrument_type: _Optional[str] = ..., security_type: _Optional[str] = ..., lot_size: _Optional[int] = ..., price_tick: _Optional[float] = ..., contract_unit: _Optional[float] = ..., intraday_trading: _Optional[int] = ..., is_sub: _Optional[int] = ..., is_withdraw: _Optional[int] = ..., fund_etfpr_minnav: _Optional[int] = ..., withdraw_basket_volume: _Optional[int] = ..., long_posi_limit: _Optional[int] = ..., short_posi_limit: _Optional[int] = ..., intraday_open_limit: _Optional[int] = ..., max_up: _Optional[float] = ..., max_down: _Optional[float] = ..., underlying_instrument_id: _Optional[str] = ..., chain_codes: _Optional[_Iterable[str]] = ..., fund_etfpr_estcash: _Optional[float] = ..., wind_market: _Optional[str] = ..., comments: _Optional[str] = ..., is_replace_price: _Optional[int] = ..., replace_price: _Optional[float] = ..., quote_currency_id: _Optional[str] = ..., settle_currency_id: _Optional[str] = ..., instrument_sub_type: _Optional[str] = ..., min_size: _Optional[int] = ..., max_size: _Optional[int] = ..., list_date: _Optional[str] = ..., delist_date: _Optional[str] = ..., settle_date: _Optional[str] = ..., total_share: _Optional[int] = ...) -> None: ...

class LoginReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "passwd", "request_id", "user_id"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PASSWD_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    passwd: str
    request_id: str
    user_id: str
    def __init__(self, msg_type: _Optional[int] = ..., user_id: _Optional[str] = ..., passwd: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class LoginRsp(_message.Message):
    __slots__ = ["error_msg", "is_succ", "last_timestamp", "msg_type", "request_id"]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    IS_SUCC_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    error_msg: str
    is_succ: bool
    last_timestamp: int
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., is_succ: bool = ..., error_msg: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class MDSnapshot(_message.Message):
    __slots__ = ["close_price", "depth_quote", "down_limit", "high_price", "instrument_id", "iopv", "last_price", "last_timestamp", "low_price", "market", "md_date", "md_time", "md_type", "msg_sequence", "msg_type", "open_price", "phase_code", "pre_close_price", "security_id", "security_type", "signal_id", "signal_name", "signal_value", "status", "trade_nums", "turnover", "up_limit", "volume"]
    CLOSE_PRICE_FIELD_NUMBER: _ClassVar[int]
    DEPTH_QUOTE_FIELD_NUMBER: _ClassVar[int]
    DOWN_LIMIT_FIELD_NUMBER: _ClassVar[int]
    HIGH_PRICE_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    IOPV_FIELD_NUMBER: _ClassVar[int]
    LAST_PRICE_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LOW_PRICE_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MD_DATE_FIELD_NUMBER: _ClassVar[int]
    MD_TIME_FIELD_NUMBER: _ClassVar[int]
    MD_TYPE_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPEN_PRICE_FIELD_NUMBER: _ClassVar[int]
    PHASE_CODE_FIELD_NUMBER: _ClassVar[int]
    PRE_CLOSE_PRICE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRADE_NUMS_FIELD_NUMBER: _ClassVar[int]
    TURNOVER_FIELD_NUMBER: _ClassVar[int]
    UP_LIMIT_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    close_price: int
    depth_quote: _containers.RepeatedCompositeFieldContainer[QuoteLevelData]
    down_limit: int
    high_price: int
    instrument_id: str
    iopv: int
    last_price: int
    last_timestamp: int
    low_price: int
    market: str
    md_date: int
    md_time: int
    md_type: int
    msg_sequence: int
    msg_type: int
    open_price: int
    phase_code: int
    pre_close_price: int
    security_id: str
    security_type: str
    signal_id: int
    signal_name: str
    signal_value: int
    status: int
    trade_nums: int
    turnover: int
    up_limit: int
    volume: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., instrument_id: _Optional[str] = ..., market: _Optional[str] = ..., security_id: _Optional[str] = ..., security_type: _Optional[str] = ..., md_date: _Optional[int] = ..., md_time: _Optional[int] = ..., md_type: _Optional[int] = ..., last_price: _Optional[int] = ..., volume: _Optional[int] = ..., turnover: _Optional[int] = ..., high_price: _Optional[int] = ..., low_price: _Optional[int] = ..., open_price: _Optional[int] = ..., close_price: _Optional[int] = ..., pre_close_price: _Optional[int] = ..., up_limit: _Optional[int] = ..., down_limit: _Optional[int] = ..., iopv: _Optional[int] = ..., trade_nums: _Optional[int] = ..., status: _Optional[int] = ..., phase_code: _Optional[int] = ..., signal_value: _Optional[int] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., depth_quote: _Optional[_Iterable[_Union[QuoteLevelData, _Mapping]]] = ...) -> None: ...

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

class ManagerSyncReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "request_id"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class ManagerSyncRsp(_message.Message):
    __slots__ = ["error_msg", "last_timestamp", "msg_type", "request_id", "status"]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error_msg: str
    last_timestamp: int
    msg_type: int
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., status: _Optional[int] = ..., error_msg: _Optional[str] = ...) -> None: ...

class NewBasketTemplateReq(_message.Message):
    __slots__ = ["basket_info_details", "msg_type", "request_id", "strategy_name", "template_id", "template_type"]
    BASKET_INFO_DETAILS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    basket_info_details: _containers.RepeatedCompositeFieldContainer[BasketInfoDetail]
    msg_type: int
    request_id: str
    strategy_name: str
    template_id: str
    template_type: str
    def __init__(self, msg_type: _Optional[int] = ..., template_id: _Optional[str] = ..., basket_info_details: _Optional[_Iterable[_Union[BasketInfoDetail, _Mapping]]] = ..., strategy_name: _Optional[str] = ..., request_id: _Optional[str] = ..., template_type: _Optional[str] = ...) -> None: ...

class NewBasketTemplateRsp(_message.Message):
    __slots__ = ["msg_type", "reason", "request_id", "status", "template_id", "template_type"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    reason: str
    request_id: str
    status: int
    template_id: str
    template_type: str
    def __init__(self, msg_type: _Optional[int] = ..., template_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., request_id: _Optional[str] = ..., template_type: _Optional[str] = ...) -> None: ...

class NewSignalParamsReq(_message.Message):
    __slots__ = ["instrument_id", "last_timestamp", "msg_type", "node_name", "package_info", "request_id", "signal_info_l2", "signal_name", "signal_params", "signal_template_id", "text"]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_INFO_L2_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    instrument_id: str
    last_timestamp: int
    msg_type: int
    node_name: str
    package_info: _containers.RepeatedCompositeFieldContainer[PackageInfo]
    request_id: str
    signal_info_l2: _containers.RepeatedCompositeFieldContainer[SignalInfoL2]
    signal_name: str
    signal_params: str
    signal_template_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., signal_name: _Optional[str] = ..., text: _Optional[str] = ..., signal_params: _Optional[str] = ..., signal_template_id: _Optional[str] = ..., package_info: _Optional[_Iterable[_Union[PackageInfo, _Mapping]]] = ..., signal_info_l2: _Optional[_Iterable[_Union[SignalInfoL2, _Mapping]]] = ..., node_name: _Optional[str] = ...) -> None: ...

class NewSignalParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "request_id", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    request_id: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class Node(_message.Message):
    __slots__ = ["comments", "data_center", "ip_address", "network_delay", "node_id", "node_name", "node_status", "node_type", "quote_id"]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    DATA_CENTER_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NETWORK_DELAY_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_STATUS_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ID_FIELD_NUMBER: _ClassVar[int]
    comments: str
    data_center: str
    ip_address: str
    network_delay: int
    node_id: int
    node_name: str
    node_status: str
    node_type: int
    quote_id: str
    def __init__(self, node_name: _Optional[str] = ..., data_center: _Optional[str] = ..., ip_address: _Optional[str] = ..., node_status: _Optional[str] = ..., comments: _Optional[str] = ..., network_delay: _Optional[int] = ..., quote_id: _Optional[str] = ..., node_id: _Optional[int] = ..., node_type: _Optional[int] = ...) -> None: ...

class Order(_message.Message):
    __slots__ = ["account_id", "algo_params", "algo_type", "appl_id", "attachment", "basket_id", "cancel_qty", "cancel_time", "cl_order_id", "contract_unit", "counter_order_id", "instrument_id", "investor_id", "is_pass", "is_pre_order", "market", "match_amt", "match_qty", "op_marks", "order_amt", "order_date", "order_id", "order_price", "order_qty", "order_source", "order_status", "order_time", "order_type", "owner_type", "parent_order_id", "position_effect", "purpose", "reject_qty", "reject_reason", "risk_info", "security_id", "security_type", "side", "strategy_id", "strategy_name", "symbol", "text", "time_in_force", "trigger_time", "user_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALGO_PARAMS_FIELD_NUMBER: _ClassVar[int]
    ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    BASKET_ID_FIELD_NUMBER: _ClassVar[int]
    CANCEL_QTY_FIELD_NUMBER: _ClassVar[int]
    CANCEL_TIME_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    COUNTER_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PASS_FIELD_NUMBER: _ClassVar[int]
    IS_PRE_ORDER_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MATCH_AMT_FIELD_NUMBER: _ClassVar[int]
    MATCH_QTY_FIELD_NUMBER: _ClassVar[int]
    OP_MARKS_FIELD_NUMBER: _ClassVar[int]
    ORDER_AMT_FIELD_NUMBER: _ClassVar[int]
    ORDER_DATE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_PRICE_FIELD_NUMBER: _ClassVar[int]
    ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    ORDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ORDER_STATUS_FIELD_NUMBER: _ClassVar[int]
    ORDER_TIME_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_EFFECT_FIELD_NUMBER: _ClassVar[int]
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    REJECT_QTY_FIELD_NUMBER: _ClassVar[int]
    REJECT_REASON_FIELD_NUMBER: _ClassVar[int]
    RISK_INFO_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    TIME_IN_FORCE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_TIME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    algo_params: AlgoParams
    algo_type: int
    appl_id: str
    attachment: str
    basket_id: str
    cancel_qty: int
    cancel_time: int
    cl_order_id: str
    contract_unit: float
    counter_order_id: str
    instrument_id: str
    investor_id: str
    is_pass: int
    is_pre_order: int
    market: str
    match_amt: float
    match_qty: int
    op_marks: str
    order_amt: float
    order_date: int
    order_id: str
    order_price: float
    order_qty: int
    order_source: str
    order_status: int
    order_time: int
    order_type: int
    owner_type: int
    parent_order_id: str
    position_effect: int
    purpose: int
    reject_qty: int
    reject_reason: int
    risk_info: str
    security_id: str
    security_type: str
    side: int
    strategy_id: int
    strategy_name: str
    symbol: str
    text: str
    time_in_force: int
    trigger_time: int
    user_id: str
    def __init__(self, order_id: _Optional[str] = ..., cl_order_id: _Optional[str] = ..., counter_order_id: _Optional[str] = ..., order_date: _Optional[int] = ..., order_time: _Optional[int] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., security_type: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., contract_unit: _Optional[float] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., order_type: _Optional[int] = ..., side: _Optional[int] = ..., position_effect: _Optional[int] = ..., time_in_force: _Optional[int] = ..., purpose: _Optional[int] = ..., order_qty: _Optional[int] = ..., order_price: _Optional[float] = ..., order_amt: _Optional[float] = ..., order_status: _Optional[int] = ..., match_qty: _Optional[int] = ..., match_amt: _Optional[float] = ..., cancel_qty: _Optional[int] = ..., reject_qty: _Optional[int] = ..., is_pass: _Optional[int] = ..., owner_type: _Optional[int] = ..., reject_reason: _Optional[int] = ..., text: _Optional[str] = ..., is_pre_order: _Optional[int] = ..., trigger_time: _Optional[int] = ..., parent_order_id: _Optional[str] = ..., algo_type: _Optional[int] = ..., algo_params: _Optional[_Union[AlgoParams, _Mapping]] = ..., order_source: _Optional[str] = ..., attachment: _Optional[str] = ..., cancel_time: _Optional[int] = ..., user_id: _Optional[str] = ..., risk_info: _Optional[str] = ..., op_marks: _Optional[str] = ..., symbol: _Optional[str] = ..., basket_id: _Optional[str] = ...) -> None: ...

class OrderConfirm(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "confirm_qty", "contract_unit", "counter_order_id", "instrument_id", "investor_id", "is_pass", "market", "msg_sequence", "msg_type", "order_id", "order_price", "reject_qty", "security_id", "strategy_id", "strategy_name"]
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
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_PRICE_FIELD_NUMBER: _ClassVar[int]
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
    order_id: str
    order_price: float
    reject_qty: int
    security_id: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., counter_order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., confirm_qty: _Optional[int] = ..., reject_qty: _Optional[int] = ..., is_pass: _Optional[int] = ..., order_price: _Optional[float] = ..., contract_unit: _Optional[float] = ...) -> None: ...

class OrderEvent(_message.Message):
    __slots__ = ["msg_sequence", "msg_type", "order"]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    msg_sequence: int
    msg_type: int
    order: Order
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., order: _Optional[_Union[Order, _Mapping]] = ...) -> None: ...

class OrderPendingConfirm(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "confirm_qty", "instrument_id", "investor_id", "is_pass", "market", "msg_sequence", "msg_type", "order_id", "reject_qty", "security_id", "strategy_id", "strategy_name"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_QTY_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PASS_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    REJECT_QTY_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    appl_id: str
    cl_order_id: str
    confirm_qty: int
    instrument_id: str
    investor_id: str
    is_pass: int
    market: str
    msg_sequence: int
    msg_type: int
    order_id: str
    reject_qty: int
    security_id: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., confirm_qty: _Optional[int] = ..., reject_qty: _Optional[int] = ..., is_pass: _Optional[int] = ...) -> None: ...

class OrderReject(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "contract_unit", "instrument_id", "investor_id", "is_pass", "market", "msg_sequence", "msg_type", "order_id", "order_price", "reject_qty", "reject_reason", "security_id", "strategy_id", "strategy_name", "text"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PASS_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    instrument_id: str
    investor_id: str
    is_pass: int
    market: str
    msg_sequence: int
    msg_type: int
    order_id: str
    order_price: float
    reject_qty: int
    reject_reason: int
    security_id: str
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., reject_reason: _Optional[int] = ..., text: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., reject_qty: _Optional[int] = ..., is_pass: _Optional[int] = ..., order_price: _Optional[float] = ..., contract_unit: _Optional[float] = ...) -> None: ...

class PackageInfo(_message.Message):
    __slots__ = ["component_instrument_id", "component_qty", "instrument_id", "is_sub_cash_replace", "is_sub_cash_replace_amount", "is_withdraw_cash", "is_withdraw_cash_replace_amount"]
    COMPONENT_INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_QTY_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    IS_SUB_CASH_REPLACE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    IS_SUB_CASH_REPLACE_FIELD_NUMBER: _ClassVar[int]
    IS_WITHDRAW_CASH_FIELD_NUMBER: _ClassVar[int]
    IS_WITHDRAW_CASH_REPLACE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    component_instrument_id: str
    component_qty: int
    instrument_id: str
    is_sub_cash_replace: int
    is_sub_cash_replace_amount: float
    is_withdraw_cash: int
    is_withdraw_cash_replace_amount: float
    def __init__(self, instrument_id: _Optional[str] = ..., component_instrument_id: _Optional[str] = ..., component_qty: _Optional[int] = ..., is_sub_cash_replace: _Optional[int] = ..., is_sub_cash_replace_amount: _Optional[float] = ..., is_withdraw_cash: _Optional[int] = ..., is_withdraw_cash_replace_amount: _Optional[float] = ...) -> None: ...

class Ping(_message.Message):
    __slots__ = ["msg_sequence", "msg_type"]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_sequence: int
    msg_type: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ...) -> None: ...

class PlaceArbitrageOrder(_message.Message):
    __slots__ = ["arbitrage_cl_order_id", "arbitrage_type", "leg_exec_seq", "legs", "msg_type", "order_source", "strategy_id", "strategy_name"]
    class Leg(_message.Message):
        __slots__ = ["algo_params", "algo_type", "leg_cl_order_id", "leg_id", "leg_type", "order_price", "order_qty", "order_type", "side", "target_process"]
        ALGO_PARAMS_FIELD_NUMBER: _ClassVar[int]
        ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
        LEG_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
        LEG_ID_FIELD_NUMBER: _ClassVar[int]
        LEG_TYPE_FIELD_NUMBER: _ClassVar[int]
        ORDER_PRICE_FIELD_NUMBER: _ClassVar[int]
        ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
        ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
        SIDE_FIELD_NUMBER: _ClassVar[int]
        TARGET_PROCESS_FIELD_NUMBER: _ClassVar[int]
        algo_params: AlgoParams
        algo_type: int
        leg_cl_order_id: str
        leg_id: str
        leg_type: str
        order_price: float
        order_qty: int
        order_type: int
        side: int
        target_process: float
        def __init__(self, leg_id: _Optional[str] = ..., leg_type: _Optional[str] = ..., order_qty: _Optional[int] = ..., side: _Optional[int] = ..., leg_cl_order_id: _Optional[str] = ..., algo_type: _Optional[int] = ..., algo_params: _Optional[_Union[AlgoParams, _Mapping]] = ..., order_type: _Optional[int] = ..., target_process: _Optional[float] = ..., order_price: _Optional[float] = ...) -> None: ...
    ARBITRAGE_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ARBITRAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LEGS_FIELD_NUMBER: _ClassVar[int]
    LEG_EXEC_SEQ_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    arbitrage_cl_order_id: str
    arbitrage_type: str
    leg_exec_seq: str
    legs: _containers.RepeatedCompositeFieldContainer[PlaceArbitrageOrder.Leg]
    msg_type: int
    order_source: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., arbitrage_cl_order_id: _Optional[str] = ..., arbitrage_type: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., order_source: _Optional[str] = ..., leg_exec_seq: _Optional[str] = ..., legs: _Optional[_Iterable[_Union[PlaceArbitrageOrder.Leg, _Mapping]]] = ...) -> None: ...

class PlaceArbitrageOrderRsp(_message.Message):
    __slots__ = ["arbitrage_cl_order_id", "msg_type", "order", "reason", "status"]
    ARBITRAGE_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    arbitrage_cl_order_id: str
    msg_type: int
    order: ArbitrageOrder
    reason: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., arbitrage_cl_order_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., order: _Optional[_Union[ArbitrageOrder, _Mapping]] = ...) -> None: ...

class PlaceBasketOrder(_message.Message):
    __slots__ = ["algo_params", "algo_type", "attachment", "basket_cl_order_id", "basket_qty", "msg_type", "order_source", "purpose", "side", "strategy_id", "template_id"]
    ALGO_PARAMS_FIELD_NUMBER: _ClassVar[int]
    ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    BASKET_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    BASKET_QTY_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    algo_params: AlgoParams
    algo_type: int
    attachment: str
    basket_cl_order_id: str
    basket_qty: int
    msg_type: int
    order_source: str
    purpose: int
    side: int
    strategy_id: int
    template_id: str
    def __init__(self, msg_type: _Optional[int] = ..., basket_cl_order_id: _Optional[str] = ..., template_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., side: _Optional[int] = ..., purpose: _Optional[int] = ..., basket_qty: _Optional[int] = ..., algo_type: _Optional[int] = ..., algo_params: _Optional[_Union[AlgoParams, _Mapping]] = ..., order_source: _Optional[str] = ..., attachment: _Optional[str] = ...) -> None: ...

class PlaceBasketOrderRsp(_message.Message):
    __slots__ = ["algo_params", "algo_type", "basket_amt", "basket_cl_order_id", "basket_id", "basket_qty", "create_time", "msg_type", "order_source", "process_amt", "process_qty", "reason", "side", "status", "strategy_id", "strategy_name", "template_id", "trade_amt"]
    ALGO_PARAMS_FIELD_NUMBER: _ClassVar[int]
    ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
    BASKET_AMT_FIELD_NUMBER: _ClassVar[int]
    BASKET_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    BASKET_ID_FIELD_NUMBER: _ClassVar[int]
    BASKET_QTY_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    PROCESS_AMT_FIELD_NUMBER: _ClassVar[int]
    PROCESS_QTY_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TRADE_AMT_FIELD_NUMBER: _ClassVar[int]
    algo_params: AlgoParams
    algo_type: int
    basket_amt: float
    basket_cl_order_id: str
    basket_id: str
    basket_qty: int
    create_time: int
    msg_type: int
    order_source: str
    process_amt: float
    process_qty: float
    reason: str
    side: int
    status: int
    strategy_id: int
    strategy_name: str
    template_id: str
    trade_amt: float
    def __init__(self, msg_type: _Optional[int] = ..., basket_cl_order_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., basket_id: _Optional[str] = ..., template_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., side: _Optional[int] = ..., basket_amt: _Optional[float] = ..., trade_amt: _Optional[float] = ..., basket_qty: _Optional[int] = ..., process_qty: _Optional[float] = ..., process_amt: _Optional[float] = ..., create_time: _Optional[int] = ..., algo_type: _Optional[int] = ..., algo_params: _Optional[_Union[AlgoParams, _Mapping]] = ..., order_source: _Optional[str] = ...) -> None: ...

class PlaceBatchOrder(_message.Message):
    __slots__ = ["account_id", "algo_params", "algo_type", "attachment", "basket_cl_order_id", "msg_type", "order_source", "orders", "strategy_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALGO_PARAMS_FIELD_NUMBER: _ClassVar[int]
    ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    BASKET_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    ORDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    algo_params: AlgoParams
    algo_type: int
    attachment: str
    basket_cl_order_id: str
    msg_type: int
    order_source: str
    orders: _containers.RepeatedCompositeFieldContainer[BasketInfoDetail]
    strategy_id: int
    def __init__(self, msg_type: _Optional[int] = ..., basket_cl_order_id: _Optional[str] = ..., orders: _Optional[_Iterable[_Union[BasketInfoDetail, _Mapping]]] = ..., strategy_id: _Optional[int] = ..., account_id: _Optional[str] = ..., algo_type: _Optional[int] = ..., algo_params: _Optional[_Union[AlgoParams, _Mapping]] = ..., order_source: _Optional[str] = ..., attachment: _Optional[str] = ...) -> None: ...

class PlaceBatchOrderRsp(_message.Message):
    __slots__ = ["basket_cl_order_id", "basket_id", "create_time", "msg_type", "reason", "status"]
    BASKET_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    BASKET_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    basket_cl_order_id: str
    basket_id: str
    create_time: int
    msg_type: int
    reason: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., basket_cl_order_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., basket_id: _Optional[str] = ..., create_time: _Optional[int] = ...) -> None: ...

class PlaceOrder(_message.Message):
    __slots__ = ["account_id", "algo_params", "algo_type", "attachment", "basket_id", "cl_order_id", "instrument_id", "investor_id", "is_pass", "is_pre_order", "msg_type", "order_price", "order_qty", "order_source", "order_type", "owner_type", "parent_order_id", "position_effect", "purpose", "side", "stop_px", "strategy_id", "strategy_name", "time_in_force", "trigger_time"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALGO_PARAMS_FIELD_NUMBER: _ClassVar[int]
    ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    BASKET_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PASS_FIELD_NUMBER: _ClassVar[int]
    IS_PRE_ORDER_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_PRICE_FIELD_NUMBER: _ClassVar[int]
    ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    ORDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_EFFECT_FIELD_NUMBER: _ClassVar[int]
    PURPOSE_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STOP_PX_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TIME_IN_FORCE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_TIME_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    algo_params: AlgoParams
    algo_type: int
    attachment: str
    basket_id: str
    cl_order_id: str
    instrument_id: str
    investor_id: str
    is_pass: int
    is_pre_order: int
    msg_type: int
    order_price: float
    order_qty: int
    order_source: str
    order_type: int
    owner_type: int
    parent_order_id: str
    position_effect: int
    purpose: int
    side: int
    stop_px: float
    strategy_id: int
    strategy_name: str
    time_in_force: int
    trigger_time: int
    def __init__(self, msg_type: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., is_pre_order: _Optional[int] = ..., trigger_time: _Optional[int] = ..., order_type: _Optional[int] = ..., side: _Optional[int] = ..., position_effect: _Optional[int] = ..., time_in_force: _Optional[int] = ..., purpose: _Optional[int] = ..., stop_px: _Optional[float] = ..., order_price: _Optional[float] = ..., order_qty: _Optional[int] = ..., is_pass: _Optional[int] = ..., owner_type: _Optional[int] = ..., algo_type: _Optional[int] = ..., algo_params: _Optional[_Union[AlgoParams, _Mapping]] = ..., order_source: _Optional[str] = ..., attachment: _Optional[str] = ..., parent_order_id: _Optional[str] = ..., basket_id: _Optional[str] = ...) -> None: ...

class Pong(_message.Message):
    __slots__ = ["msg_sequence", "msg_type"]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_sequence: int
    msg_type: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ...) -> None: ...

class Position(_message.Message):
    __slots__ = ["account_id", "apply_avl", "available", "balance", "buy_in", "cost_price", "frozen", "instrument_id", "investor_id", "last_price", "market", "market_value", "posi_side", "realized_pnl", "security_id", "security_type", "sell_out", "sod", "symbol", "trans_avl", "trans_in", "trans_out", "version"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPLY_AVL_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    BUY_IN_FIELD_NUMBER: _ClassVar[int]
    COST_PRICE_FIELD_NUMBER: _ClassVar[int]
    FROZEN_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_PRICE_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MARKET_VALUE_FIELD_NUMBER: _ClassVar[int]
    POSI_SIDE_FIELD_NUMBER: _ClassVar[int]
    REALIZED_PNL_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SELL_OUT_FIELD_NUMBER: _ClassVar[int]
    SOD_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TRANS_AVL_FIELD_NUMBER: _ClassVar[int]
    TRANS_IN_FIELD_NUMBER: _ClassVar[int]
    TRANS_OUT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    apply_avl: int
    available: int
    balance: int
    buy_in: int
    cost_price: float
    frozen: int
    instrument_id: str
    investor_id: str
    last_price: float
    market: str
    market_value: float
    posi_side: int
    realized_pnl: float
    security_id: str
    security_type: str
    sell_out: int
    sod: int
    symbol: str
    trans_avl: int
    trans_in: int
    trans_out: int
    version: int
    def __init__(self, account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., market: _Optional[str] = ..., security_id: _Optional[str] = ..., security_type: _Optional[str] = ..., symbol: _Optional[str] = ..., posi_side: _Optional[int] = ..., instrument_id: _Optional[str] = ..., sod: _Optional[int] = ..., balance: _Optional[int] = ..., available: _Optional[int] = ..., frozen: _Optional[int] = ..., buy_in: _Optional[int] = ..., sell_out: _Optional[int] = ..., trans_in: _Optional[int] = ..., trans_out: _Optional[int] = ..., trans_avl: _Optional[int] = ..., apply_avl: _Optional[int] = ..., cost_price: _Optional[float] = ..., realized_pnl: _Optional[float] = ..., version: _Optional[int] = ..., last_price: _Optional[float] = ..., market_value: _Optional[float] = ...) -> None: ...

class PositionQty(_message.Message):
    __slots__ = ["qty", "type"]
    QTY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    qty: int
    type: PosType
    def __init__(self, type: _Optional[_Union[PosType, str]] = ..., qty: _Optional[int] = ...) -> None: ...

class PositionReport(_message.Message):
    __slots__ = ["account_id", "available", "balance", "cost_price", "investor_id", "is_last", "market", "msg_sequence", "msg_type", "node_name", "pos_account_type", "pos_qty", "pos_req_type", "pos_rpt_id", "posi_side", "realized_pnl", "request_id", "security_id", "security_type", "status", "symbol", "text", "version"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    COST_PRICE_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
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
    cost_price: int
    investor_id: str
    is_last: bool
    market: str
    msg_sequence: int
    msg_type: int
    node_name: str
    pos_account_type: PosAccountType
    pos_qty: _containers.RepeatedCompositeFieldContainer[PositionQty]
    pos_req_type: PosReqType
    pos_rpt_id: str
    posi_side: int
    realized_pnl: int
    request_id: str
    security_id: str
    security_type: str
    status: int
    symbol: str
    text: str
    version: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., node_name: _Optional[str] = ..., request_id: _Optional[str] = ..., pos_req_type: _Optional[_Union[PosReqType, str]] = ..., pos_account_type: _Optional[_Union[PosAccountType, str]] = ..., pos_rpt_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., is_last: bool = ..., version: _Optional[int] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., market: _Optional[str] = ..., security_id: _Optional[str] = ..., balance: _Optional[int] = ..., available: _Optional[int] = ..., cost_price: _Optional[int] = ..., realized_pnl: _Optional[int] = ..., symbol: _Optional[str] = ..., security_type: _Optional[str] = ..., posi_side: _Optional[int] = ..., pos_qty: _Optional[_Iterable[_Union[PositionQty, _Mapping]]] = ...) -> None: ...

class QryArbitrageOrderReq(_message.Message):
    __slots__ = ["msg_type", "request_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryArbitrageOrderRsp(_message.Message):
    __slots__ = ["msg_type", "reason", "request_id", "status"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryBasketInfoReq(_message.Message):
    __slots__ = ["msg_type", "request_id", "template_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    request_id: str
    template_id: str
    def __init__(self, msg_type: _Optional[int] = ..., template_id: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryBasketInfoRsp(_message.Message):
    __slots__ = ["basket_infos", "msg_type", "request_id"]
    BASKET_INFOS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    basket_infos: _containers.RepeatedCompositeFieldContainer[BasketInfo]
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., basket_infos: _Optional[_Iterable[_Union[BasketInfo, _Mapping]]] = ...) -> None: ...

class QryBasketOrderReq(_message.Message):
    __slots__ = ["msg_type", "request_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryBasketOrderRsp(_message.Message):
    __slots__ = ["msg_type", "reason", "request_id", "status"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryBasketOrderStatReq(_message.Message):
    __slots__ = ["basket_cl_order_id", "msg_type", "request_id"]
    BASKET_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    basket_cl_order_id: str
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., basket_cl_order_id: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryBasketOrderStatRsp(_message.Message):
    __slots__ = ["basket_cl_order_id", "basket_order_stats", "msg_type", "reason", "request_id", "status"]
    BASKET_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    BASKET_ORDER_STATS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    basket_cl_order_id: str
    basket_order_stats: _containers.RepeatedCompositeFieldContainer[BasketOrderStat]
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., basket_cl_order_id: _Optional[str] = ..., basket_order_stats: _Optional[_Iterable[_Union[BasketOrderStat, _Mapping]]] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ...) -> None: ...

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
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    books: _containers.RepeatedCompositeFieldContainer[Book]
    msg_type: int
    request_id: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., books: _Optional[_Iterable[_Union[Book, _Mapping]]] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class QryBrokerFundReq(_message.Message):
    __slots__ = ["account_id", "msg_type", "node_name", "node_type", "page_size", "request_id", "start_row"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    msg_type: int
    node_name: str
    node_type: int
    page_size: int
    request_id: str
    start_row: int
    def __init__(self, msg_type: _Optional[int] = ..., node_type: _Optional[int] = ..., node_name: _Optional[str] = ..., account_id: _Optional[str] = ..., request_id: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class QryBrokerFundRsp(_message.Message):
    __slots__ = ["fund", "is_last", "last_timestamp", "msg_sequence", "msg_type", "node_name", "node_type", "page_size", "reason", "request_id", "start_row", "status", "total_row"]
    FUND_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
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
    fund: _containers.RepeatedCompositeFieldContainer[Fund]
    is_last: bool
    last_timestamp: int
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
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., fund: _Optional[_Iterable[_Union[Fund, _Mapping]]] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class QryBrokerPosiReq(_message.Message):
    __slots__ = ["account_id", "msg_type", "page_size", "request_id", "start_row"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    msg_type: int
    page_size: int
    request_id: str
    start_row: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., account_id: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class QryBrokerPosiRsp(_message.Message):
    __slots__ = ["is_last", "last_timestamp", "msg_sequence", "msg_type", "node_name", "node_type", "page_size", "position", "reason", "request_id", "start_row", "status", "total_row"]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
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
    last_timestamp: int
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    page_size: int
    position: _containers.RepeatedCompositeFieldContainer[Position]
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., position: _Optional[_Iterable[_Union[Position, _Mapping]]] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class QryCurrencyReq(_message.Message):
    __slots__ = ["msg_type", "request_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryCurrencyRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "reason", "request_id", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[Currency]
    is_last: bool
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[Currency, _Mapping]]] = ...) -> None: ...

class QryFundReq(_message.Message):
    __slots__ = ["msg_type", "node_name", "node_type", "page_size", "request_id", "start_row"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    node_name: str
    node_type: int
    page_size: int
    request_id: str
    start_row: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class QryFundRsp(_message.Message):
    __slots__ = ["fund", "is_last", "msg_type", "page_size", "reason", "request_id", "start_row", "status", "total_row"]
    FUND_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_ROW_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ROW_FIELD_NUMBER: _ClassVar[int]
    fund: _containers.RepeatedCompositeFieldContainer[Fund]
    is_last: bool
    msg_type: int
    page_size: int
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., fund: _Optional[_Iterable[_Union[Fund, _Mapping]]] = ...) -> None: ...

class QryInstrumentReq(_message.Message):
    __slots__ = ["basket_instrument_id", "instrument_id", "msg_type", "request_id"]
    BASKET_INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    basket_instrument_id: str
    instrument_id: str
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., basket_instrument_id: _Optional[str] = ...) -> None: ...

class QryInstrumentRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "reason", "request_id", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[Instrument]
    is_last: bool
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[Instrument, _Mapping]]] = ...) -> None: ...

class QryNodeReq(_message.Message):
    __slots__ = ["msg_type", "request_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryNodeRsp(_message.Message):
    __slots__ = ["msg_type", "nodes", "reason", "request_id", "status"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    nodes: _containers.RepeatedCompositeFieldContainer[Node]
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., nodes: _Optional[_Iterable[_Union[Node, _Mapping]]] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryOrdersReq(_message.Message):
    __slots__ = ["account_id", "cl_order_id", "instrument_id", "is_active", "msg_sequence", "msg_type", "order_id", "owner_type", "page_size", "request_id", "start_row", "strategy_id", "token"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    order_id: str
    owner_type: int
    page_size: int
    request_id: str
    start_row: int
    strategy_id: int
    token: str
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., token: _Optional[str] = ..., request_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., account_id: _Optional[str] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., is_active: _Optional[int] = ..., owner_type: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class QryOrdersRsp(_message.Message):
    __slots__ = ["is_last", "msg_sequence", "msg_type", "order", "page_size", "reason", "request_id", "start_row", "status", "total_row"]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    order: _containers.RepeatedCompositeFieldContainer[Order]
    page_size: int
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., order: _Optional[_Iterable[_Union[Order, _Mapping]]] = ...) -> None: ...

class QryPosiReq(_message.Message):
    __slots__ = ["account_id", "market", "msg_type", "node_name", "node_type", "request_id", "security_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    market: str
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    security_id: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., account_id: _Optional[str] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ...) -> None: ...

class QryPosiRsp(_message.Message):
    __slots__ = ["is_last", "msg_sequence", "msg_type", "page_size", "position", "reason", "request_id", "start_row", "status", "total_row"]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    page_size: int
    position: _containers.RepeatedCompositeFieldContainer[Position]
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., position: _Optional[_Iterable[_Union[Position, _Mapping]]] = ...) -> None: ...

class QryQuoteInstanceReq(_message.Message):
    __slots__ = ["msg_type", "request_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryQuoteInstanceRsp(_message.Message):
    __slots__ = ["msg_type", "quote_instances", "reason", "request_id", "status"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUOTE_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    quote_instances: _containers.RepeatedCompositeFieldContainer[QuoteInstance]
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., quote_instances: _Optional[_Iterable[_Union[QuoteInstance, _Mapping]]] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryRiskItemReq(_message.Message):
    __slots__ = ["account_id", "instrument_id", "msg_type", "request_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: _containers.RepeatedScalarFieldContainer[str]
    instrument_id: _containers.RepeatedScalarFieldContainer[str]
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., account_id: _Optional[_Iterable[str]] = ..., instrument_id: _Optional[_Iterable[str]] = ...) -> None: ...

class QryRiskItemRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "reason", "request_id", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[RiskItem]
    is_last: bool
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[RiskItem, _Mapping]]] = ...) -> None: ...

class QryRiskMarketParamsReq(_message.Message):
    __slots__ = ["account_id", "market", "msg_type", "request_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: _containers.RepeatedScalarFieldContainer[str]
    market: _containers.RepeatedScalarFieldContainer[str]
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., account_id: _Optional[_Iterable[str]] = ..., market: _Optional[_Iterable[str]] = ...) -> None: ...

class QryRiskMarketParamsRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "reason", "request_id", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[RiskMarketParams]
    is_last: bool
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[RiskMarketParams, _Mapping]]] = ...) -> None: ...

class QrySignalInfoReq(_message.Message):
    __slots__ = ["msg_type", "request_id", "signal_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    request_id: str
    signal_id: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., signal_id: _Optional[int] = ...) -> None: ...

class QrySignalInfoRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "reason", "request_id", "status"]
    class SignalInfoData(_message.Message):
        __slots__ = ["global_params", "global_params_schema", "params_schema", "signal_list", "signal_template_id", "signal_template_type"]
        GLOBAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
        GLOBAL_PARAMS_SCHEMA_FIELD_NUMBER: _ClassVar[int]
        PARAMS_SCHEMA_FIELD_NUMBER: _ClassVar[int]
        SIGNAL_LIST_FIELD_NUMBER: _ClassVar[int]
        SIGNAL_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
        SIGNAL_TEMPLATE_TYPE_FIELD_NUMBER: _ClassVar[int]
        global_params: str
        global_params_schema: str
        params_schema: str
        signal_list: _containers.RepeatedCompositeFieldContainer[SignalInfo]
        signal_template_id: str
        signal_template_type: str
        def __init__(self, signal_template_id: _Optional[str] = ..., global_params: _Optional[str] = ..., signal_list: _Optional[_Iterable[_Union[SignalInfo, _Mapping]]] = ..., signal_template_type: _Optional[str] = ..., params_schema: _Optional[str] = ..., global_params_schema: _Optional[str] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[QrySignalInfoRsp.SignalInfoData]
    is_last: bool
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[QrySignalInfoRsp.SignalInfoData, _Mapping]]] = ...) -> None: ...

class QrySignalKlineReq(_message.Message):
    __slots__ = ["msg_type", "request_id", "signal_id", "start_date"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    request_id: str
    signal_id: int
    start_date: str
    def __init__(self, msg_type: _Optional[int] = ..., signal_id: _Optional[int] = ..., start_date: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class QrySignalKlineRsp(_message.Message):
    __slots__ = ["data", "is_last", "last_timestamp", "msg_type", "reason", "request_id", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[MDSnapshot]
    is_last: bool
    last_timestamp: int
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., data: _Optional[_Iterable[_Union[MDSnapshot, _Mapping]]] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class QrySignalStatReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "request_id", "signal_id"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    signal_id: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., signal_id: _Optional[int] = ...) -> None: ...

class QrySignalStatRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "request_id", "signal_stat"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_STAT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    signal_stat: _containers.RepeatedCompositeFieldContainer[SignalStatDetail]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., signal_stat: _Optional[_Iterable[_Union[SignalStatDetail, _Mapping]]] = ...) -> None: ...

class QryStrategyInfoReq(_message.Message):
    __slots__ = ["msg_type", "node_name", "request_id", "strategy_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    node_name: str
    request_id: str
    strategy_id: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., request_id: _Optional[str] = ..., strategy_id: _Optional[int] = ...) -> None: ...

class QryStrategyInfoRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "reason", "request_id", "status"]
    class StrategyInfoData(_message.Message):
        __slots__ = ["global_params", "global_params_schema", "monitor_params_schema", "params_schema", "strategy_list", "strategy_template_id"]
        GLOBAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
        GLOBAL_PARAMS_SCHEMA_FIELD_NUMBER: _ClassVar[int]
        MONITOR_PARAMS_SCHEMA_FIELD_NUMBER: _ClassVar[int]
        PARAMS_SCHEMA_FIELD_NUMBER: _ClassVar[int]
        STRATEGY_LIST_FIELD_NUMBER: _ClassVar[int]
        STRATEGY_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
        global_params: str
        global_params_schema: str
        monitor_params_schema: str
        params_schema: str
        strategy_list: _containers.RepeatedCompositeFieldContainer[StrategyInfo]
        strategy_template_id: str
        def __init__(self, strategy_template_id: _Optional[str] = ..., global_params: _Optional[str] = ..., strategy_list: _Optional[_Iterable[_Union[StrategyInfo, _Mapping]]] = ..., params_schema: _Optional[str] = ..., global_params_schema: _Optional[str] = ..., monitor_params_schema: _Optional[str] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[QryStrategyInfoRsp.StrategyInfoData]
    is_last: bool
    msg_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[QryStrategyInfoRsp.StrategyInfoData, _Mapping]]] = ...) -> None: ...

class QryStrategyLogReq(_message.Message):
    __slots__ = ["msg_type", "request_id", "start_time"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    request_id: str
    start_time: int
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., start_time: _Optional[int] = ...) -> None: ...

class QryStrategyLogRsp(_message.Message):
    __slots__ = ["is_last", "logs", "msg_type", "request_id", "status", "text"]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    is_last: bool
    logs: _containers.RepeatedCompositeFieldContainer[StrategyLogEvent]
    msg_type: int
    request_id: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., logs: _Optional[_Iterable[_Union[StrategyLogEvent, _Mapping]]] = ..., is_last: bool = ...) -> None: ...

class QryStrategyPositionReq(_message.Message):
    __slots__ = ["book_id", "msg_type", "request_id"]
    BOOK_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    book_id: str
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., book_id: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryStrategyPositionRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "reason", "request_id", "status", "strategy_positions"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    reason: str
    request_id: str
    status: int
    strategy_positions: _containers.RepeatedCompositeFieldContainer[StrategyPosition]
    def __init__(self, msg_type: _Optional[int] = ..., strategy_positions: _Optional[_Iterable[_Union[StrategyPosition, _Mapping]]] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class QryStrategyStatReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "request_id", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    request_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., text: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryStrategyStatRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "request_id", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    request_id: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class QryTradesReq(_message.Message):
    __slots__ = ["account_id", "appl_id", "cl_order_id", "instrument_id", "is_active", "market", "msg_sequence", "msg_type", "order_id", "page_size", "request_id", "security_id", "start_row", "strategy_id", "strategy_name", "token"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    order_id: str
    page_size: int
    request_id: str
    security_id: str
    start_row: int
    strategy_id: int
    strategy_name: str
    token: str
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., token: _Optional[str] = ..., request_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., is_active: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ...) -> None: ...

class QryTradesRsp(_message.Message):
    __slots__ = ["is_last", "msg_sequence", "msg_type", "page_size", "reason", "request_id", "start_row", "status", "total_row", "trade"]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    page_size: int
    reason: str
    request_id: str
    start_row: int
    status: int
    total_row: int
    trade: _containers.RepeatedCompositeFieldContainer[Trade]
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., request_id: _Optional[str] = ..., total_row: _Optional[int] = ..., start_row: _Optional[int] = ..., page_size: _Optional[int] = ..., is_last: bool = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., trade: _Optional[_Iterable[_Union[Trade, _Mapping]]] = ...) -> None: ...

class QuoteInstance(_message.Message):
    __slots__ = ["comments", "data_center", "ip_address", "node_status", "quote_id", "quote_type"]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    DATA_CENTER_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NODE_STATUS_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ID_FIELD_NUMBER: _ClassVar[int]
    QUOTE_TYPE_FIELD_NUMBER: _ClassVar[int]
    comments: str
    data_center: str
    ip_address: str
    node_status: str
    quote_id: str
    quote_type: str
    def __init__(self, quote_id: _Optional[str] = ..., quote_type: _Optional[str] = ..., ip_address: _Optional[str] = ..., comments: _Optional[str] = ..., data_center: _Optional[str] = ..., node_status: _Optional[str] = ...) -> None: ...

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

class RCParam(_message.Message):
    __slots__ = ["account_id", "buy_active_amt", "buy_active_qty", "buy_cancel_num", "buy_order_amt", "buy_order_num", "buy_order_qty", "buy_trade_amt", "buy_trade_qty", "instrument_id", "last_timestamp", "market", "msg_sequence", "msg_type", "security_id", "sell_active_amt", "sell_active_qty", "sell_cancel_num", "sell_order_amt", "sell_order_num", "sell_order_qty", "sell_trade_amt", "sell_trade_qty"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BUY_ACTIVE_AMT_FIELD_NUMBER: _ClassVar[int]
    BUY_ACTIVE_QTY_FIELD_NUMBER: _ClassVar[int]
    BUY_CANCEL_NUM_FIELD_NUMBER: _ClassVar[int]
    BUY_ORDER_AMT_FIELD_NUMBER: _ClassVar[int]
    BUY_ORDER_NUM_FIELD_NUMBER: _ClassVar[int]
    BUY_ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    BUY_TRADE_AMT_FIELD_NUMBER: _ClassVar[int]
    BUY_TRADE_QTY_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SELL_ACTIVE_AMT_FIELD_NUMBER: _ClassVar[int]
    SELL_ACTIVE_QTY_FIELD_NUMBER: _ClassVar[int]
    SELL_CANCEL_NUM_FIELD_NUMBER: _ClassVar[int]
    SELL_ORDER_AMT_FIELD_NUMBER: _ClassVar[int]
    SELL_ORDER_NUM_FIELD_NUMBER: _ClassVar[int]
    SELL_ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    SELL_TRADE_AMT_FIELD_NUMBER: _ClassVar[int]
    SELL_TRADE_QTY_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    buy_active_amt: float
    buy_active_qty: int
    buy_cancel_num: int
    buy_order_amt: float
    buy_order_num: int
    buy_order_qty: int
    buy_trade_amt: float
    buy_trade_qty: int
    instrument_id: str
    last_timestamp: int
    market: str
    msg_sequence: int
    msg_type: int
    security_id: str
    sell_active_amt: float
    sell_active_qty: int
    sell_cancel_num: int
    sell_order_amt: float
    sell_order_num: int
    sell_order_qty: int
    sell_trade_amt: float
    sell_trade_qty: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., account_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., market: _Optional[str] = ..., security_id: _Optional[str] = ..., buy_order_num: _Optional[int] = ..., sell_order_num: _Optional[int] = ..., buy_cancel_num: _Optional[int] = ..., sell_cancel_num: _Optional[int] = ..., buy_order_qty: _Optional[int] = ..., sell_order_qty: _Optional[int] = ..., buy_order_amt: _Optional[float] = ..., sell_order_amt: _Optional[float] = ..., buy_active_qty: _Optional[int] = ..., sell_active_qty: _Optional[int] = ..., buy_active_amt: _Optional[float] = ..., sell_active_amt: _Optional[float] = ..., buy_trade_qty: _Optional[int] = ..., sell_trade_qty: _Optional[int] = ..., buy_trade_amt: _Optional[float] = ..., sell_trade_amt: _Optional[float] = ...) -> None: ...

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

class RiskItem(_message.Message):
    __slots__ = ["account_id", "best_price_deviation", "fund_available", "instrument_id", "last_price_deviation", "long_posi_qty_up", "posi_concentration", "prev_price_deviation", "short_posi_qty_up", "single_order_qty", "status", "symbol", "total_buy_active_qty", "total_buy_order_amt", "total_buy_order_nums", "total_buy_order_qty", "total_buy_trade_amt", "total_buy_trade_qty", "total_sell_active_qty", "total_sell_order_amt", "total_sell_order_nums", "total_sell_order_qty", "total_sell_trade_amt", "total_sell_trade_qty", "warning_ratio"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BEST_PRICE_DEVIATION_FIELD_NUMBER: _ClassVar[int]
    FUND_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_PRICE_DEVIATION_FIELD_NUMBER: _ClassVar[int]
    LONG_POSI_QTY_UP_FIELD_NUMBER: _ClassVar[int]
    POSI_CONCENTRATION_FIELD_NUMBER: _ClassVar[int]
    PREV_PRICE_DEVIATION_FIELD_NUMBER: _ClassVar[int]
    SHORT_POSI_QTY_UP_FIELD_NUMBER: _ClassVar[int]
    SINGLE_ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BUY_ACTIVE_QTY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BUY_ORDER_AMT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BUY_ORDER_NUMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BUY_ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BUY_TRADE_AMT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BUY_TRADE_QTY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SELL_ACTIVE_QTY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SELL_ORDER_AMT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SELL_ORDER_NUMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SELL_ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SELL_TRADE_AMT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SELL_TRADE_QTY_FIELD_NUMBER: _ClassVar[int]
    WARNING_RATIO_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    best_price_deviation: float
    fund_available: float
    instrument_id: str
    last_price_deviation: float
    long_posi_qty_up: int
    posi_concentration: float
    prev_price_deviation: float
    short_posi_qty_up: int
    single_order_qty: int
    status: int
    symbol: str
    total_buy_active_qty: int
    total_buy_order_amt: float
    total_buy_order_nums: int
    total_buy_order_qty: int
    total_buy_trade_amt: float
    total_buy_trade_qty: int
    total_sell_active_qty: int
    total_sell_order_amt: float
    total_sell_order_nums: int
    total_sell_order_qty: int
    total_sell_trade_amt: float
    total_sell_trade_qty: int
    warning_ratio: float
    def __init__(self, account_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., status: _Optional[int] = ..., symbol: _Optional[str] = ..., single_order_qty: _Optional[int] = ..., long_posi_qty_up: _Optional[int] = ..., short_posi_qty_up: _Optional[int] = ..., prev_price_deviation: _Optional[float] = ..., last_price_deviation: _Optional[float] = ..., best_price_deviation: _Optional[float] = ..., posi_concentration: _Optional[float] = ..., fund_available: _Optional[float] = ..., total_buy_order_qty: _Optional[int] = ..., total_sell_order_qty: _Optional[int] = ..., total_buy_order_amt: _Optional[float] = ..., total_sell_order_amt: _Optional[float] = ..., total_buy_trade_qty: _Optional[int] = ..., total_sell_trade_qty: _Optional[int] = ..., total_buy_trade_amt: _Optional[float] = ..., total_sell_trade_amt: _Optional[float] = ..., total_buy_active_qty: _Optional[int] = ..., total_sell_active_qty: _Optional[int] = ..., total_buy_order_nums: _Optional[int] = ..., total_sell_order_nums: _Optional[int] = ..., warning_ratio: _Optional[float] = ...) -> None: ...

class RiskMarketParams(_message.Message):
    __slots__ = ["account_id", "comments", "control_point", "control_type", "create_by", "create_time", "market", "params", "risk_code", "risk_name", "set_value", "status", "update_by", "update_time"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
    CONTROL_TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATE_BY_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    RISK_CODE_FIELD_NUMBER: _ClassVar[int]
    RISK_NAME_FIELD_NUMBER: _ClassVar[int]
    SET_VALUE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    comments: str
    control_point: str
    control_type: str
    create_by: str
    create_time: str
    market: str
    params: str
    risk_code: str
    risk_name: str
    set_value: float
    status: int
    update_by: str
    update_time: str
    def __init__(self, account_id: _Optional[str] = ..., market: _Optional[str] = ..., risk_code: _Optional[str] = ..., risk_name: _Optional[str] = ..., control_type: _Optional[str] = ..., control_point: _Optional[str] = ..., status: _Optional[int] = ..., set_value: _Optional[float] = ..., params: _Optional[str] = ..., comments: _Optional[str] = ..., create_by: _Optional[str] = ..., update_by: _Optional[str] = ..., create_time: _Optional[str] = ..., update_time: _Optional[str] = ...) -> None: ...

class SaveStrategyParamsToDefaultReq(_message.Message):
    __slots__ = ["msg_type", "request_id", "strategy_id_list"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    request_id: str
    strategy_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., strategy_id_list: _Optional[_Iterable[int]] = ...) -> None: ...

class SaveStrategyParamsToDefaultRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "request_id", "status", "strategy_id_list", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    request_id: str
    status: int
    strategy_id_list: _containers.RepeatedScalarFieldContainer[int]
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., request_id: _Optional[str] = ..., strategy_id_list: _Optional[_Iterable[int]] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class SignalControlReq(_message.Message):
    __slots__ = ["control_type", "last_timestamp", "msg_type", "operate_type", "request_id", "signal_id", "signal_name"]
    class ControlType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CONTROL_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    control_type: SignalControlReq.ControlType
    kClose: SignalControlReq.ControlType
    kInit: SignalControlReq.ControlType
    kPause: SignalControlReq.ControlType
    kRun: SignalControlReq.ControlType
    kStop: SignalControlReq.ControlType
    last_timestamp: int
    msg_type: int
    operate_type: int
    request_id: str
    signal_id: int
    signal_name: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[int] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., control_type: _Optional[_Union[SignalControlReq.ControlType, str]] = ...) -> None: ...

class SignalControlRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "request_id", "signal_id", "signal_name", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    signal_id: int
    signal_name: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., signal_name: _Optional[str] = ..., signal_id: _Optional[int] = ..., status: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class SignalInfo(_message.Message):
    __slots__ = ["comment", "fund_etfpr_estcash", "fund_etfpr_minnav", "instrument_id", "instrument_type", "market", "node_id", "node_name", "package_info", "params", "security_id", "signal_id", "signal_info_l2", "signal_name", "status", "trade_date"]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    FUND_ETFPR_ESTCASH_FIELD_NUMBER: _ClassVar[int]
    FUND_ETFPR_MINNAV_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_INFO_L2_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRADE_DATE_FIELD_NUMBER: _ClassVar[int]
    comment: str
    fund_etfpr_estcash: float
    fund_etfpr_minnav: float
    instrument_id: str
    instrument_type: str
    market: str
    node_id: int
    node_name: str
    package_info: _containers.RepeatedCompositeFieldContainer[PackageInfo]
    params: str
    security_id: str
    signal_id: int
    signal_info_l2: _containers.RepeatedCompositeFieldContainer[SignalInfoL2]
    signal_name: str
    status: str
    trade_date: str
    def __init__(self, signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., instrument_id: _Optional[str] = ..., instrument_type: _Optional[str] = ..., market: _Optional[str] = ..., security_id: _Optional[str] = ..., status: _Optional[str] = ..., comment: _Optional[str] = ..., node_id: _Optional[int] = ..., node_name: _Optional[str] = ..., trade_date: _Optional[str] = ..., fund_etfpr_minnav: _Optional[float] = ..., fund_etfpr_estcash: _Optional[float] = ..., params: _Optional[str] = ..., package_info: _Optional[_Iterable[_Union[PackageInfo, _Mapping]]] = ..., signal_info_l2: _Optional[_Iterable[_Union[SignalInfoL2, _Mapping]]] = ...) -> None: ...

class SignalInfoL2(_message.Message):
    __slots__ = ["comments", "l2_signal_id", "l2_signal_name", "source_signal_id", "source_signal_name", "weight"]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    L2_SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    L2_SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    comments: str
    l2_signal_id: int
    l2_signal_name: str
    source_signal_id: int
    source_signal_name: str
    weight: float
    def __init__(self, l2_signal_id: _Optional[int] = ..., source_signal_id: _Optional[int] = ..., l2_signal_name: _Optional[str] = ..., comments: _Optional[str] = ..., weight: _Optional[float] = ..., source_signal_name: _Optional[str] = ...) -> None: ...

class SignalQuoteData(_message.Message):
    __slots__ = ["id", "value"]
    ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    id: str
    value: int
    def __init__(self, id: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...

class SignalSnapshot(_message.Message):
    __slots__ = ["depth_quote", "instrument_id", "last_timestamp", "market", "md_date", "md_time", "msg_sequence", "msg_type", "security_id", "security_type", "signal_id", "signal_name", "signal_quote", "signal_type", "signal_value", "symbol"]
    DEPTH_QUOTE_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MD_DATE_FIELD_NUMBER: _ClassVar[int]
    MD_TIME_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_QUOTE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    depth_quote: _containers.RepeatedCompositeFieldContainer[QuoteLevelData]
    instrument_id: str
    last_timestamp: int
    market: str
    md_date: int
    md_time: int
    msg_sequence: int
    msg_type: int
    security_id: str
    security_type: str
    signal_id: int
    signal_name: str
    signal_quote: _containers.RepeatedCompositeFieldContainer[SignalQuoteData]
    signal_type: int
    signal_value: int
    symbol: str
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., instrument_id: _Optional[str] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., security_type: _Optional[str] = ..., symbol: _Optional[str] = ..., md_date: _Optional[int] = ..., md_time: _Optional[int] = ..., signal_type: _Optional[int] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., signal_value: _Optional[int] = ..., signal_quote: _Optional[_Iterable[_Union[SignalQuoteData, _Mapping]]] = ..., depth_quote: _Optional[_Iterable[_Union[QuoteLevelData, _Mapping]]] = ...) -> None: ...

class SignalStatDetail(_message.Message):
    __slots__ = ["instrument_id", "last_price", "md_time", "md_type", "signal_id", "signal_name", "signal_value", "status", "text"]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_PRICE_FIELD_NUMBER: _ClassVar[int]
    MD_TIME_FIELD_NUMBER: _ClassVar[int]
    MD_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    instrument_id: str
    last_price: int
    md_time: int
    md_type: int
    signal_id: int
    signal_name: str
    signal_value: int
    status: str
    text: str
    def __init__(self, signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., status: _Optional[str] = ..., text: _Optional[str] = ..., instrument_id: _Optional[str] = ..., md_type: _Optional[int] = ..., md_time: _Optional[int] = ..., signal_value: _Optional[int] = ..., last_price: _Optional[int] = ...) -> None: ...

class SignalStatEvent(_message.Message):
    __slots__ = ["last_timestamp", "msg_sequence", "msg_type", "node_name", "node_type", "signal_id", "signal_name", "signal_stat"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_STAT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_sequence: int
    msg_type: int
    node_name: str
    node_type: int
    signal_id: int
    signal_name: str
    signal_stat: _containers.RepeatedCompositeFieldContainer[SignalStatDetail]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., signal_stat: _Optional[_Iterable[_Union[SignalStatDetail, _Mapping]]] = ...) -> None: ...

class StrategyControlReq(_message.Message):
    __slots__ = ["control_type", "last_timestamp", "msg_type", "operate_type", "request_id", "strategy_id", "strategy_name"]
    class ControlType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CONTROL_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    control_type: StrategyControlReq.ControlType
    kInit: StrategyControlReq.ControlType
    kPause: StrategyControlReq.ControlType
    kRunning: StrategyControlReq.ControlType
    kStop: StrategyControlReq.ControlType
    last_timestamp: int
    msg_type: int
    operate_type: int
    request_id: str
    strategy_id: int
    strategy_name: str
    def __init__(self, msg_type: _Optional[int] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., control_type: _Optional[_Union[StrategyControlReq.ControlType, str]] = ..., operate_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class StrategyControlRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "request_id", "status", "strategy_id", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    request_id: str
    status: int
    strategy_id: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., strategy_id: _Optional[int] = ..., status: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., text: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class StrategyInfo(_message.Message):
    __slots__ = ["account_id", "book_id", "comment", "counter_account_id", "counter_id", "default_params", "monitor_params", "node_id", "node_name", "params", "signal_id", "signal_name", "status", "strategy_id", "strategy_instruments", "strategy_name", "target_qty", "trade_date"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BOOK_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    COUNTER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    COUNTER_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MONITOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_INSTRUMENTS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_QTY_FIELD_NUMBER: _ClassVar[int]
    TRADE_DATE_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    book_id: str
    comment: str
    counter_account_id: str
    counter_id: str
    default_params: str
    monitor_params: str
    node_id: int
    node_name: str
    params: str
    signal_id: int
    signal_name: str
    status: str
    strategy_id: int
    strategy_instruments: _containers.RepeatedCompositeFieldContainer[StrategyInstrument]
    strategy_name: str
    target_qty: int
    trade_date: str
    def __init__(self, strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., book_id: _Optional[str] = ..., status: _Optional[str] = ..., comment: _Optional[str] = ..., node_id: _Optional[int] = ..., node_name: _Optional[str] = ..., account_id: _Optional[str] = ..., trade_date: _Optional[str] = ..., params: _Optional[str] = ..., monitor_params: _Optional[str] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., strategy_instruments: _Optional[_Iterable[_Union[StrategyInstrument, _Mapping]]] = ..., target_qty: _Optional[int] = ..., counter_id: _Optional[str] = ..., counter_account_id: _Optional[str] = ..., default_params: _Optional[str] = ...) -> None: ...

class StrategyInstrument(_message.Message):
    __slots__ = ["instrument_id", "market", "security_id", "sod_amount", "sod_qty"]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SOD_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SOD_QTY_FIELD_NUMBER: _ClassVar[int]
    instrument_id: str
    market: str
    security_id: str
    sod_amount: float
    sod_qty: int
    def __init__(self, instrument_id: _Optional[str] = ..., market: _Optional[str] = ..., security_id: _Optional[str] = ..., sod_qty: _Optional[int] = ..., sod_amount: _Optional[float] = ...) -> None: ...

class StrategyInstrumentStat(_message.Message):
    __slots__ = ["account_id", "book_id", "buy_amount", "buy_avg_price", "buy_pnl", "buy_qty", "current_qty", "fee", "instrument_id", "last_price", "prev_close", "sell_amount", "sell_avg_price", "sell_pnl", "sell_qty", "sod_pnl", "sod_qty", "strategy_id", "strategy_name", "symbol", "total_pnl", "trade_amount", "trade_pnl", "trade_qty"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BOOK_ID_FIELD_NUMBER: _ClassVar[int]
    BUY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    BUY_AVG_PRICE_FIELD_NUMBER: _ClassVar[int]
    BUY_PNL_FIELD_NUMBER: _ClassVar[int]
    BUY_QTY_FIELD_NUMBER: _ClassVar[int]
    CURRENT_QTY_FIELD_NUMBER: _ClassVar[int]
    FEE_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_PRICE_FIELD_NUMBER: _ClassVar[int]
    PREV_CLOSE_FIELD_NUMBER: _ClassVar[int]
    SELL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SELL_AVG_PRICE_FIELD_NUMBER: _ClassVar[int]
    SELL_PNL_FIELD_NUMBER: _ClassVar[int]
    SELL_QTY_FIELD_NUMBER: _ClassVar[int]
    SOD_PNL_FIELD_NUMBER: _ClassVar[int]
    SOD_QTY_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PNL_FIELD_NUMBER: _ClassVar[int]
    TRADE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TRADE_PNL_FIELD_NUMBER: _ClassVar[int]
    TRADE_QTY_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    book_id: str
    buy_amount: float
    buy_avg_price: float
    buy_pnl: float
    buy_qty: int
    current_qty: int
    fee: float
    instrument_id: str
    last_price: float
    prev_close: float
    sell_amount: float
    sell_avg_price: float
    sell_pnl: float
    sell_qty: int
    sod_pnl: float
    sod_qty: int
    strategy_id: int
    strategy_name: str
    symbol: str
    total_pnl: float
    trade_amount: float
    trade_pnl: float
    trade_qty: int
    def __init__(self, strategy_name: _Optional[str] = ..., instrument_id: _Optional[str] = ..., book_id: _Optional[str] = ..., account_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., sod_qty: _Optional[int] = ..., trade_pnl: _Optional[float] = ..., total_pnl: _Optional[float] = ..., current_qty: _Optional[int] = ..., trade_qty: _Optional[int] = ..., trade_amount: _Optional[float] = ..., last_price: _Optional[float] = ..., fee: _Optional[float] = ..., buy_qty: _Optional[int] = ..., sell_qty: _Optional[int] = ..., buy_amount: _Optional[float] = ..., sell_amount: _Optional[float] = ..., buy_pnl: _Optional[float] = ..., sell_pnl: _Optional[float] = ..., buy_avg_price: _Optional[float] = ..., sell_avg_price: _Optional[float] = ..., prev_close: _Optional[float] = ..., sod_pnl: _Optional[float] = ..., symbol: _Optional[str] = ...) -> None: ...

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
    def __init__(self, msg_type: _Optional[int] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., log_level: _Optional[_Union[StrategyLogEvent.LogLevel, str]] = ..., occur_time: _Optional[int] = ..., file_name: _Optional[str] = ..., function_name: _Optional[str] = ..., line: _Optional[int] = ..., text: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ...) -> None: ...

class StrategyPosition(_message.Message):
    __slots__ = ["account_id", "avail_qty", "book_id", "buy_amount", "buy_qty", "contract_unit", "current_qty", "instrument_id", "last_px", "posi_amount", "prev_close", "sell_amount", "sell_qty", "sod_amount", "sod_qty", "strategy_id", "strategy_name", "target_qty"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    AVAIL_QTY_FIELD_NUMBER: _ClassVar[int]
    BOOK_ID_FIELD_NUMBER: _ClassVar[int]
    BUY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    BUY_QTY_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    CURRENT_QTY_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_PX_FIELD_NUMBER: _ClassVar[int]
    POSI_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    PREV_CLOSE_FIELD_NUMBER: _ClassVar[int]
    SELL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SELL_QTY_FIELD_NUMBER: _ClassVar[int]
    SOD_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SOD_QTY_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_QTY_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    avail_qty: int
    book_id: str
    buy_amount: float
    buy_qty: int
    contract_unit: float
    current_qty: int
    instrument_id: str
    last_px: float
    posi_amount: float
    prev_close: float
    sell_amount: float
    sell_qty: int
    sod_amount: float
    sod_qty: int
    strategy_id: int
    strategy_name: str
    target_qty: int
    def __init__(self, strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., instrument_id: _Optional[str] = ..., target_qty: _Optional[int] = ..., sod_qty: _Optional[int] = ..., current_qty: _Optional[int] = ..., posi_amount: _Optional[float] = ..., last_px: _Optional[float] = ..., buy_amount: _Optional[float] = ..., sell_amount: _Optional[float] = ..., buy_qty: _Optional[int] = ..., sell_qty: _Optional[int] = ..., avail_qty: _Optional[int] = ..., contract_unit: _Optional[float] = ..., sod_amount: _Optional[float] = ..., account_id: _Optional[str] = ..., book_id: _Optional[str] = ..., prev_close: _Optional[float] = ...) -> None: ...

class StrategyStatDetail(_message.Message):
    __slots__ = ["active_buy_amt", "active_buy_price", "active_order_nums", "active_order_qty", "active_sell_amt", "active_sell_price", "ask_premium_rate", "avail_qty", "best_order_spread", "bid_premium_rate", "buy_amount", "buy_qty", "contract_unit", "cost_price", "current_qty", "diff2limit", "effective_active_amt", "expo_amt", "expo_qty", "float_pnl", "impact_factor", "instrument_id", "last_px", "max_spread_in_target_order_amt", "net_buy_amount", "net_change", "node_id", "node_name", "order_depth", "orders", "original_price", "posi_adjust_rate", "posi_amount", "positon_rate", "pre_close_price", "sell_amount", "sell_qty", "sod_qty", "stat_ask_price", "stat_bid_price", "stat_fields", "stat_status", "status", "strategy_id", "strategy_name", "strategy_template_id", "symbol", "target_qty", "text", "theory_price", "total_cancel_nums", "total_order_nums", "total_order_qty", "total_trade_amount", "trade_rate", "trade_side_rate"]
    class DepthItem(_message.Message):
        __slots__ = ["price", "side", "volume"]
        PRICE_FIELD_NUMBER: _ClassVar[int]
        SIDE_FIELD_NUMBER: _ClassVar[int]
        VOLUME_FIELD_NUMBER: _ClassVar[int]
        price: float
        side: int
        volume: int
        def __init__(self, price: _Optional[float] = ..., volume: _Optional[int] = ..., side: _Optional[int] = ...) -> None: ...
    class OrderItem(_message.Message):
        __slots__ = ["ids", "price", "qty", "side"]
        IDS_FIELD_NUMBER: _ClassVar[int]
        PRICE_FIELD_NUMBER: _ClassVar[int]
        QTY_FIELD_NUMBER: _ClassVar[int]
        SIDE_FIELD_NUMBER: _ClassVar[int]
        ids: _containers.RepeatedScalarFieldContainer[str]
        price: float
        qty: int
        side: int
        def __init__(self, price: _Optional[float] = ..., qty: _Optional[int] = ..., side: _Optional[int] = ..., ids: _Optional[_Iterable[str]] = ...) -> None: ...
    ACTIVE_BUY_AMT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_BUY_PRICE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ORDER_NUMS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SELL_AMT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SELL_PRICE_FIELD_NUMBER: _ClassVar[int]
    ASK_PREMIUM_RATE_FIELD_NUMBER: _ClassVar[int]
    AVAIL_QTY_FIELD_NUMBER: _ClassVar[int]
    BEST_ORDER_SPREAD_FIELD_NUMBER: _ClassVar[int]
    BID_PREMIUM_RATE_FIELD_NUMBER: _ClassVar[int]
    BUY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    BUY_QTY_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    COST_PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_QTY_FIELD_NUMBER: _ClassVar[int]
    DIFF2LIMIT_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_ACTIVE_AMT_FIELD_NUMBER: _ClassVar[int]
    EXPO_AMT_FIELD_NUMBER: _ClassVar[int]
    EXPO_QTY_FIELD_NUMBER: _ClassVar[int]
    FLOAT_PNL_FIELD_NUMBER: _ClassVar[int]
    IMPACT_FACTOR_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_PX_FIELD_NUMBER: _ClassVar[int]
    MAX_SPREAD_IN_TARGET_ORDER_AMT_FIELD_NUMBER: _ClassVar[int]
    NET_BUY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    NET_CHANGE_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    ORDER_DEPTH_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_PRICE_FIELD_NUMBER: _ClassVar[int]
    POSITON_RATE_FIELD_NUMBER: _ClassVar[int]
    POSI_ADJUST_RATE_FIELD_NUMBER: _ClassVar[int]
    POSI_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    PRE_CLOSE_PRICE_FIELD_NUMBER: _ClassVar[int]
    SELL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SELL_QTY_FIELD_NUMBER: _ClassVar[int]
    SOD_QTY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STAT_ASK_PRICE_FIELD_NUMBER: _ClassVar[int]
    STAT_BID_PRICE_FIELD_NUMBER: _ClassVar[int]
    STAT_FIELDS_FIELD_NUMBER: _ClassVar[int]
    STAT_STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TARGET_QTY_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    THEORY_PRICE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CANCEL_NUMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ORDER_NUMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ORDER_QTY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TRADE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TRADE_RATE_FIELD_NUMBER: _ClassVar[int]
    TRADE_SIDE_RATE_FIELD_NUMBER: _ClassVar[int]
    active_buy_amt: float
    active_buy_price: float
    active_order_nums: int
    active_order_qty: int
    active_sell_amt: float
    active_sell_price: float
    ask_premium_rate: float
    avail_qty: int
    best_order_spread: int
    bid_premium_rate: float
    buy_amount: float
    buy_qty: int
    contract_unit: float
    cost_price: float
    current_qty: int
    diff2limit: float
    effective_active_amt: float
    expo_amt: float
    expo_qty: int
    float_pnl: float
    impact_factor: float
    instrument_id: str
    last_px: float
    max_spread_in_target_order_amt: int
    net_buy_amount: float
    net_change: float
    node_id: int
    node_name: str
    order_depth: _containers.RepeatedCompositeFieldContainer[StrategyStatDetail.DepthItem]
    orders: _containers.RepeatedCompositeFieldContainer[StrategyStatDetail.OrderItem]
    original_price: float
    posi_adjust_rate: float
    posi_amount: float
    positon_rate: float
    pre_close_price: float
    sell_amount: float
    sell_qty: int
    sod_qty: int
    stat_ask_price: float
    stat_bid_price: float
    stat_fields: str
    stat_status: int
    status: str
    strategy_id: int
    strategy_name: str
    strategy_template_id: str
    symbol: str
    target_qty: int
    text: str
    theory_price: float
    total_cancel_nums: int
    total_order_nums: int
    total_order_qty: int
    total_trade_amount: float
    trade_rate: float
    trade_side_rate: float
    def __init__(self, strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., strategy_template_id: _Optional[str] = ..., status: _Optional[str] = ..., instrument_id: _Optional[str] = ..., symbol: _Optional[str] = ..., expo_qty: _Optional[int] = ..., sod_qty: _Optional[int] = ..., current_qty: _Optional[int] = ..., posi_amount: _Optional[float] = ..., last_px: _Optional[float] = ..., buy_amount: _Optional[float] = ..., sell_amount: _Optional[float] = ..., buy_qty: _Optional[int] = ..., sell_qty: _Optional[int] = ..., expo_amt: _Optional[float] = ..., active_order_nums: _Optional[int] = ..., text: _Optional[str] = ..., avail_qty: _Optional[int] = ..., net_change: _Optional[float] = ..., best_order_spread: _Optional[int] = ..., positon_rate: _Optional[float] = ..., trade_side_rate: _Optional[float] = ..., net_buy_amount: _Optional[float] = ..., total_trade_amount: _Optional[float] = ..., trade_rate: _Optional[float] = ..., diff2limit: _Optional[float] = ..., order_depth: _Optional[_Iterable[_Union[StrategyStatDetail.DepthItem, _Mapping]]] = ..., orders: _Optional[_Iterable[_Union[StrategyStatDetail.OrderItem, _Mapping]]] = ..., bid_premium_rate: _Optional[float] = ..., ask_premium_rate: _Optional[float] = ..., impact_factor: _Optional[float] = ..., theory_price: _Optional[float] = ..., original_price: _Optional[float] = ..., cost_price: _Optional[float] = ..., pre_close_price: _Optional[float] = ..., float_pnl: _Optional[float] = ..., contract_unit: _Optional[float] = ..., posi_adjust_rate: _Optional[float] = ..., active_buy_amt: _Optional[float] = ..., active_sell_amt: _Optional[float] = ..., max_spread_in_target_order_amt: _Optional[int] = ..., target_qty: _Optional[int] = ..., node_id: _Optional[int] = ..., node_name: _Optional[str] = ..., active_buy_price: _Optional[float] = ..., active_sell_price: _Optional[float] = ..., effective_active_amt: _Optional[float] = ..., stat_bid_price: _Optional[float] = ..., stat_ask_price: _Optional[float] = ..., stat_fields: _Optional[str] = ..., stat_status: _Optional[int] = ..., active_order_qty: _Optional[int] = ..., total_order_qty: _Optional[int] = ..., total_order_nums: _Optional[int] = ..., total_cancel_nums: _Optional[int] = ...) -> None: ...

class StrategyStatEvent(_message.Message):
    __slots__ = ["last_timestamp", "msg_sequence", "msg_type", "strategy_id", "strategy_name", "strategy_stat"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_STAT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_sequence: int
    msg_type: int
    strategy_id: int
    strategy_name: str
    strategy_stat: StrategyStatDetail
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., strategy_stat: _Optional[_Union[StrategyStatDetail, _Mapping]] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class StrategySummary(_message.Message):
    __slots__ = ["account_id", "book_id", "buy_amount", "buy_pnl", "fee", "sell_amount", "sell_pnl", "sod_pnl", "stats", "strategy_id", "strategy_name", "total_amount", "total_instruments", "total_pnl", "trade_amount", "trade_pnl"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BOOK_ID_FIELD_NUMBER: _ClassVar[int]
    BUY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    BUY_PNL_FIELD_NUMBER: _ClassVar[int]
    FEE_FIELD_NUMBER: _ClassVar[int]
    SELL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SELL_PNL_FIELD_NUMBER: _ClassVar[int]
    SOD_PNL_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_INSTRUMENTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PNL_FIELD_NUMBER: _ClassVar[int]
    TRADE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TRADE_PNL_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    book_id: str
    buy_amount: float
    buy_pnl: float
    fee: float
    sell_amount: float
    sell_pnl: float
    sod_pnl: float
    stats: _containers.RepeatedCompositeFieldContainer[StrategyInstrumentStat]
    strategy_id: int
    strategy_name: str
    total_amount: float
    total_instruments: int
    total_pnl: float
    trade_amount: float
    trade_pnl: float
    def __init__(self, strategy_name: _Optional[str] = ..., book_id: _Optional[str] = ..., account_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., trade_pnl: _Optional[float] = ..., total_pnl: _Optional[float] = ..., trade_amount: _Optional[float] = ..., total_amount: _Optional[float] = ..., fee: _Optional[float] = ..., buy_amount: _Optional[float] = ..., sell_amount: _Optional[float] = ..., buy_pnl: _Optional[float] = ..., sell_pnl: _Optional[float] = ..., sod_pnl: _Optional[float] = ..., stats: _Optional[_Iterable[_Union[StrategyInstrumentStat, _Mapping]]] = ..., total_instruments: _Optional[int] = ...) -> None: ...

class SubscribeReq(_message.Message):
    __slots__ = ["instrument_id", "msg_type", "quote_type", "request_id", "sub_type"]
    class QuoteType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class SubscribeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ETF_SNAPSHOT: SubscribeReq.QuoteType
    ETF_TICK: SubscribeReq.QuoteType
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MD_SNAPSHOT: SubscribeReq.QuoteType
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    QUOTE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_SNAPSHOT: SubscribeReq.QuoteType
    SUBSCRIBE: SubscribeReq.SubscribeType
    SUB_TYPE_FIELD_NUMBER: _ClassVar[int]
    TICK: SubscribeReq.QuoteType
    UNSUBSCRIBE: SubscribeReq.SubscribeType
    instrument_id: str
    msg_type: int
    quote_type: SubscribeReq.QuoteType
    request_id: str
    sub_type: SubscribeReq.SubscribeType
    def __init__(self, msg_type: _Optional[int] = ..., sub_type: _Optional[_Union[SubscribeReq.SubscribeType, str]] = ..., quote_type: _Optional[_Union[SubscribeReq.QuoteType, str]] = ..., instrument_id: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class SubscribeRsp(_message.Message):
    __slots__ = ["error_msg", "is_succ", "last_timestamp", "msg_type", "request_id"]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    IS_SUCC_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    error_msg: str
    is_succ: bool
    last_timestamp: int
    msg_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., is_succ: bool = ..., error_msg: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class Trade(_message.Message):
    __slots__ = ["account_id", "algo_type", "appl_id", "attachment", "business_type", "cl_order_id", "contract_unit", "counter_cl_order_id", "counter_order_id", "instrument_id", "investor_id", "last_amt", "last_px", "last_qty", "market", "match_place", "order_date", "order_id", "order_source", "order_time", "order_type", "owner_type", "parent_order_id", "position_effect", "security_id", "security_type", "side", "strategy_id", "strategy_name", "symbol", "trade_id", "trade_time", "user_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALGO_TYPE_FIELD_NUMBER: _ClassVar[int]
    APPL_ID_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_UNIT_FIELD_NUMBER: _ClassVar[int]
    COUNTER_CL_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    COUNTER_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_AMT_FIELD_NUMBER: _ClassVar[int]
    LAST_PX_FIELD_NUMBER: _ClassVar[int]
    LAST_QTY_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MATCH_PLACE_FIELD_NUMBER: _ClassVar[int]
    ORDER_DATE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ORDER_TIME_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_EFFECT_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ID_FIELD_NUMBER: _ClassVar[int]
    SECURITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TRADE_ID_FIELD_NUMBER: _ClassVar[int]
    TRADE_TIME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    algo_type: int
    appl_id: str
    attachment: str
    business_type: str
    cl_order_id: str
    contract_unit: float
    counter_cl_order_id: str
    counter_order_id: str
    instrument_id: str
    investor_id: str
    last_amt: float
    last_px: float
    last_qty: int
    market: str
    match_place: int
    order_date: int
    order_id: str
    order_source: str
    order_time: int
    order_type: int
    owner_type: int
    parent_order_id: str
    position_effect: int
    security_id: str
    security_type: str
    side: int
    strategy_id: int
    strategy_name: str
    symbol: str
    trade_id: str
    trade_time: int
    user_id: str
    def __init__(self, order_id: _Optional[str] = ..., cl_order_id: _Optional[str] = ..., order_date: _Optional[int] = ..., order_time: _Optional[int] = ..., trade_id: _Optional[str] = ..., trade_time: _Optional[int] = ..., order_type: _Optional[int] = ..., side: _Optional[int] = ..., position_effect: _Optional[int] = ..., owner_type: _Optional[int] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., security_type: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., contract_unit: _Optional[float] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., business_type: _Optional[str] = ..., last_qty: _Optional[int] = ..., last_px: _Optional[float] = ..., last_amt: _Optional[float] = ..., match_place: _Optional[int] = ..., algo_type: _Optional[int] = ..., order_source: _Optional[str] = ..., attachment: _Optional[str] = ..., user_id: _Optional[str] = ..., counter_cl_order_id: _Optional[str] = ..., counter_order_id: _Optional[str] = ..., symbol: _Optional[str] = ..., parent_order_id: _Optional[str] = ...) -> None: ...

class TradeConfirm(_message.Message):
    __slots__ = ["account_id", "algo_type", "appl_id", "attachment", "basket_id", "business_type", "cl_order_id", "contract_unit", "counter_cl_order_id", "counter_order_id", "counterparty_id", "instrument_id", "investor_id", "is_maker", "last_px", "last_qty", "market", "match_place", "msg_sequence", "msg_type", "order_id", "order_price", "order_qty", "order_source", "order_type", "owner_type", "parent_order_id", "position_effect", "security_id", "side", "strategy_id", "strategy_name", "symbol", "trade_amt", "trade_id", "trade_time", "user_id"]
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
    def __init__(self, msg_type: _Optional[int] = ..., msg_sequence: _Optional[int] = ..., cl_order_id: _Optional[str] = ..., order_id: _Optional[str] = ..., counter_order_id: _Optional[str] = ..., trade_id: _Optional[str] = ..., trade_time: _Optional[int] = ..., last_px: _Optional[float] = ..., last_qty: _Optional[int] = ..., security_id: _Optional[str] = ..., market: _Optional[str] = ..., instrument_id: _Optional[str] = ..., appl_id: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., match_place: _Optional[int] = ..., counterparty_id: _Optional[str] = ..., is_maker: _Optional[int] = ..., side: _Optional[int] = ..., position_effect: _Optional[int] = ..., trade_amt: _Optional[float] = ..., order_qty: _Optional[int] = ..., order_price: _Optional[float] = ..., contract_unit: _Optional[float] = ..., order_type: _Optional[int] = ..., order_source: _Optional[str] = ..., user_id: _Optional[str] = ..., counter_cl_order_id: _Optional[str] = ..., owner_type: _Optional[int] = ..., business_type: _Optional[str] = ..., symbol: _Optional[str] = ..., parent_order_id: _Optional[str] = ..., algo_type: _Optional[int] = ..., attachment: _Optional[str] = ..., basket_id: _Optional[str] = ...) -> None: ...

class UpdateBasketTemplateReq(_message.Message):
    __slots__ = ["basket_info_details", "msg_type", "new_template_id", "request_id", "strategy_name", "template_id", "template_type"]
    BASKET_INFO_DETAILS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NEW_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    basket_info_details: _containers.RepeatedCompositeFieldContainer[BasketInfoDetail]
    msg_type: int
    new_template_id: str
    request_id: str
    strategy_name: str
    template_id: str
    template_type: str
    def __init__(self, msg_type: _Optional[int] = ..., template_id: _Optional[str] = ..., new_template_id: _Optional[str] = ..., basket_info_details: _Optional[_Iterable[_Union[BasketInfoDetail, _Mapping]]] = ..., strategy_name: _Optional[str] = ..., request_id: _Optional[str] = ..., template_type: _Optional[str] = ...) -> None: ...

class UpdateBasketTemplateRsp(_message.Message):
    __slots__ = ["msg_type", "reason", "request_id", "status", "template_id", "template_type"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    reason: str
    request_id: str
    status: int
    template_id: str
    template_type: str
    def __init__(self, msg_type: _Optional[int] = ..., template_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., request_id: _Optional[str] = ..., template_type: _Optional[str] = ...) -> None: ...

class UpdateCurrencyPriceReq(_message.Message):
    __slots__ = ["currency_id", "currency_price", "last_timestamp", "msg_type", "request_id", "text"]
    CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_PRICE_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    currency_id: str
    currency_price: int
    last_timestamp: int
    msg_type: int
    request_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., currency_id: _Optional[str] = ..., currency_price: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class UpdateCurrencyPriceRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "request_id", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    request_id: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., status: _Optional[int] = ..., request_id: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class UpdateDefaultStrategyParamsEvent(_message.Message):
    __slots__ = ["default_params", "last_timestamp", "msg_type", "strategy_id", "strategy_name", "text"]
    DEFAULT_PARAMS_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    default_params: str
    last_timestamp: int
    msg_type: int
    strategy_id: int
    strategy_name: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., strategy_name: _Optional[str] = ..., strategy_id: _Optional[int] = ..., default_params: _Optional[str] = ..., text: _Optional[str] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class UpdateRiskMarketParamsReq(_message.Message):
    __slots__ = ["account_id", "last_timestamp", "msg_type", "operate_type", "request_id", "risk_params"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RISK_PARAMS_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    last_timestamp: int
    msg_type: int
    operate_type: str
    request_id: str
    risk_params: _containers.RepeatedCompositeFieldContainer[RiskMarketParams]
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[str] = ..., risk_params: _Optional[_Iterable[_Union[RiskMarketParams, _Mapping]]] = ..., account_id: _Optional[str] = ...) -> None: ...

class UpdateRiskMarketParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "operate_type", "request_id", "risk_params", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RISK_PARAMS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    operate_type: str
    request_id: str
    risk_params: _containers.RepeatedCompositeFieldContainer[RiskMarketParams]
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., risk_params: _Optional[_Iterable[_Union[RiskMarketParams, _Mapping]]] = ...) -> None: ...

class UpdateRiskParamsReq(_message.Message):
    __slots__ = ["account_id", "last_timestamp", "msg_type", "operate_type", "request_id", "risk_item"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RISK_ITEM_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    last_timestamp: int
    msg_type: int
    operate_type: str
    request_id: str
    risk_item: _containers.RepeatedCompositeFieldContainer[RiskItem]
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[str] = ..., risk_item: _Optional[_Iterable[_Union[RiskItem, _Mapping]]] = ..., account_id: _Optional[str] = ...) -> None: ...

class UpdateRiskParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "request_id", "risk_item", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RISK_ITEM_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    request_id: str
    risk_item: _containers.RepeatedCompositeFieldContainer[RiskItem]
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., risk_item: _Optional[_Iterable[_Union[RiskItem, _Mapping]]] = ...) -> None: ...

class UpdateSignalGlobalParamsEvent(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "signal_params", "signal_template_id", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    signal_params: str
    signal_template_id: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., signal_template_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., signal_params: _Optional[str] = ...) -> None: ...

class UpdateSignalGlobalParamsReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "request_id", "signal_params", "signal_template_id", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    request_id: str
    signal_params: str
    signal_template_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., signal_template_id: _Optional[str] = ..., text: _Optional[str] = ..., signal_params: _Optional[str] = ...) -> None: ...

class UpdateSignalGlobalParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "request_id", "signal_params", "signal_template_id", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    request_id: str
    signal_params: str
    signal_template_id: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., signal_template_id: _Optional[str] = ..., status: _Optional[int] = ..., request_id: _Optional[str] = ..., text: _Optional[str] = ..., signal_params: _Optional[str] = ...) -> None: ...

class UpdateSignalParamsEvent(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "package_info", "signal_id", "signal_info_l2", "signal_name", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_INFO_L2_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    package_info: _containers.RepeatedCompositeFieldContainer[PackageInfo]
    signal_id: int
    signal_info_l2: _containers.RepeatedCompositeFieldContainer[SignalInfoL2]
    signal_name: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., signal_name: _Optional[str] = ..., signal_id: _Optional[int] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., package_info: _Optional[_Iterable[_Union[PackageInfo, _Mapping]]] = ..., signal_info_l2: _Optional[_Iterable[_Union[SignalInfoL2, _Mapping]]] = ...) -> None: ...

class UpdateSignalParamsReq(_message.Message):
    __slots__ = ["fund_etfpr_estcash", "fund_etfpr_minnav", "last_timestamp", "msg_type", "package_info", "request_id", "signal_id", "signal_info_l2", "signal_name", "signal_params", "text"]
    FUND_ETFPR_ESTCASH_FIELD_NUMBER: _ClassVar[int]
    FUND_ETFPR_MINNAV_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_INFO_L2_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    fund_etfpr_estcash: float
    fund_etfpr_minnav: float
    last_timestamp: int
    msg_type: int
    package_info: _containers.RepeatedCompositeFieldContainer[PackageInfo]
    request_id: str
    signal_id: int
    signal_info_l2: _containers.RepeatedCompositeFieldContainer[SignalInfoL2]
    signal_name: str
    signal_params: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., signal_name: _Optional[str] = ..., signal_id: _Optional[int] = ..., text: _Optional[str] = ..., signal_params: _Optional[str] = ..., fund_etfpr_minnav: _Optional[float] = ..., fund_etfpr_estcash: _Optional[float] = ..., package_info: _Optional[_Iterable[_Union[PackageInfo, _Mapping]]] = ..., signal_info_l2: _Optional[_Iterable[_Union[SignalInfoL2, _Mapping]]] = ...) -> None: ...

class UpdateSignalParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "package_info", "request_id", "signal_id", "signal_info_l2", "signal_name", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_INFO_L2_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    package_info: _containers.RepeatedCompositeFieldContainer[PackageInfo]
    request_id: str
    signal_id: int
    signal_info_l2: _containers.RepeatedCompositeFieldContainer[SignalInfoL2]
    signal_name: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., signal_name: _Optional[str] = ..., signal_id: _Optional[int] = ..., status: _Optional[int] = ..., request_id: _Optional[str] = ..., text: _Optional[str] = ..., package_info: _Optional[_Iterable[_Union[PackageInfo, _Mapping]]] = ..., signal_info_l2: _Optional[_Iterable[_Union[SignalInfoL2, _Mapping]]] = ...) -> None: ...

class UpdateStrategyGlobalParamsEvent(_message.Message):
    __slots__ = ["last_timestamp", "monitor_params", "msg_type", "strategy_params", "strategy_template_id", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MONITOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_PARAMS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    monitor_params: str
    msg_type: int
    strategy_params: str
    strategy_template_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., strategy_template_id: _Optional[str] = ..., strategy_params: _Optional[str] = ..., monitor_params: _Optional[str] = ..., text: _Optional[str] = ..., last_timestamp: _Optional[int] = ...) -> None: ...

class UpdateStrategyGlobalParamsReq(_message.Message):
    __slots__ = ["last_timestamp", "monitor_params", "msg_type", "request_id", "strategy_params", "strategy_template_id", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MONITOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_PARAMS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    monitor_params: str
    msg_type: int
    request_id: str
    strategy_params: str
    strategy_template_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., strategy_template_id: _Optional[str] = ..., text: _Optional[str] = ..., strategy_params: _Optional[str] = ..., monitor_params: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class UpdateStrategyGlobalParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "monitor_params", "msg_type", "request_id", "status", "strategy_params", "strategy_template_id", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MONITOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_PARAMS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    monitor_params: str
    msg_type: int
    request_id: str
    status: int
    strategy_params: str
    strategy_template_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., strategy_template_id: _Optional[str] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., strategy_params: _Optional[str] = ..., monitor_params: _Optional[str] = ...) -> None: ...

class UpdateStrategyParamsEvent(_message.Message):
    __slots__ = ["last_timestamp", "monitor_params", "msg_type", "signal_id", "signal_name", "strategy_id", "strategy_instruments", "strategy_name", "strategy_params", "target_qty", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MONITOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    signal_id: int
    signal_name: str
    strategy_id: int
    strategy_instruments: _containers.RepeatedCompositeFieldContainer[StrategyInstrument]
    strategy_name: str
    strategy_params: str
    target_qty: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., strategy_name: _Optional[str] = ..., strategy_id: _Optional[int] = ..., strategy_params: _Optional[str] = ..., monitor_params: _Optional[str] = ..., text: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., strategy_instruments: _Optional[_Iterable[_Union[StrategyInstrument, _Mapping]]] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., target_qty: _Optional[int] = ...) -> None: ...

class UpdateStrategyParamsReq(_message.Message):
    __slots__ = ["last_timestamp", "monitor_params", "msg_type", "request_id", "signal_id", "signal_name", "strategy_id", "strategy_instruments", "strategy_name", "strategy_params", "target_qty", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MONITOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    request_id: str
    signal_id: int
    signal_name: str
    strategy_id: int
    strategy_instruments: _containers.RepeatedCompositeFieldContainer[StrategyInstrument]
    strategy_name: str
    strategy_params: str
    target_qty: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., strategy_name: _Optional[str] = ..., strategy_id: _Optional[int] = ..., text: _Optional[str] = ..., strategy_params: _Optional[str] = ..., monitor_params: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., strategy_instruments: _Optional[_Iterable[_Union[StrategyInstrument, _Mapping]]] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., target_qty: _Optional[int] = ...) -> None: ...

class UpdateStrategyParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "monitor_params", "msg_type", "request_id", "signal_id", "signal_name", "status", "strategy_id", "strategy_instruments", "strategy_name", "strategy_params", "target_qty", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MONITOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
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
    request_id: str
    signal_id: int
    signal_name: str
    status: int
    strategy_id: int
    strategy_instruments: _containers.RepeatedCompositeFieldContainer[StrategyInstrument]
    strategy_name: str
    strategy_params: str
    target_qty: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., strategy_name: _Optional[str] = ..., strategy_id: _Optional[int] = ..., status: _Optional[int] = ..., text: _Optional[str] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., strategy_params: _Optional[str] = ..., monitor_params: _Optional[str] = ..., strategy_instruments: _Optional[_Iterable[_Union[StrategyInstrument, _Mapping]]] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., target_qty: _Optional[int] = ...) -> None: ...

class PosType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class PosReqType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class PosAccountType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
