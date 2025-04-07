# D8N8D

A Python library that provides an **D8N8D** function — it forcefully terminates the process, even if common exit methods are monkey-patched or overridden.

---

## 🚀 Features

- Bypasses `sys.exit`, `os._exit`, and `nt._exit` patching.
- Works on **Windows**, **Linux**, and **macOS**.
- Uses low-level system calls to guarantee termination.
- Simple API: `D8N8D.D8N8D._exit(code)`

---

## 📦 Installation

```bash
pip install D8N8D
