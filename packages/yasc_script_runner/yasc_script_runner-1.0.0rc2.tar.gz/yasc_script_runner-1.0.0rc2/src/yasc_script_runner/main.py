import argparse
import asyncio
from os import getenv
from pathlib import Path
from signal import SIGINT, SIGTERM, signal
from .watchdog_handler import WatchdogHandler
from .yasc_client import YascClient
from .script_service import ScriptService
from .script_server import ScriptServer
from watchdog.observers import polling
from importlib.metadata import version


async def run(yasc_client: YascClient, scripts_dir: Path):
    script_service=ScriptService(yasc_client, scripts_dir)
    server = ScriptServer(script_service)
    port = server.port
    await server.run()
    print(f"[*] Listening on {port}.")

    reply = yasc_client.set_script_server_port(port)
    if not reply.success:
        print("[!] Yasc server refused connection.")
        return
    print("[+] Connected to Yasc server.")

    yasc_client.set_scripts_dir(str(scripts_dir))
    print(f"[+] Set scripts dir to {scripts_dir}.")

    print(f"[*] Waiting requests from Yasc server...")

    await server.wait_for_termination()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--yasc-server-port", dest='yasc_server_port', default=getenv('YASC_SERVER_PORT'), help="Yasc server's port")
    parser.add_argument("-d", "--scripts-dir", dest='scripts_dir', default=getenv('YASC_SCRIPTS_DIR'), help="Scripts directory")
    parser.add_argument("--disable-watchdog", dest='disable_watchdog', action='store_true', help="Disable watchdog")
    parser.add_argument("-v","--version", action='version', version=version('yasc_script_runner'))
    args = parser.parse_args()

    if not args.yasc_server_port:
        print("[!] Yasc server's port: not given")
        exit(1)

    try:
        yasc_server_port = int(args.yasc_server_port)
    except ValueError:
        print(f"[!] Yasc server's port: invalid int value")
        exit(1)


    if not args.scripts_dir:
        print("[!] Scripts directory: not given")
        exit(1)

    scripts_dir = Path(args.scripts_dir)
    resolved_scripts_dir = scripts_dir.resolve()
    if not resolved_scripts_dir.is_dir():
        print(f"[!] Scripts directory: not found: {resolved_scripts_dir}")
        return

    if not args.disable_watchdog:
        event_handler = WatchdogHandler()
        observer = polling.PollingObserver()
        observer.schedule(event_handler, str(resolved_scripts_dir), recursive=False)
        observer.start()

    yasc_client = YascClient(yasc_server_port, resolved_scripts_dir)

    def signal_handler(s,f):
        yasc_client.close()

        if not args.disable_watchdog:
            observer.stop()
        
        print("[*] Stopped.")
        exit(0)
    signal(SIGINT,signal_handler)
    signal(SIGTERM,signal_handler)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(yasc_client, resolved_scripts_dir))