import json
import re
import sys
import requests
from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import exceptions as es_exceptions
from elasticsearch.exceptions import ApiError, TransportError

ES_URL         = "http://localhost:9200"
INDEX          = "application-logs-*"
OLLAMA_URL     = "http://localhost:11434/api/chat"
MODEL          = "llama3:latest"
OLLAMA_TIMEOUT = 60  
ES_TIMEOUT     = 10   

INTENT_SYSTEM_PROMPT = """
You are a log query intent parser for an application log search system.
 
The user may type messy, incomplete, or gibberish queries. Your job is to extract
the intent and rewrite it as a clean, precise log search question.
 
Available log fields you can reference:
- message          → the log text content
- @timestamp       → when the log was created
- host.hostname    → which server/host
- log.level        → severity (ERROR, WARN, INFO, DEBUG)
- log.file.path    → which log file
 
Rules:
- Output ONLY the cleaned question as plain text — no JSON, no explanation
- Preserve all important keywords (error names, hostnames, status codes, actions)
- Infer intent from partial words: "authn fail" → "authentication failures",
  "err" → "errors", "cnt" or "cnt" → "count", "lst" → "list"
- If the user seems to want a count, include "count" in the cleaned question
- If the user seems to want recent entries, include "latest" or "recent"
- If the input is completely uninterpretable, output: UNCLEAR
""".strip()

DSL_SYSTEM_PROMPT = """
You generate Elasticsearch 8+ Query DSL.

Rules:
- Output ONLY valid JSON — no explanation, no markdown, no trailing commas
- Use double quotes only
- Top-level key must be "query" or "aggs" (or both)
- Default size = 10; if user asks for a count use "size": 0
- Search log text in the "message" field
- For first/last timestamp use "aggs" with "min"/"max" on "@timestamp"
- For breakdowns/groupings use "terms" aggregation on the relevant field
- Always include "size" explicitly
""".strip()

ANSWER_SYSTEM_PROMPT = """
You are a log analysis assistant. You are given:
1. A user's question about application logs
2. The Elasticsearch results that answer it

Your job is to answer the user's question in clear, concise plain English.

Rules:
- Be direct and specific — include actual numbers, hostnames, error messages from the data
- If there are log entries, summarize the key patterns you see (common errors, affected hosts, time range)
- If it's just a count, state it naturally e.g. "There were 1,075 authentication failures"
- If there are aggregations, explain what they show
- Keep it to 3-5 sentences max unless the data warrants more
- Do not mention Elasticsearch, DSL, or JSON in your answer
- If results are empty, say so clearly and suggest why
""".strip()

def normalise_input(user_text: str) -> str:
   
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": INTENT_SYSTEM_PROMPT},
            {"role": "user",   "content": user_text},
        ],
        "stream": False,
    }
    cleaned = _call_ollama(payload).strip()
    return cleaned

def generate_dsl(user_text: str) -> dict:
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": DSL_SYSTEM_PROMPT},
            {"role": "user",   "content": f"{user_text}\nReturn ONLY valid JSON"},
        ],
        "stream": False,
    }
    raw = _call_ollama(payload)
    return _parse_json_from_llm(raw)


def generate_answer(user_question: str, es_result: dict) -> str:
    

    summary = _summarise_result(es_result)

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
            {"role": "user", "content": (
                f"User question: {user_question}\n\n"
                f"Elasticsearch results:\n{summary}"
            )},
        ],
        "stream": False,
    }
    return _call_ollama(payload)


def _summarise_result(result: dict) -> str:
   
    lines = []

    hits_block = result.get("hits", {})
    if hits_block:
        total = hits_block.get("total", {}).get("value", 0)
        lines.append(f"Total matching documents: {total}")

        hits = hits_block.get("hits", [])
        if hits:
            lines.append(f"\nTop {len(hits)} log entries:")
            for hit in hits:
                src = hit.get("_source", {})
                entry = {
                    "timestamp": src.get("@timestamp"),
                    "host":      _safe_get(src, "host", "hostname"),
                    "level":     src.get("log", {}).get("level") or src.get("level"),
                    "file":      _safe_get(src, "log", "file", "path"),
                    "message":   src.get("message", "")[:200],
                }
                entry = {k: v for k, v in entry.items() if v}
                lines.append(json.dumps(entry))

    if "aggregations" in result:
        lines.append("\nAggregations:")
        lines.append(json.dumps(result["aggregations"], indent=2))

    return "\n".join(lines) if lines else "No results returned."


def _call_ollama(payload: dict) -> str:
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError(f"Ollama did not respond within {OLLAMA_TIMEOUT}s")
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc

    return response.json()["message"]["content"].strip()


def _parse_json_from_llm(raw: str) -> dict:
   
    raw = re.sub(r"```(?:json)?", "", raw).strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM output:\n{raw}")
    try:
        return json.loads(match.group())
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM returned invalid JSON:\n{match.group()}") from exc


def run_query(es: Elasticsearch, dsl: dict) -> dict:
    try:
        return es.search(index=INDEX, **dsl, request_timeout=ES_TIMEOUT)
    except Exception as exc:
        raise RuntimeError(f"Elasticsearch error: {exc}") from exc



def _safe_get(doc: dict, *keys, default=None):
    for key in keys:
        if not isinstance(doc, dict):
            return default
        doc = doc.get(key, default)
    return doc


def main() -> None:
    es = Elasticsearch(ES_URL)

    if not es.ping():
        sys.exit(f"Cannot reach Elasticsearch at {ES_URL}")

    print("ES AI Agent  (type 'exit' to quit)\n")

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "exit":
            break

        try:
            
            
            dsl = generate_dsl(user_input)
            print(json.dumps(dsl, indent=2))

            result = run_query(es, dsl)

            answer = generate_answer(user_input, result)

            print(answer)
            print()

        except (RuntimeError, ValueError) as exc:
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    main()