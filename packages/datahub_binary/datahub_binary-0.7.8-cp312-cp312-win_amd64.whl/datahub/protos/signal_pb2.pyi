import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QrySignalStatReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "op_user", "request_id", "signal_id"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    request_id: str
    signal_id: int
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., signal_id: _Optional[int] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ...) -> None: ...

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

class SignalControlReq(_message.Message):
    __slots__ = ["control_type", "last_timestamp", "msg_type", "node_name", "node_type", "op_user", "operate_type", "request_id", "signal_id", "signal_name"]
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
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    operate_type: int
    request_id: str
    signal_id: int
    signal_name: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[int] = ..., signal_id: _Optional[int] = ..., signal_name: _Optional[str] = ..., control_type: _Optional[_Union[SignalControlReq.ControlType, str]] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ...) -> None: ...

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

class UpdateCurrencyPriceReq(_message.Message):
    __slots__ = ["currency_id", "currency_price", "last_timestamp", "msg_type", "node_name", "node_type", "op_user", "request_id", "text"]
    CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_PRICE_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    currency_id: str
    currency_price: int
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    request_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., currency_id: _Optional[str] = ..., currency_price: _Optional[int] = ..., text: _Optional[str] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ...) -> None: ...

class UpdateCurrencyPriceRsp(_message.Message):
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
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., status: _Optional[int] = ..., request_id: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class UpdateSignalGlobalParamsReq(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "op_user", "operate_type", "request_id", "signal_params", "signal_template_id", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    operate_type: int
    request_id: str
    signal_params: str
    signal_template_id: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[int] = ..., signal_template_id: _Optional[str] = ..., text: _Optional[str] = ..., signal_params: _Optional[str] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ...) -> None: ...

class UpdateSignalGlobalParamsRsp(_message.Message):
    __slots__ = ["last_timestamp", "msg_type", "node_name", "node_type", "request_id", "signal_params", "signal_template_id", "status", "text"]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    request_id: str
    signal_params: str
    signal_template_id: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., signal_template_id: _Optional[str] = ..., status: _Optional[int] = ..., request_id: _Optional[str] = ..., text: _Optional[str] = ..., signal_params: _Optional[str] = ...) -> None: ...

class UpdateSignalParamsReq(_message.Message):
    __slots__ = ["fund_etfpr_estcash", "fund_etfpr_minnav", "last_timestamp", "msg_type", "node_name", "node_type", "op_user", "operate_type", "package_info", "request_id", "signal_id", "signal_info_l2", "signal_name", "signal_params", "text"]
    FUND_ETFPR_ESTCASH_FIELD_NUMBER: _ClassVar[int]
    FUND_ETFPR_MINNAV_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_USER_FIELD_NUMBER: _ClassVar[int]
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
    node_name: str
    node_type: int
    op_user: _common_pb2.OpUser
    operate_type: int
    package_info: _containers.RepeatedCompositeFieldContainer[_common_pb2.PackageInfo]
    request_id: str
    signal_id: int
    signal_info_l2: _containers.RepeatedCompositeFieldContainer[_common_pb2.SignalInfoL2]
    signal_name: str
    signal_params: str
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., request_id: _Optional[str] = ..., operate_type: _Optional[int] = ..., signal_name: _Optional[str] = ..., signal_id: _Optional[int] = ..., text: _Optional[str] = ..., signal_params: _Optional[str] = ..., fund_etfpr_minnav: _Optional[float] = ..., fund_etfpr_estcash: _Optional[float] = ..., package_info: _Optional[_Iterable[_Union[_common_pb2.PackageInfo, _Mapping]]] = ..., signal_info_l2: _Optional[_Iterable[_Union[_common_pb2.SignalInfoL2, _Mapping]]] = ..., op_user: _Optional[_Union[_common_pb2.OpUser, _Mapping]] = ...) -> None: ...

class UpdateSignalParamsRsp(_message.Message):
    __slots__ = ["fund_etfpr_estcash", "fund_etfpr_minnav", "last_timestamp", "msg_type", "node_name", "node_type", "package_info", "request_id", "signal_id", "signal_info_l2", "signal_name", "signal_params", "status", "text"]
    FUND_ETFPR_ESTCASH_FIELD_NUMBER: _ClassVar[int]
    FUND_ETFPR_MINNAV_FIELD_NUMBER: _ClassVar[int]
    LAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_INFO_L2_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_NAME_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_PARAMS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    fund_etfpr_estcash: float
    fund_etfpr_minnav: float
    last_timestamp: int
    msg_type: int
    node_name: str
    node_type: int
    package_info: _containers.RepeatedCompositeFieldContainer[_common_pb2.PackageInfo]
    request_id: str
    signal_id: int
    signal_info_l2: _containers.RepeatedCompositeFieldContainer[_common_pb2.SignalInfoL2]
    signal_name: str
    signal_params: str
    status: int
    text: str
    def __init__(self, msg_type: _Optional[int] = ..., node_name: _Optional[str] = ..., node_type: _Optional[int] = ..., last_timestamp: _Optional[int] = ..., signal_name: _Optional[str] = ..., signal_id: _Optional[int] = ..., status: _Optional[int] = ..., request_id: _Optional[str] = ..., text: _Optional[str] = ..., signal_params: _Optional[str] = ..., fund_etfpr_minnav: _Optional[float] = ..., fund_etfpr_estcash: _Optional[float] = ..., package_info: _Optional[_Iterable[_Union[_common_pb2.PackageInfo, _Mapping]]] = ..., signal_info_l2: _Optional[_Iterable[_Union[_common_pb2.SignalInfoL2, _Mapping]]] = ...) -> None: ...
