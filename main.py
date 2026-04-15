import sys, json, logging
from elasticsearch import Elasticsearch
from config import ES_URL, INDEX, DEFAULT_HOURS
from pipeline import normalise_input, generate_dsl, generate_answer, inject_time_filter
from templates import match_template
from validator import validate_dsl
from elasticsearch_client import run_query

def main(): ...   # just the REPL loop

if __name__ == "__main__":
    main()