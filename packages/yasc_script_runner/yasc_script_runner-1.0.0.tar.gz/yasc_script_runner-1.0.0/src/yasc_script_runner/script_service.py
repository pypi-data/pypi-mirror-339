from importlib import import_module, reload
from pathlib import Path
from traceback import format_exc

from .yasc_client import YascClient
from .proto.script_pb2 import RunScriptReply, RunScriptRequest
from .proto.script_pb2_grpc import ScriptServicer
from sys import path


class ScriptService(ScriptServicer):
    def __init__(self, yasc_client: YascClient, scripts_dir:Path):
        super().__init__()
        self.yasc_client = yasc_client
        self.scripts_dir = scripts_dir
        path.append(str(scripts_dir.parent))
    
    async def RunScript(self, request, context):
        return await self.run_script(request)

    async def run_script(
        self, run_script_request: "RunScriptRequest"
    ) -> "RunScriptReply":

        script_path = Path(run_script_request.scriptPath)
        script_name = script_path.stem

        try:
            script = import_module(f"{self.scripts_dir.name}.{script_name}")

            result = script.run(
                self.yasc_client,
                run_script_request.httpRequest,
                run_script_request.httpResponse,
                run_script_request.isPostScript,
            )
        except Exception as e:
            error = format_exc()
            print(f"[!] Error\n{error}\n")
            return RunScriptReply(error=error)

        return RunScriptReply(modifiedRequestToBeSent=result)


