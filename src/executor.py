import ctypes
import sys
import threading
import traceback
from pathlib import Path, PureWindowsPath

from utils import logger_print


class ExecutorThread(threading.Thread):
    def __init__(self, name="ExecT1", *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.name = name

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit)
        )
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


class Executor:
    def add_script_workdir(self, file_path: str):
        """Add Executing script path for relative imports"""
        path = Path(file_path)
        parent_dir_path = PureWindowsPath(path.parent)
        sys.path.insert(0, str(parent_dir_path))

    def remove_script_workdir(self):
        """Clear Executing script after execution"""
        sys.path.pop(0)

    def execute_python_script(self, file_path: str):
        """Read the script file and pass to exec()"""
        self.add_script_workdir(file_path)
        logger_print(f"> Running script: {file_path}")

        try:
            with open(file_path) as file:
                try:
                    exec(file.read(), globals())
                except SystemExit as exc:
                    traceback.print_exception(exc)
                    logger_print(
                        "> Failed to complete :( \nSystem Exited or Stopped by user."
                    )
                except Exception as exc:
                    traceback.print_exception(exc)
                    logger_print("> Failed to complete :( ")
                else:
                    logger_print("> Successfully executed script")
        except:
            logger_print("> [ERROR] File Not Found. Please check the file again")
        self.remove_script_workdir()
        print("\n\n")
