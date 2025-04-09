from agi_med_protos import commons_pb2 as _commons_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalAssistantContentRouterRequest(_message.Message):
    __slots__ = ("RequestId", "OuterContext", "ResourceId", "Prompt")
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    OUTERCONTEXT_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    RequestId: str
    OuterContext: _commons_pb2.OuterContextItem
    ResourceId: str
    Prompt: str
    def __init__(self, RequestId: _Optional[str] = ..., OuterContext: _Optional[_Union[_commons_pb2.OuterContextItem, _Mapping]] = ..., ResourceId: _Optional[str] = ..., Prompt: _Optional[str] = ...) -> None: ...

class DigitalAssistantContentRouterResponse(_message.Message):
    __slots__ = ("Interpretation", "ResourceId")
    INTERPRETATION_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    Interpretation: str
    ResourceId: str
    def __init__(self, Interpretation: _Optional[str] = ..., ResourceId: _Optional[str] = ...) -> None: ...
