from .script_service import ScriptService
import grpc
from .proto import script_pb2_grpc


class ScriptServer:
    def __init__(self,script_service:ScriptService):
        self.server = grpc.aio.server()
        script_pb2_grpc.add_ScriptServicer_to_server(script_service, self.server)

        self.port = self.server.add_insecure_port("127.0.0.1:0")

    async def run(self):
        await self.server.start()

    async def wait_for_termination(self):
        await self.server.wait_for_termination()
