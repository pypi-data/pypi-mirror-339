from pathlib import Path
import grpc
from .proto.yasc_pb2 import RawHttpRequest, FetchSmtpMessagesRequest, SetScriptServerPortRequest, SetScriptsDirRequest
from .proto.yasc_pb2_grpc import YascStub


class YascClient:

    def __init__(self, yasc_server_port:int, scripts_dir:Path):
        self.scripts_dir = scripts_dir

        self.channel = grpc.insecure_channel('127.0.0.1:'+str(yasc_server_port))
        self.yasc_service = YascStub(self.channel)

    def send_raw_request(self, base_url, req, needs_response):
        reply = self.yasc_service.SendRawHttpRequest(
            RawHttpRequest(baseUrl=base_url, request=req, needsResponse=needs_response)
        )
        return reply

    def fetch_smtp_messages(self, index=-1):
        reply = self.yasc_service.FetchSmtpMessages(
            FetchSmtpMessagesRequest(index=index)
        )
        return reply

    def set_script_server_port(self, port: int):
        reply = self.yasc_service.SetScriptServerPort(
            SetScriptServerPortRequest(port=port)
        )
        return reply

    def set_scripts_dir(self, scripts_dir: str):
        reply = self.yasc_service.SetScriptsDir(
            SetScriptsDirRequest(scriptsDir=scripts_dir)
        )
        return reply

    def close(self):
        self.channel.close()
