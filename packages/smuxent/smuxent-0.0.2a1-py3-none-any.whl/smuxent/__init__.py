import platform
import importlib
import sys

__doc__ = """ 
Smuxent - A lightweight native threading utility for Python.
Written by me starting from 05/04/2025.

This library provides simple, low-level access to native C++ threads from Python.
It's designed for lightweight concurrency and fire-and-forget execution models,
with minimal amount of tools for managing.

Current Features:
- Run Python functions in detached threads
- Track threads by ID
- Kill individual threads or all running threads
- Check if a thread is still alive
- A demo function (hello_thread) to test the system

Below will be the useable functions and a short description of each
-def basic_thread(func: Callable, *args: Any) -> int: ...
A function that runs a given funtion on a new thread

-def hello_thread(loop_count: int = 1) -> int: ...
A function that print "Hello, Thread!" once every 0.5 seconds for x amount of times

-def is_alive(id: int) -> bool: ...
Returns True if the thread with the given ID is still running

-def kill_thread(id: int) -> None: ...
Kills a specified thread

-def kill_all_threads() -> None: ...
Kills all currently running threads

-def get_all_thread_ids() -> List[int]: ...
Returns a list of all currently running thread IDs

# === Deprecated(added for fun) ===

-def __basic_threadOld(func: Callable, *args: Any) -> None:
    "[Deprecated] Use basic_thread instead. This version does not return a thread ID."

-def __hello_threadOld(loop_count: int = 1) -> None:
    "[Deprecated] Use hello_thread instead. This version does not support thread tracking."




Planned Additions (TODO):
- Thread pool implementation
- Future/promise support for result retrieval
- Message queues or inter-thread channels
- Shared memory
- Event-driven threading pattern

This project was built for fun, learning, and utility. If you're using this, thanks!
Feedback and suggestions are welcome though not sure where that'd be.


-- Patryk Wrzesniewski
""" 

def _detect_thread_module_name():
    system = platform.system()
    arch = platform.architecture()[0]
    pyver = f"{sys.version_info.major}{sys.version_info.minor}"

    if system != "Windows":
        raise ImportError("Smuxent only supports Windows for now.")

    suffix = "64" if "64" in arch else "32"
    return f"py{pyver}ThreadWin{suffix}"

# Import the correct native module
_threadmod = importlib.import_module(f"smuxent.{_detect_thread_module_name()}")

# Optional: expose functions directly through smuxent
basic_thread = _threadmod.basic_thread
hello_thread = _threadmod.hello_thread
is_alive = _threadmod.is_alive
kill_thread = _threadmod.kill_thread
kill_all_threads = _threadmod.kill_all_threads
get_all_thread_ids = _threadmod.get_all_thread_ids

# For debugging
def get_loaded_native_module():
    return _threadmod
