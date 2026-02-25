import json
import os
from typing import Any, Dict, Optional

from elasticsearch import Elasticsearch
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain.tools import StructuredTool
from langchain.agents import AgentExecutor, create_tool_calling_agent

ES_URL = "http://localhost:9200"
DEFAULT_INDEX = "application-logs-*"
MEMORY_FILE = "elk_agent_memory.json"

MAX_SIZE = 50
MAX_RETRIES = 2 

def es_search(index: str, query_json: str) -> Dict[str, Any]:
    """
    Executes ES search and returns trimmed response.
    """
    es = Elasticsearch(ES_URL)
    body = json.loads(query_json)
    resp = es.search(index=index, body=body)

    hits = resp.get("hits", {}).get("hits", [])
    total = resp.get("hits", {}).get("total", {})
    total_val = total.get("value") if isinstance(total, dict) else total

    trimmed = {
        "total_hits": total_val,
        "hits_sample": [h.get("_source", {}) for h in hits[:5]],
        "aggregations": resp.get("aggregations", {}),
        "took_ms": resp.get("took"),
    }
    return trimmed

es_search_tool = StructuredTool.from_function(
    name="es_search",
    description="Run an Elasticsearch _search using a DSL JSON query body.",
    func=es_search,
    args_schema=ESSearchInput,
)

def validate_query_dict(q: Dict[str, Any]) -> Optional[str]:
    """
    Return an error string if query is unsafe/invalid; else None.
    """
    if not isinstance(q, dict):
        return "Query is not a JSON object."

    if "query" not in q:
        return "Missing top-level 'query'."

    size = q.get("size", 10)
    if isinstance(size, int) and size > MAX_SIZE:
        return f"Query 'size' too large ({size}). Max allowed is {MAX_SIZE}."

    # Block script usage (safe for practice)
    q_str = json.dumps(q).lower()
    forbidden = ["script", "_delete", "_update", "delete_by_query", "update_by_query"]
    if any(word in q_str for word in forbidden):
        return "Unsafe query: contains forbidden keywords (script/delete/update)."

    return None

def load_memory() -> Dict[str, Any]:
     if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
     return {}


def save_memory(mem: Dict[str, Any]) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2)


SYSTEM = f"""
You are an Agentic Elasticsearch Query Assistant.

You must help the user query Elasticsearch logs safely and correctly.

Rules:
- When asked to output query JSON, output ONLY valid JSON (no markdown).
- Default index: "{DEFAULT_INDEX}" unless user specifies.
- Default size 10; max size {MAX_SIZE}.
- Use @timestamp for time windows (e.g., last 15 minutes -> now-15m).
- If user asks "top N", use an aggregation (terms) and set size: 0.
- Prefer fields: @timestamp, message, level/severity; but if uncertain, use match_all + sort by @timestamp desc.
- You may call tools to execute the query. You are allowed to refine queries after seeing results.

Safety:
- No delete/update actions.
- No scripts.
"""

# Prompt to GENERATE a DSL query JSON
prompt_generate = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=SYSTEM),
        ("human",
         "User request: {user_request}\n"
         "Recent memory (if any): {memory}\n\n"
         "Create an Elasticsearch Query DSL JSON body ONLY."),
    ]
)

# Prompt to REFINE query if error / zero hits
prompt_refine = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=SYSTEM),
        ("human",
         "User request: {user_request}\n"
         "Previous query JSON: {prev_query}\n"
         "Tool result: {tool_result}\n"
         "Error (if any): {error}\n\n"
         "Refine the query to better answer the request.\n"
         "Return ONLY the new DSL JSON body."),
    ]
)

# Prompt to SUMMARIZE
prompt_summarize = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=SYSTEM),
        ("human",
         "User request: {user_request}\n"
         "Final query JSON: {final_query}\n"
         "Tool result (trimmed): {tool_result}\n\n"
         "Write a clear summary (5-10 lines). "
         "If aggregations exist, summarize top buckets. "
         "If hits exist, show 3 sample messages with timestamps if present."),
    ]
)