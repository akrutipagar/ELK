import json
import logging
from config import DEFAULT_HOURS
from redactor import redact
from ES import safe_get

log = logging.getLogger("es_agent")

def summarise_result(result: dict) -> str:
    lines = []
    hits_block = result.get("hits", {})

    if hits_block:
        total = hits_block.get("total", {}).get("value", 0)
        lines.append(f"Total matching documents: {total}")
        hits = hits_block.get("hits", [])
        if hits:
            lines.append(len(hits))
            for hit in hits:
                sourse = hit.get("_source", {})
                entry = {
                    "timestamp": sourse.get("@timestamp"),
                    "host":safe_get(sourse, "host", "hostname"),
                    "level":sourse.get("log", {}).get("level") or sourse.get("level"),
                    "message":redact(sourse.get("message", "")[:200]),
                }
                entry = {k: v for k, v in entry.items() if v}
                lines.append(json.dumps(entry))

    if "aggregations" in result:
        lines.append("\nAggregations:")
        lines.append(json.dumps(result["aggregations"], indent=2))

    return "\n".join(lines) if lines else "No results returned."


def format_answer(clean: str, result: dict) -> str | None:
    
    hits_block = result.get("hits", {})
    total= hits_block.get("total", {}).get("value")
    hits= hits_block.get("hits", [])
    aggs= result.get("aggregations", {})

    
    if total is not None and not hits and not aggs:
        return f"There were {total:,} matching log entries in the last {DEFAULT_HOURS} hours."

    
    if "min_time" in aggs and "max_time" in aggs:
        mn = aggs["min_time"].get("value_as_string", aggs["min_time"].get("value", "unknown"))
        mx = aggs["max_time"].get("value_as_string", aggs["max_time"].get("value", "unknown"))
        return f"Logs span from {mn} to {mx}."

    
    for agg_name, agg_val in aggs.items():
        buckets = agg_val.get("buckets", [])
        if buckets:
            lines = [f"Breakdown by '{agg_name}':"]
            for b in buckets[:10]:
                lines.append(f"  {b.get('key', '?')}: {b.get('doc_count', 0):,}")
            return "\n".join(lines)

    
    if hits and not aggs:
        if total == 0:
            return "No matching log entries found. The search term may not exist in recent logs."
        lines = [f"Found {total:,} entries. Showing latest {len(hits)}:"]
        for h in hits:
            src = h.get("_source", {})
            ts  = src.get("@timestamp", "")[:19]
            lvl = src.get("log", {}).get("level", "")
            msg = redact(src.get("message", ""))[:120]
            lines.append(f"  [{ts}] {lvl} — {msg}")
        return "\n".join(lines)

    return None  