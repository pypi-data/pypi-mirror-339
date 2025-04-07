from watchdog.events import FileSystemEvent, FileSystemEventHandler
from importlib import import_module, reload
from pathlib import Path


class WatchdogHandler(FileSystemEventHandler):

    def reload_module(self, src_path_str: str):
        if not src_path_str.endswith(".py"):
            return

        try:
            src_path = Path(src_path_str)
            script_file_name = src_path.stem
            script_dir_name = src_path.parent.name
            reload(import_module(f"{script_dir_name}.{script_file_name}"))
        except Exception as e:
            print(f"[!] Error\n{e}\n")

    def on_created(self, event: FileSystemEvent) -> None:
        self.reload_module(event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        self.reload_module(event.src_path)

