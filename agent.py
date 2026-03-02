import json
import requests
from elasticsearch import Elasticsearch

ES_URL = "http://localhost:9200"
INDEX = "application-logs-*"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"

es = Elasticsearch(ES_URL)

SYSTEM_PROMPT = """
Convert the user request into valid Elasticsearch Query DSL JSON.
Return ONLY JSON. No explanations.

Rules:
- Must include "query".
- Default size = 10.
- If user asks "top N", use aggregation and set size = 0.
- If time mentioned (last 15 minutes, 1 hour), use @timestamp range.
- Do not use delete/update/script.
"""

def generate_dsl(user_text):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    text = response.json()["message"]["content"]

    text = text.strip().replace("```json", "").replace("```", "").strip()

    return json.loads(text)

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
        total = result["hits"]["total"]["value"]
        print("Total hits:", total)

        for hit in result["hits"]["hits"][:5]:
            print(hit["_source"])

        print()

    except Exception as e:
        print("Error:", e)
        print()