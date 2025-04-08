from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HttpMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GET: _ClassVar[HttpMethod]
    POST: _ClassVar[HttpMethod]
    PUT: _ClassVar[HttpMethod]
    DELETE: _ClassVar[HttpMethod]
    PATCH: _ClassVar[HttpMethod]
GET: HttpMethod
POST: HttpMethod
PUT: HttpMethod
DELETE: HttpMethod
PATCH: HttpMethod

class HttpHeader(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class HttpCookie(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class ParsedHttpRequest(_message.Message):
    __slots__ = ("url", "method", "headers", "body", "needsResponse")
    URL_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    NEEDSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    url: str
    method: HttpMethod
    headers: _containers.RepeatedCompositeFieldContainer[HttpHeader]
    body: str
    needsResponse: bool
    def __init__(self, url: _Optional[str] = ..., method: _Optional[_Union[HttpMethod, str]] = ..., headers: _Optional[_Iterable[_Union[HttpHeader, _Mapping]]] = ..., body: _Optional[str] = ..., needsResponse: bool = ...) -> None: ...

class RawHttpRequest(_message.Message):
    __slots__ = ("baseUrl", "request", "needsResponse")
    BASEURL_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    NEEDSRESPONSE_FIELD_NUMBER: _ClassVar[int]
    baseUrl: str
    request: bytes
    needsResponse: bool
    def __init__(self, baseUrl: _Optional[str] = ..., request: _Optional[bytes] = ..., needsResponse: bool = ...) -> None: ...

class RawHttpResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: bytes
    def __init__(self, response: _Optional[bytes] = ...) -> None: ...

class FetchSmtpMessagesRequest(_message.Message):
    __slots__ = ("index",)
    INDEX_FIELD_NUMBER: _ClassVar[int]
    index: int
    def __init__(self, index: _Optional[int] = ...) -> None: ...

class FetchSmtpMessagesResponse(_message.Message):
    __slots__ = ("conversations",)
    CONVERSATIONS_FIELD_NUMBER: _ClassVar[int]
    conversations: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, conversations: _Optional[_Iterable[str]] = ...) -> None: ...

class SetScriptServerPortRequest(_message.Message):
    __slots__ = ("port",)
    PORT_FIELD_NUMBER: _ClassVar[int]
    port: int
    def __init__(self, port: _Optional[int] = ...) -> None: ...

class SetScriptServerPortReply(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class SetScriptsDirRequest(_message.Message):
    __slots__ = ("scriptsDir",)
    SCRIPTSDIR_FIELD_NUMBER: _ClassVar[int]
    scriptsDir: str
    def __init__(self, scriptsDir: _Optional[str] = ...) -> None: ...

class SetScriptsDirReply(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
