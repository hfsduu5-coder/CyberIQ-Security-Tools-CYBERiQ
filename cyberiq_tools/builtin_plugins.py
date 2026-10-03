from .core import header_review, indicators, log_summary, url_inventory
from .plugins import Plugin, register

def load_builtin_plugins() -> None:
    builtins=(
      Plugin("headers","Review saved HTTP headers.",header_review),
      Plugin("indicators","Count indicator-like patterns.",indicators),
      Plugin("logs","Summarize saved logs.",log_summary),
      Plugin("urls","Inventory URLs from saved text.",url_inventory),
    )
    for p in builtins:
        try: register(p)
        except ValueError: pass
