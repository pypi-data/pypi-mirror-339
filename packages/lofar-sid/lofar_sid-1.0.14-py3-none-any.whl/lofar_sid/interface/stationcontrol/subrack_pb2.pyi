from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Subrack_Power_Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Subrack_POWER_OFF: _ClassVar[Subrack_Power_Status]
    Subrack_POWER_ON: _ClassVar[Subrack_Power_Status]
Subrack_POWER_OFF: Subrack_Power_Status
Subrack_POWER_ON: Subrack_Power_Status

class SubrackIdentifier(_message.Message):
    __slots__ = ("subrack_id",)
    SUBRACK_ID_FIELD_NUMBER: _ClassVar[int]
    subrack_id: str
    def __init__(self, subrack_id: _Optional[str] = ...) -> None: ...

class SetSubrackRequest(_message.Message):
    __slots__ = ("identifier", "power_status")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    POWER_STATUS_FIELD_NUMBER: _ClassVar[int]
    identifier: SubrackIdentifier
    power_status: Subrack_Power_Status
    def __init__(self, identifier: _Optional[_Union[SubrackIdentifier, _Mapping]] = ..., power_status: _Optional[_Union[Subrack_Power_Status, str]] = ...) -> None: ...

class GetSubrackRequest(_message.Message):
    __slots__ = ("identifier",)
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    identifier: SubrackIdentifier
    def __init__(self, identifier: _Optional[_Union[SubrackIdentifier, _Mapping]] = ...) -> None: ...

class SubrackResult(_message.Message):
    __slots__ = ("identifier", "power_status")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    POWER_STATUS_FIELD_NUMBER: _ClassVar[int]
    identifier: SubrackIdentifier
    power_status: Subrack_Power_Status
    def __init__(self, identifier: _Optional[_Union[SubrackIdentifier, _Mapping]] = ..., power_status: _Optional[_Union[Subrack_Power_Status, str]] = ...) -> None: ...

class SubrackReply(_message.Message):
    __slots__ = ("success", "exception", "result")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    exception: str
    result: SubrackResult
    def __init__(self, success: bool = ..., exception: _Optional[str] = ..., result: _Optional[_Union[SubrackResult, _Mapping]] = ...) -> None: ...
