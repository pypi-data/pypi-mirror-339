from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RunScriptRequest(_message.Message):
    __slots__ = ("scriptPath", "httpRequest", "httpResponse", "isPostScript")
    SCRIPTPATH_FIELD_NUMBER: _ClassVar[int]
    HTTPREQUEST_FIELD_NUMBER: _ClassVar[int]
    HTTPRESPONSE_FIELD_NUMBER: _ClassVar[int]
    ISPOSTSCRIPT_FIELD_NUMBER: _ClassVar[int]
    scriptPath: str
    httpRequest: bytes
    httpResponse: bytes
    isPostScript: bool
    def __init__(self, scriptPath: _Optional[str] = ..., httpRequest: _Optional[bytes] = ..., httpResponse: _Optional[bytes] = ..., isPostScript: bool = ...) -> None: ...

class RunScriptReply(_message.Message):
    __slots__ = ("modifiedRequestToBeSent", "error")
    MODIFIEDREQUESTTOBESENT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    modifiedRequestToBeSent: bytes
    error: str
    def __init__(self, modifiedRequestToBeSent: _Optional[bytes] = ..., error: _Optional[str] = ...) -> None: ...
