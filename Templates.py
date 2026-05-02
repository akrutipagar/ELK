import re
import copy
import logging

log = logging.getLogger("es_agent")


INTENT_TEMPLATES = [
    {
        "name":     "error count",
        "patterns": [r"how many.*(error|err)", r"count.*error", r"total.*error", r"error.*count"],
        "dsl":      lambda: {"query": {"term": {"log.level": "ERROR"}}, "size": 0},
    },
    {
        "name":     "warn count",
        "patterns": [r"how many.*warn", r"count.*warn", r"total.*warn"],
        "dsl":      lambda: {"query": {"term": {"log.level": "WARN"}}, "size": 0},
    },
    {
        "name":     "authentication failures",
        "patterns": [r"auth.*fail", r"authentication.*failure", r"login.*fail", r"failed.*login"],
        "dsl":      lambda: {"query": {"match_phrase": {"message": "authentication failure"}}, "size": 0},
    },
    {
        "name":     "latest errors",
        "patterns": [r"latest.*error", r"recent.*error", r"show.*error.*log"],
        "dsl":      lambda: {
            "query": {"term": {"log.level": "ERROR"}},
            "size":  10,
            "sort":  [{"@timestamp": {"order": "desc"}}]
        },
    },
    {
        "name":     "errors by host",
        "patterns": [r"error.*by\s+host", r"which\s+host.*error", r"host.*most.*error"],
        "dsl":      lambda: {
            "query": {"term": {"log.level": "ERROR"}},
            "aggs":  {"by_host": {"terms": {"field": "host.hostname", "size": 10}}},
            "size":  0
        },
    },
    {
        "name":     "breakdown by level",
        "patterns": [r"error.*by\s+level", r"count.*by\s+level", r"breakdown.*level"],
        "dsl":      lambda: {
            "aggs": {"by_level": {"terms": {"field": "log.level", "size": 10}}},
            "size": 0
        },
    },
    {
        "name":     "timestamp range",
        "patterns": [r"first.*timestamp", r"last.*timestamp", r"earliest.*log",
                     r"latest.*timestamp", r"time\s+range"],
        "dsl":      lambda: {
            "aggs": {
                "min_time": {"min": {"field": "@timestamp"}},
                "max_time": {"max": {"field": "@timestamp"}}
            },
            "size": 0
        },
    },
    {
        "name":     "latest logs",
        "patterns": [r"latest\s+\d+\s+log", r"recent\s+log", r"show.*latest"],
        "dsl":lambda: {
            "query": {"match_all": {}},
            "size":  10,
            "sort":  [{"@timestamp": {"order": "desc"}}]
        },
    },
]


def match_template(clean: str) -> dict | None:
    
    c = clean.lower().strip()
    for template in INTENT_TEMPLATES:
        for pattern in template["patterns"]:
            if re.search(pattern, c):
                log.info("Template matched: '%s'", template["name"])
                return copy.deepcopy(template["dsl"]())
    return None 



