from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Plugin:
    name: str
    description: str
    run: Callable[[str],Any]

_REGISTRY: dict[str,Plugin]={}

def register(plugin: Plugin) -> None:
    if not isinstance(plugin,Plugin): raise TypeError("plugin must be a Plugin instance.")
    if not plugin.name or not plugin.name.replace("-","").isalnum(): raise ValueError("Invalid plugin name.")
    if not plugin.description.strip(): raise ValueError("Plugin description cannot be empty.")
    if not callable(plugin.run): raise TypeError("Plugin run handler must be callable.")
    if plugin.name in _REGISTRY: raise ValueError(f"Plugin already registered: {plugin.name}")
    _REGISTRY[plugin.name]=plugin

def list_plugins() -> list[Plugin]:
    return sorted(_REGISTRY.values(),key=lambda p:p.name)

def run_plugin(name: str, text: str):
    if name not in _REGISTRY: raise ValueError(f"Unknown plugin: {name}")
    try:
        return _REGISTRY[name].run(text)
    except Exception as exc:
        raise RuntimeError(f"Plugin {name} failed: {exc}") from exc
