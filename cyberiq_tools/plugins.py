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
    if not plugin.name.replace("-","").isalnum(): raise ValueError("Invalid plugin name.")
    if plugin.name in _REGISTRY: raise ValueError(f"Plugin already registered: {plugin.name}")
    _REGISTRY[plugin.name]=plugin

def list_plugins() -> list[Plugin]:
    return sorted(_REGISTRY.values(),key=lambda p:p.name)

def run_plugin(name: str, text: str):
    if name not in _REGISTRY: raise ValueError(f"Unknown plugin: {name}")
    return _REGISTRY[name].run(text)
