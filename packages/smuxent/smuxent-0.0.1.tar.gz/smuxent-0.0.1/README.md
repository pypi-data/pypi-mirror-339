# Smuxent
v0.0.1
**Smuxent** is a lightweight native threading module for Python, backed by C++ and pybind11.  
It allows you to easily launch background threads in Python using true native threads — with cooperative control and ID tracking.

This project was built for fun, learning, and utility. If you're using this, thanks!
Feedback and suggestions are welcome though not sure where that'd be.

> Currently supports: **Python 3.12.2** on **Windows (x64 and x86)**

---

## What It Does

- Run Python functions in detached threads
- Track threads by ID
- Kill individual threads or all running threads
- Track thread IDs and check if they are alive
- Automatically loads the correct native extension based on system architecture

---

## Example

```python
from Smuxent import hello_thread, basic_thread

hello_thread(3)  # prints "Hello, Thread!" three times on another thread

def my_func():
    print("Running on another thread")

thread_id = basic_thread(my_func)  # runs my_func() on another thread, returning the thread ID