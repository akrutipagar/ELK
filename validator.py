import json
import logging
from config import ALLOWED_TOP_KEYS, BLOCKED_DSL_KEYS, MAX_SIZE

log = logging.getLogger("es_agent")

def validate_dsl(dsl: dict) -> dict:
    
    raw_str = json.dumps(dsl)
    for bad in BLOCKED_DSL_KEYS:
        if bad in raw_str:
            raise ValueError(f"DSL contains blocked key '{bad}' — not allowed")

    bad_keys = set(dsl.keys()) - ALLOWED_TOP_KEYS
    if bad_keys:
        raise ValueError(f"DSL contains disallowed top-level keys: {bad_keys}")

    if "query" not in dsl and "aggs" not in dsl:
        raise ValueError("DSL must contain 'query' or 'aggs'")

    dsl["size"] = min(int(dsl.get("size", 10)), MAX_SIZE)

    log.info("DSL validated OK")
    return dsl