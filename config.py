import os
import sys

def get_env(key: str, default: int) -> int:
    val = os.getenv(key, str(default))
    if not val.isdigit() or int(val) < 1:
        sys.exit(f"Config error: {key} must be a positive integer, got {val!r}")
    return int(val)

def get_url(key: str, default: str) -> str:
    val = os.getenv(key, default)
    if not val.startswith("http"):
        sys.exit(f"Config error: {key} must start with http, got {val!r}")
    return val


ES_URL         = get_url("ES_URL","http://localhost:9200")
INDEX          = os.getenv("ES_INDEX","application-logs-*")
OLLAMA_URL     = get_url("OLLAMA_URL","http://localhost:11434/api/chat")
MODEL          = os.getenv("OLLAMA_MODEL","llama3")
OLLAMA_TIMEOUT = get_env("OLLAMA_TIMEOUT",60)
ES_TIMEOUT     = get_env("ES_TIMEOUT",10)
MAX_SIZE       = get_env("MAX_SIZE",100)
DEFAULT_HOURS  = get_env("DEFAULT_HOURS",24)

OLLAMA_OPTIONS = {
    "temperature":    0,
    "top_k":          1,
    "top_p":          1,
    "repeat_penalty": 1.1,
}

ALLOWED_TOP_KEYS = {"query", "aggs", "size", "sort", "from", "_source"}
BLOCKED_DSL_KEYS = {
    "script", "script_score", "function_score",
    "pinned", "percolate", "wrapper", "more_like_this"
}