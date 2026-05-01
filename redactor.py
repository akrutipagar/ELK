import re


PATTERNS = [
    (re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'),"[EMAIL]"),
    (re.compile(r'(?i)(password|passwd|token|secret|api_?key)["\s:=]+\S+'),"[REDACTED]"),
    (re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),"[IP]"),
    (re.compile(r'Bearer\s+\S+'),"[TOKEN]"),
    (re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', re.I),"[UUID]"),
    (re.compile(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+'),"[JWT]"),
    (re.compile(r'\b\d{10,}\b'),"[ID]"),
    (re.compile(r'(?i)(at\s+[\w$.]+\([\w.]+:\d+\)\n?){2,}'),"[STACKTRACE]"),
]

def redact(text: str) -> str:
   
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    return text