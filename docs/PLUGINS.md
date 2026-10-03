# Plugin Guide

A plugin is a named callable that accepts supplied text and returns structured data.

```python
from cyberiq_tools.plugins import Plugin, register

def my_parser(text: str) -> dict:
    return {"characters": len(text)}

register(Plugin("my-parser", "Example local parser.", my_parser))
```

Keep plugins deterministic, offline where practical, and suitable for owned, lab, CTF, educational, defensive, or explicitly authorized data.
