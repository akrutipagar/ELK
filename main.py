import sys
import json
import logging
import requests
from elasticsearch import Elasticsearch
from config import ES_URL, INDEX, DEFAULT_HOURS, OLLAMA_URL
from pipeline import normalise_input, generate_dsl, generate_answer, inject_time_filter
from templates import match_template
from validator import validate_dsl
from es_client import run_query



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("es_agent.log"),
        logging.StreamHandler(sys.stderr),
    ]
)
log = logging.getLogger("es_agent")




def _check_ollama_model() -> None:
    """Warn if configured model is not found in Ollama."""
    try:
        from config import MODEL
        tags_url = OLLAMA_URL.replace("/api/chat", "/api/tags")
        resp = requests.get(tags_url, timeout=5)
        resp.raise_for_status()
        models = [m["name"] for m in resp.json().get("models", [])]
        base = MODEL.split(":")[0]
        if not any(base in m for m in models):
            print(f"Warning: model '{MODEL}' not found. Available: {models}")
            print(f"Run: ollama pull {MODEL}")
    except Exception:
        log.warning("Could not verify Ollama model — proceeding anyway")




def main() -> None:
    es = Elasticsearch(ES_URL)
    if not es.ping():
        sys.exit(f"Cannot reach Elasticsearch at {ES_URL}")

    _check_ollama_model()

    print("ES AI Agent  (type 'exit' to quit)")
    print(f"Default time window: last {DEFAULT_HOURS}h  |  Index: {INDEX}")
    print("Commands: 'show dsl' · 'debug' · 'no time filter'\n")

    show_dsl        = True
    debug_mode      = False
    use_time_filter = True

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

        if user_input.lower() == "show dsl":
            show_dsl = not show_dsl
            print(f"DSL display {'ON' if show_dsl else 'OFF'}\n")
            continue

        if user_input.lower() == "debug":
            debug_mode = not debug_mode
            log.setLevel(logging.DEBUG if debug_mode else logging.INFO)
            print(f"Debug mode {'ON' if debug_mode else 'OFF'}\n")
            continue

        if user_input.lower() == "no time filter":
            use_time_filter = not use_time_filter
            status = f"last {DEFAULT_HOURS}h" if use_time_filter else "all time"
            print(f"Time filter: {status}\n")
            continue

        
        try:
        
            clean = normalise_input(user_input)

            if clean.upper() == "UNCLEAR":
                print(" Could not understand. Try something like:")
                print("'count authentication failures'")
                print("'show latest errors'")
                print("'which host has the most errors'\n")
                continue
            dsl = match_template(clean)
            if dsl:
                dsl = validate_dsl(dsl)
                print("   (matched intent template)")
            else:
                dsl = generate_dsl(clean)

            
            asked_for_time = any(w in clean.lower()
                for w in ["timestamp", "first", "last", "all time", "ever", "oldest"])
            if use_time_filter:
                dsl = inject_time_filter(dsl, asked_for_time)

            if show_dsl:
                print("Generated DSL:")
                print(json.dumps(dsl, indent=2))

            
            result = run_query(es, dsl)

            answer = generate_answer(clean, result)

            print(answer)
            print()

        except (RuntimeError, ValueError) as exc:
            log.error("Pipeline error: %s", exc)
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    main()