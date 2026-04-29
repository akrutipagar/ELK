import re
import json
import time
import logging
import requests
from config import OLLAMA_URL, OLLAMA_TIMEOUT, MODEL, OLLAMA_OPTIONS

log = logging.getLogger("es_agent")

def call_ollama(system_prompt: str,user_content: str, _retry: int = 1) -> str:
    payload = {
        "model":MODEL,
        "stream":False,
        "options":OLLAMA_OPTIONS,
        "messages":[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_content},
        ],
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload,timeout=OLLAMA_TIMEOUT)
        response.raise_for_status()
        return response.json()["message"]["content"].strip()

    except requests.exceptions.Timeout:
        if _retry > 0:
            log.warning("Ollama timeout — retrying once")
            time.sleep(2)
            return call_ollama(system_prompt, user_content, _retry - 1)
        raise RuntimeError(f"Ollama did not respond within {OLLAMA_TIMEOUT}s after retry")

    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Cannot connect to Ollama at {OLLAMA_URL}.")

    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(
            f"Ollama returned HTTP {exc.response.status_code}.") from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc


def parse_json_from_llm(raw: str) -> dict:
    
    raw = re.sub(r"```(?:json)?", "", raw).strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM output")
    try:
        return json.loads(match.group())
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM returned invalid JSON") from exc