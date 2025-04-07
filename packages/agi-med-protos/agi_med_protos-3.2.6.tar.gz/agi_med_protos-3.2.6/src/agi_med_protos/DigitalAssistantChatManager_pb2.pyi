from agi_med_protos import commons_pb2 as _commons_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalAssistantChatManagerRequest(_message.Message):
    __slots__ = ("Text", "OuterContext", "RequestId", "ResourceId")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    OUTERCONTEXT_FIELD_NUMBER: _ClassVar[int]
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    Text: str
    OuterContext: _commons_pb2.OuterContextItem
    RequestId: str
    ResourceId: str
    def __init__(self, Text: _Optional[str] = ..., OuterContext: _Optional[_Union[_commons_pb2.OuterContextItem, _Mapping]] = ..., RequestId: _Optional[str] = ..., ResourceId: _Optional[str] = ...) -> None: ...

class DigitalAssistantChatManagerResponse(_message.Message):
    __slots__ = ("Text", "State", "Action", "ResourceId")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    Text: str
    State: str
    Action: str
    ResourceId: str
    def __init__(self, Text: _Optional[str] = ..., State: _Optional[str] = ..., Action: _Optional[str] = ..., ResourceId: _Optional[str] = ...) -> None: ...
