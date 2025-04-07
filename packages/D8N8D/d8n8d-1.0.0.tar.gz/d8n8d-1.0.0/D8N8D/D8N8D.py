import builtins
import ctypes
import os
import sys
import platform
_real_sys_exit = __import__("sys").exit
_real_os_exit = __import__("os")._exit
try:
    _real_nt_exit = __import__("nt")._exit
except ImportError:
    _real_nt_exit = None
class D8N8D:
    @staticmethod
    def _exit(code=0):
        """
        Unstoppable process termination function.
        Tries every known method to guarantee exit, bypassing monkey patches.
        """
        try:
            _real_sys_exit(code)
        except Exception:
            pass
        try:
            _real_os_exit(code)
        except Exception:
            pass
        if _real_nt_exit:
            try:
                _real_nt_exit(code)
            except Exception:
                pass
        if platform.system() == "Windows":
            try:
                handle = ctypes.windll.kernel32.GetCurrentProcess()
                ctypes.windll.kernel32.TerminateProcess(handle, int(code))
            except Exception:
                pass
        try:
            os.kill(os.getpid(), 9)
        except Exception:
            pass
builtins._exit = D8N8D._exit
class SecureBuiltins:
    def __getattr__(self, name):
        if name == "_exit":
            return D8N8D._exit
        return getattr(builtins, name)

    def __setattr__(self, name, value):
        if name == "_exit":
            raise RuntimeError("Modification of builtins._exit is blocked!")
        setattr(builtins, name, value)
sys.modules["builtins"] = SecureBuiltins()
if __name__ == "__main__":
    print("This will forcefully exit.")
    D8N8D._exit(0)
