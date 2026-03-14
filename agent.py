import json
import requests
from elasticsearch import Elasticsearch

ES_URL = "http://localhost:9200"
INDEX = "application-logs-*"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"

es = Elasticsearch(ES_URL)

SYSTEM_PROMPT = """
You generate Elasticsearch 8+ Query DSL.

Rules:
- Output ONLY valid JSON
- No explanation
- No markdown
- No trailing commas
- Use double quotes only
- Must include top-level "query" or "aggs"
- Default size = 10
- If user asks for count, use "size": 0
- Search log text inside the "message" field
- If user asks for first/last timestamp, use "aggs" with "min" and "max" on "@timestamp"
"""

def generate_dsl(user_text):

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text + "\nReturn ONLY valid JSON"}
        ],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    raw = response.json()["message"]["content"].strip()

    raw = raw.replace("```json", "").replace("```", "").strip()

    start = raw.find("{")
    end = raw.rfind("}")

    if start != -1 and end != -1:
        raw = raw[start:end+1]

    try:
        return json.loads(raw)

    except Exception:
        print("\nInvalid JSON from LLM:\n")
        print(raw)
        raise


def run_query(dsl):
    return es.search(index=INDEX, body=dsl)


print("Simple ES AI Agent (type 'exit' to quit)\n")

while True:

    user_input = input("> ")

    if user_input.lower() == "exit":
        break

    try:

        dsl = generate_dsl(user_input)

        print("\nGenerated DSL:")
        print(json.dumps(dsl, indent=2))

        result = run_query(dsl)

        print("\nResults:")

        if "hits" in result:
            total = result["hits"]["total"]["value"]
            print("Total hits:", total)

            for hit in result["hits"]["hits"][:5]:
                src = hit["_source"]

                print({
                    "@timestamp": src.get("@timestamp"),
                    "host": src.get("host", {}).get("hostname"),
                    "file": src.get("log", {}).get("file", {}).get("path")
                })

        if "aggregations" in result:
            print("Aggregations:")
            print(json.dumps(result["aggregations"], indent=2))

        print()

    except Exception as e:
        print("Error:", e)
        print()