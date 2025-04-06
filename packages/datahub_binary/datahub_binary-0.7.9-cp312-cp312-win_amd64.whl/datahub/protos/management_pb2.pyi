import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Counter(_message.Message):
    __slots__ = ["account_id", "comment", "counter_id", "counter_type", "investor_id", "ip_address", "params", "passwd", "sec_investor_id"]
    class SecInvestor(_message.Message):
        __slots__ = ["market", "sec_investor_id"]
        MARKET_FIELD_NUMBER: _ClassVar[int]
        SEC_INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
        market: str
        sec_investor_id: str
        def __init__(self, market: _Optional[str] = ..., sec_investor_id: _Optional[str] = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    COUNTER_ID_FIELD_NUMBER: _ClassVar[int]
    COUNTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    PASSWD_FIELD_NUMBER: _ClassVar[int]
    SEC_INVESTOR_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: str
    comment: str
    counter_id: str
    counter_type: str
    investor_id: str
    ip_address: str
    params: str
    passwd: str
    sec_investor_id: _containers.RepeatedCompositeFieldContainer[Counter.SecInvestor]
    def __init__(self, counter_id: _Optional[str] = ..., counter_type: _Optional[str] = ..., account_id: _Optional[str] = ..., investor_id: _Optional[str] = ..., sec_investor_id: _Optional[_Iterable[_Union[Counter.SecInvestor, _Mapping]]] = ..., passwd: _Optional[str] = ..., ip_address: _Optional[str] = ..., params: _Optional[str] = ..., comment: _Optional[str] = ...) -> None: ...

class HttpLoginReq(_message.Message):
    __slots__ = ["passwd", "user_id"]
    PASSWD_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    passwd: str
    user_id: str
    def __init__(self, user_id: _Optional[str] = ..., passwd: _Optional[str] = ...) -> None: ...

class HttpLoginRsp(_message.Message):
    __slots__ = ["data", "status"]
    class Data(_message.Message):
        __slots__ = ["token"]
        TOKEN_FIELD_NUMBER: _ClassVar[int]
        token: str
        def __init__(self, token: _Optional[str] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: HttpLoginRsp.Data
    status: str
    def __init__(self, status: _Optional[str] = ..., data: _Optional[_Union[HttpLoginRsp.Data, _Mapping]] = ...) -> None: ...

class HttpQryInstrumentRsp(_message.Message):
    __slots__ = ["data", "page", "page_size", "status", "total_page", "total_size"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PAGE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_common_pb2.Instrument]
    page: int
    page_size: int
    status: str
    total_page: int
    total_size: int
    def __init__(self, status: _Optional[str] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., total_page: _Optional[int] = ..., total_size: _Optional[int] = ..., data: _Optional[_Iterable[_Union[_common_pb2.Instrument, _Mapping]]] = ...) -> None: ...

class QryCounterReq(_message.Message):
    __slots__ = ["msg_type", "node_name", "node_type", "request_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryCounterRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "node_name", "node_type", "reason", "request_id", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[Counter]
    is_last: bool
    msg_type: int
    node_name: str
    node_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[Counter, _Mapping]]] = ...) -> None: ...

class QryCurrencyReq(_message.Message):
    __slots__ = ["msg_type", "node_name", "node_type", "request_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryCurrencyRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "node_name", "node_type", "reason", "request_id", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_common_pb2.Currency]
    is_last: bool
    msg_type: int
    node_name: str
    node_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[_common_pb2.Currency, _Mapping]]] = ...) -> None: ...

class QryInstrumentReq(_message.Message):
    __slots__ = ["basket_instrument_id", "instrument_id", "msg_type", "node_name", "node_type", "request_id"]
    BASKET_INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    basket_instrument_id: str
    instrument_id: str
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., instrument_id: _Optional[str] = ..., basket_instrument_id: _Optional[str] = ...) -> None: ...

class QryInstrumentRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "node_name", "node_type", "reason", "request_id", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_common_pb2.Instrument]
    is_last: bool
    msg_type: int
    node_name: str
    node_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[_common_pb2.Instrument, _Mapping]]] = ...) -> None: ...

class QryNodeConfigReq(_message.Message):
    __slots__ = ["msg_type", "node_name", "node_type", "request_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ...) -> None: ...

class QryNodeConfigRsp(_message.Message):
    __slots__ = ["counter_account", "is_last", "msg_type", "node_name", "node_type", "reason", "request_id", "status", "trading_session"]
    COUNTER_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRADING_SESSION_FIELD_NUMBER: _ClassVar[int]
    counter_account: _containers.RepeatedCompositeFieldContainer[_common_pb2.CounterAccount]
    is_last: bool
    msg_type: int
    node_name: str
    node_type: int
    reason: str
    request_id: str
    status: int
    trading_session: _containers.RepeatedCompositeFieldContainer[_common_pb2.TradingSession]
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., trading_session: _Optional[_Iterable[_Union[_common_pb2.TradingSession, _Mapping]]] = ..., counter_account: _Optional[_Iterable[_Union[_common_pb2.CounterAccount, _Mapping]]] = ...) -> None: ...

class QryRiskItemReq(_message.Message):
    __slots__ = ["account_id", "instrument_id", "msg_type", "node_name", "node_type", "request_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: _containers.RepeatedScalarFieldContainer[str]
    instrument_id: _containers.RepeatedScalarFieldContainer[str]
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., account_id: _Optional[_Iterable[str]] = ..., instrument_id: _Optional[_Iterable[str]] = ...) -> None: ...

class QryRiskItemRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "node_name", "node_type", "reason", "request_id", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_common_pb2.RiskItem]
    is_last: bool
    msg_type: int
    node_name: str
    node_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[_common_pb2.RiskItem, _Mapping]]] = ...) -> None: ...

class QryRiskMarketParamsReq(_message.Message):
    __slots__ = ["account_id", "market", "msg_type", "node_name", "node_type", "request_id"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MARKET_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: _containers.RepeatedScalarFieldContainer[str]
    market: _containers.RepeatedScalarFieldContainer[str]
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., account_id: _Optional[_Iterable[str]] = ..., market: _Optional[_Iterable[str]] = ...) -> None: ...

class QryRiskMarketParamsRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "node_name", "node_type", "reason", "request_id", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_common_pb2.RiskMarketParams]
    is_last: bool
    msg_type: int
    node_name: str
    node_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[_common_pb2.RiskMarketParams, _Mapping]]] = ...) -> None: ...

class QrySignalInfoReq(_message.Message):
    __slots__ = ["msg_type", "node_name", "node_type", "request_id", "signal_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    signal_id: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., signal_id: _Optional[int] = ...) -> None: ...

class QrySignalInfoRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "node_name", "node_type", "reason", "request_id", "status"]
    class SignalInfoData(_message.Message):
        __slots__ = ["global_params", "signal_list", "signal_template_id"]
        GLOBAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
        SIGNAL_LIST_FIELD_NUMBER: _ClassVar[int]
        SIGNAL_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
        global_params: str
        signal_list: _containers.RepeatedCompositeFieldContainer[SignalInfo]
        signal_template_id: str
        def __init__(self, signal_template_id: _Optional[str] = ..., global_params: _Optional[str] = ..., signal_list: _Optional[_Iterable[_Union[SignalInfo, _Mapping]]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[QrySignalInfoRsp.SignalInfoData]
    is_last: bool
    msg_type: int
    node_name: str
    node_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[QrySignalInfoRsp.SignalInfoData, _Mapping]]] = ...) -> None: ...

class QryStrategyInfoReq(_message.Message):
    __slots__ = ["msg_type", "node_name", "node_type", "request_id", "strategy_id"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    strategy_id: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., strategy_id: _Optional[int] = ...) -> None: ...

class QryStrategyInfoRsp(_message.Message):
    __slots__ = ["data", "is_last", "msg_type", "node_name", "node_type", "reason", "request_id", "status"]
    class StrategyInfoData(_message.Message):
        __slots__ = ["global_params", "strategy_list", "strategy_template_id", "strategy_template_type", "strategy_type"]
        GLOBAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
        STRATEGY_LIST_FIELD_NUMBER: _ClassVar[int]
        STRATEGY_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
        STRATEGY_TEMPLATE_TYPE_FIELD_NUMBER: _ClassVar[int]
        STRATEGY_TYPE_FIELD_NUMBER: _ClassVar[int]
        global_params: str
        strategy_list: _containers.RepeatedCompositeFieldContainer[StrategyInfo]
        strategy_template_id: str
        strategy_template_type: str
        strategy_type: str
        def __init__(self, strategy_template_id: _Optional[str] = ..., strategy_template_type: _Optional[str] = ..., strategy_type: _Optional[str] = ..., global_params: _Optional[str] = ..., strategy_list: _Optional[_Iterable[_Union[StrategyInfo, _Mapping]]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[QryStrategyInfoRsp.StrategyInfoData]
    is_last: bool
    msg_type: int
    node_name: str
    node_type: int
    reason: str
    request_id: str
    status: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., request_id: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., is_last: bool = ..., data: _Optional[_Iterable[_Union[QryStrategyInfoRsp.StrategyInfoData, _Mapping]]] = ...) -> None: ...

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
    package_info: _containers.RepeatedCompositeFieldContainer[_common_pb2.PackageInfo]
    params: str
    security_id: str
    signal_id: int
    signal_info_l2: _containers.RepeatedCompositeFieldContainer[_common_pb2.SignalInfoL2]
    signal_name: str
    status: str
    trade_date: str
    def __init__(self, signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., instrument_id: _Optional[str] = ..., instrument_type: _Optional[str] = ..., market: _Optional[str] = ..., security_id: _Optional[str] = ..., status: _Optional[str] = ..., comment: _Optional[str] = ..., node_id: _Optional[int] = ..., node_name: _Optional[str] = ..., trade_date: _Optional[str] = ..., fund_etfpr_minnav: _Optional[float] = ..., fund_etfpr_estcash: _Optional[float] = ..., params: _Optional[str] = ..., package_info: _Optional[_Iterable[_Union[_common_pb2.PackageInfo, _Mapping]]] = ..., signal_info_l2: _Optional[_Iterable[_Union[_common_pb2.SignalInfoL2, _Mapping]]] = ...) -> None: ...

class StrategyInfo(_message.Message):
    __slots__ = ["account_id", "book_id", "comment", "counter_account_id", "counter_id", "monitor_params", "node_id", "node_name", "params", "signal_id", "signal_name", "status", "strategy_id", "strategy_instruments", "strategy_name", "target_qty", "trade_date"]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BOOK_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    COUNTER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    COUNTER_ID_FIELD_NUMBER: _ClassVar[int]
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
    monitor_params: str
    node_id: int
    node_name: str
    params: str
    signal_id: int
    signal_name: str
    status: str
    strategy_id: int
    strategy_instruments: _containers.RepeatedCompositeFieldContainer[_common_pb2.StrategyInstrument]
    strategy_name: str
    target_qty: int
    trade_date: str
    def __init__(self, strategy_id: _Optional[int] = ..., strategy_name: _Optional[str] = ..., book_id: _Optional[str] = ..., status: _Optional[str] = ..., comment: _Optional[str] = ..., node_id: _Optional[int] = ..., node_name: _Optional[str] = ..., account_id: _Optional[str] = ..., trade_date: _Optional[str] = ..., params: _Optional[str] = ..., monitor_params: _Optional[str] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., strategy_instruments: _Optional[_Iterable[_Union[_common_pb2.StrategyInstrument, _Mapping]]] = ..., target_qty: _Optional[int] = ..., counter_id: _Optional[str] = ..., counter_account_id: _Optional[str] = ...) -> None: ...
