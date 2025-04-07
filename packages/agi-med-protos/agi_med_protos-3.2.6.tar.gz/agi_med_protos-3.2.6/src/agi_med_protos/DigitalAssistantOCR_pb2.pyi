from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OCRType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEXT_ONLY: _ClassVar[OCRType]
    TEXT_WITH_TABLES: _ClassVar[OCRType]
    TEXT_WITH_IMAGES: _ClassVar[OCRType]
    TEXT_WITH_TABLES_AND_IMAGES: _ClassVar[OCRType]
TEXT_ONLY: OCRType
TEXT_WITH_TABLES: OCRType
TEXT_WITH_IMAGES: OCRType
TEXT_WITH_TABLES_AND_IMAGES: OCRType

class DigitalAssistantOCRRequest(_message.Message):
    __slots__ = ("RequestId", "ResourceId", "OCRType")
    REQUESTID_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    OCRTYPE_FIELD_NUMBER: _ClassVar[int]
    RequestId: str
    ResourceId: str
    OCRType: OCRType
    def __init__(self, RequestId: _Optional[str] = ..., ResourceId: _Optional[str] = ..., OCRType: _Optional[_Union[OCRType, str]] = ...) -> None: ...

class DigitalAssistantOCRResponse(_message.Message):
    __slots__ = ("Text", "ResourceId")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    RESOURCEID_FIELD_NUMBER: _ClassVar[int]
    Text: str
    ResourceId: str
    def __init__(self, Text: _Optional[str] = ..., ResourceId: _Optional[str] = ...) -> None: ...
