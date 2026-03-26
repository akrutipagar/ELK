<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Log Analytics Agent — README</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@400;500;600&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --muted: #8b949e;
    --accent: #58a6ff;
    --green: #3fb950;
    --purple: #bc8cff;
    --orange: #ffa657;
    --red: #f85149;
    --tag-bg: #1f6feb26;
    --tag-border: #1f6feb;
    --code-bg: #161b22;
    --inline-code-bg: #6e768166;
  }

  body {
    font-family: 'Inter', -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    font-size: 15px;
    padding: 40px 20px;
  }

  .container {
    max-width: 860px;
    margin: 0 auto;
  }

  /* Header */
  .repo-header {
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--muted);
    font-size: 14px;
    margin-bottom: 24px;
  }
  .repo-header .repo-name {
    color: var(--accent);
    font-weight: 600;
    font-size: 20px;
  }
  .repo-header .slash { color: var(--muted); font-size: 20px; }

  /* Badges */
  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 28px;
  }
  .badge {
    display: inline-flex;
    align-items: center;
    height: 22px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    overflow: hidden;
    border: 1px solid var(--border);
  }
  .badge .label {
    background: #555;
    color: #fff;
    padding: 0 8px;
    height: 100%;
    display: flex;
    align-items: center;
  }
  .badge .value {
    padding: 0 8px;
    height: 100%;
    display: flex;
    align-items: center;
    color: #fff;
  }
  .badge.python .label { background: #3572A5; }
  .badge.python .value { background: #3572A5cc; }
  .badge.llm .label { background: #7C3AED; }
  .badge.llm .value { background: #7C3AEDcc; }
  .badge.es .label { background: #00BFB3; }
  .badge.es .value { background: #00BFB3cc; }
  .badge.status .label { background: #238636; }
  .badge.status .value { background: #238636cc; }

  /* README body */
  .readme {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 32px 40px;
  }

  h1 {
    font-size: 28px;
    font-weight: 600;
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
    margin-bottom: 20px;
    color: var(--text);
  }
  h2 {
    font-size: 20px;
    font-weight: 600;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin: 32px 0 16px;
    color: var(--text);
  }
  h3 {
    font-size: 16px;
    font-weight: 600;
    margin: 20px 0 10px;
    color: var(--text);
  }

  p { margin-bottom: 14px; color: var(--text); }

  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }

  code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    background: var(--inline-code-bg);
    padding: 2px 6px;
    border-radius: 4px;
    color: var(--orange);
  }

  pre {
    background: #010409;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 16px 20px;
    overflow-x: auto;
    margin: 14px 0 20px;
    position: relative;
  }
  pre code {
    background: none;
    padding: 0;
    color: var(--text);
    font-size: 13px;
    line-height: 1.6;
  }
  .lang-tag {
    position: absolute;
    top: 8px;
    right: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--muted);
  }

  /* Terminal demo */
  .terminal {
    background: #010409;
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    margin: 16px 0 20px;
  }
  .terminal-bar {
    background: #161b22;
    border-bottom: 1px solid var(--border);
    padding: 8px 14px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot.r { background: #ff5f57; }
  .dot.y { background: #febc2e; }
  .dot.g { background: #28c840; }
  .terminal-title { margin-left: 8px; font-size: 12px; color: var(--muted); font-family: 'JetBrains Mono', monospace; }
  .terminal-body { padding: 16px 20px; font-family: 'JetBrains Mono', monospace; font-size: 13px; line-height: 1.8; }
  .t-prompt { color: var(--green); }
  .t-input { color: var(--text); }
  .t-label { color: var(--accent); }
  .t-answer { color: #e6edf3; }
  .t-muted { color: var(--muted); }

  /* Pipeline diagram */
  .pipeline {
    display: flex;
    flex-direction: column;
    gap: 0;
    margin: 16px 0 20px;
  }
  .pipe-step {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .pipe-box {
    flex: 1;
    background: #010409;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .pipe-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    background: #21262d;
    border-radius: 4px;
    padding: 2px 7px;
    white-space: nowrap;
  }
  .pipe-label { font-size: 14px; font-weight: 500; color: var(--text); }
  .pipe-sub { font-size: 12px; color: var(--muted); margin-left: auto; font-family: 'JetBrains Mono', monospace; }
  .pipe-arrow {
    display: flex;
    justify-content: center;
    color: var(--muted);
    font-size: 16px;
    padding: 2px 0;
    margin-left: 20px;
  }
  .pipe-step.llm .pipe-box { border-color: #7C3AED88; background: #7C3AED0a; }
  .pipe-step.es .pipe-box { border-color: #00BFB388; background: #00BFB30a; }
  .pipe-step.out .pipe-box { border-color: #238636; background: #2386360a; }

  /* Table */
  table { width: 100%; border-collapse: collapse; margin: 14px 0 20px; font-size: 14px; }
  th { text-align: left; padding: 8px 12px; background: #21262d; color: var(--muted); font-weight: 600; font-size: 13px; border: 1px solid var(--border); }
  td { padding: 8px 12px; border: 1px solid var(--border); color: var(--text); }
  tr:nth-child(even) td { background: #161b2280; }

  /* Callout */
  .callout {
    border-left: 3px solid var(--accent);
    background: #1f6feb14;
    border-radius: 0 6px 6px 0;
    padding: 12px 16px;
    margin: 14px 0 20px;
    font-size: 14px;
    color: var(--muted);
  }
  .callout strong { color: var(--accent); }

  /* Checklist */
  .checklist { list-style: none; padding: 0; margin: 10px 0 20px; }
  .checklist li { padding: 4px 0; font-size: 14px; display: flex; align-items: flex-start; gap: 8px; color: var(--muted); }
  .checklist li .check { color: var(--muted); font-size: 13px; margin-top: 2px; }
  .checklist li.done .check { color: var(--green); }
  .checklist li.done { color: var(--text); }

  /* Author */
  .author-card {
    background: #010409;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    margin-top: 10px;
  }
  .author-avatar {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7C3AED, #1f6feb);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    flex-shrink: 0;
  }
  .author-name { font-weight: 600; font-size: 15px; margin-bottom: 2px; }
  .author-meta { font-size: 13px; color: var(--muted); }
  .author-links { display: flex; gap: 10px; margin-top: 8px; }
  .author-link {
    font-size: 12px;
    padding: 3px 10px;
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--accent);
    text-decoration: none;
    font-family: 'JetBrains Mono', monospace;
  }
  .author-link:hover { background: var(--tag-bg); border-color: var(--accent); }

  hr { border: none; border-top: 1px solid var(--border); margin: 28px 0; }

  ul { padding-left: 20px; margin-bottom: 14px; }
  ul li { margin-bottom: 6px; font-size: 14px; color: var(--text); }

  .highlight-green { color: var(--green); }
  .highlight-purple { color: var(--purple); }
  .highlight-orange { color: var(--orange); }
</style>
</head>
<body>
<div class="container">

  <!-- Repo header -->
  <div class="repo-header">
    <span>akruti-pagar</span>
    <span class="slash">/</span>
    <span class="repo-name">log-analytics-agent</span>
  </div>

  <!-- Badges -->
  <div class="badges">
    <div class="badge python"><span class="label">built with</span><span class="value">Python 3.10+</span></div>
    <div class="badge llm"><span class="label">LLM</span><span class="value">Llama 3 · Ollama</span></div>
    <div class="badge es"><span class="label">search</span><span class="value">Elasticsearch 8</span></div>
    <div class="badge status"><span class="label">status</span><span class="value">active</span></div>
  </div>

  <!-- README body -->
  <div class="readme">

    <h1>Log Analytics Agent — LLM-Driven Observability Assistant</h1>

    <p>A conversational AI agent that lets you investigate application logs in plain English. No Elasticsearch DSL knowledge required — just ask a question and get a plain English answer backed by real log data.</p>

    <!-- Demo terminal -->
    <div class="terminal">
      <div class="terminal-bar">
        <div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
        <span class="terminal-title">es_agent.py</span>
      </div>
      <div class="terminal-body">
        <div><span class="t-prompt">$</span> <span class="t-input">python es_agent.py</span></div>
        <div class="t-muted">ES AI Agent  (type 'exit' to quit)</div>
        <br>
        <div><span class="t-prompt">&gt;</span> <span class="t-input">show me authetication failuers</span></div>
        <div><span class="t-label">🔍 Interpreted as:</span> <span class="t-answer">show authentication failures</span></div>
        <div><span class="t-label">⏳</span> <span class="t-muted">Generating query...</span></div>
        <div><span class="t-label">⏳</span> <span class="t-muted">Querying Elasticsearch...</span></div>
        <div><span class="t-label">⏳</span> <span class="t-muted">Interpreting results...</span></div>
        <br>
        <div><span class="t-label">💬 Answer:</span></div>
        <div class="t-answer">There were 1,075 authentication failures in the logs. Most</div>
        <div class="t-answer">occurred on host web-prod-02 between 02:00–04:00 UTC, with</div>
        <div class="t-answer">the highest concentration targeting the /api/login endpoint,</div>
        <div class="t-answer">suggesting a brute-force attempt.</div>
        <br>
        <div><span class="t-prompt">&gt;</span> <span class="t-input">which host has most errors</span></div>
        <div><span class="t-label">🔍 Interpreted as:</span> <span class="t-answer">which host has the most errors</span></div>
        <div><span class="t-label">💬 Answer:</span></div>
        <div class="t-answer">web-prod-02 accounts for 67% of all error-level logs with</div>
        <div class="t-answer">2,891 entries, followed by api-gateway-01 with 843.</div>
      </div>
    </div>

    <h2>How it works</h2>
    <p>Every question runs through a 3-stage LLM pipeline. All 3 calls use <code>temperature=0</code> for consistent, deterministic output.</p>

    <div class="pipeline">
      <div class="pipe-step">
        <div class="pipe-box">
          <span class="pipe-num">input</span>
          <span class="pipe-label">Your question</span>
          <span class="pipe-sub">messy, typos, abbreviations ok</span>
        </div>
      </div>
      <div class="pipe-arrow">↓</div>
      <div class="pipe-step llm">
        <div class="pipe-box">
          <span class="pipe-num">LLM 1</span>
          <span class="pipe-label">Intent normaliser</span>
          <span class="pipe-sub">normalise_input()</span>
        </div>
      </div>
      <div class="pipe-arrow">↓</div>
      <div class="pipe-step llm">
        <div class="pipe-box">
          <span class="pipe-num">LLM 2</span>
          <span class="pipe-label">DSL generator</span>
          <span class="pipe-sub">generate_dsl()</span>
        </div>
      </div>
      <div class="pipe-arrow">↓</div>
      <div class="pipe-step es">
        <div class="pipe-box">
          <span class="pipe-num">ES</span>
          <span class="pipe-label">Elasticsearch query</span>
          <span class="pipe-sub">application-logs-*</span>
        </div>
      </div>
      <div class="pipe-arrow">↓</div>
      <div class="pipe-step llm">
        <div class="pipe-box">
          <span class="pipe-num">LLM 3</span>
          <span class="pipe-label">Answer interpreter</span>
          <span class="pipe-sub">generate_answer()</span>
        </div>
      </div>
      <div class="pipe-arrow">↓</div>
      <div class="pipe-step out">
        <div class="pipe-box">
          <span class="pipe-num">output</span>
          <span class="pipe-label">Plain English answer</span>
          <span class="pipe-sub">printed to terminal</span>
        </div>
      </div>
    </div>

    <h2>Key design decisions</h2>

    <h3>Why 3 LLM calls instead of 1?</h3>
    <p>A single call trying to understand intent, generate DSL, and explain results produces inconsistent output. Splitting into 3 focused calls — each with its own system prompt and examples — gives each step a single job and makes failures easy to diagnose.</p>

    <h3>Why <code>temperature=0</code>?</h3>
    <p>LLMs are non-deterministic by default. Without it, the same question can generate different DSL on different runs, giving inconsistent counts. Setting <code>temperature=0</code> + <code>top_k=1</code> makes the model always pick the highest-probability token — same input always gives same output.</p>

    <h3>Why few-shot examples in the DSL prompt?</h3>
    <p>Without concrete examples, the LLM improvises query structure. The prompt includes 5 worked examples (count, latest entries, bool filter, aggregation, timestamp range) that lock in the exact JSON pattern to follow.</p>

    <div class="callout">
      <strong>Prompt engineering insight:</strong> A well-structured prompt with explicit field mappings and few-shot examples outperforms a vague prompt on a larger model. The quality of the instruction matters more than the size of the model.
    </div>

    <h2>Tech stack</h2>
    <table>
      <tr><th>Layer</th><th>Technology</th></tr>
      <tr><td>Language</td><td>Python 3.10+</td></tr>
      <tr><td>LLM</td><td>Llama 3 via Ollama (runs locally)</td></tr>
      <tr><td>Search engine</td><td>Elasticsearch 8+</td></tr>
      <tr><td>Log pipeline</td><td>ELK Stack — Filebeat → Logstash → Elasticsearch</td></tr>
      <tr><td>ES client</td><td>elasticsearch-py 8</td></tr>
      <tr><td>HTTP client</td><td>requests</td></tr>
    </table>

    <h2>Setup</h2>

    <h3>Prerequisites</h3>
    <ul>
      <li><a href="https://ollama.ai">Ollama</a> installed and running</li>
      <li>Llama 3 pulled: <code>ollama pull llama3</code></li>
      <li>Elasticsearch 8+ running on <code>localhost:9200</code></li>
      <li>Logs indexed under <code>application-logs-*</code> via ELK stack</li>
    </ul>

    <h3>Install and run</h3>
    <pre><span class="lang-tag">bash</span><code># Clone the repo
git clone https://github.com/akruti-pagar/log-analytics-agent
cd log-analytics-agent

# Install dependencies
pip install elasticsearch requests

# Verify Ollama has llama3
ollama list

# Run the agent
python es_agent.py</code></pre>

    <h3>Configuration</h3>
    <p>Edit the top of <code>es_agent.py</code> to match your setup:</p>
    <pre><span class="lang-tag">python</span><code>ES_URL  = "http://localhost:9200"   # your ES endpoint
INDEX   = "application-logs-*"     # your index pattern
MODEL   = "llama3"                  # match output of `ollama list`</code></pre>

    <div class="callout">
      <strong>Important:</strong> Update the field mappings in <code>DSL_SYSTEM_PROMPT</code> to match your actual log fields. Check your real fields with:<br><br>
      <code>curl http://localhost:9200/application-logs-*/_mapping | python -m json.tool</code>
    </div>

    <h2>Project structure</h2>
    <pre><code>es_agent.py
│
├── Config + OLLAMA_OPTIONS       temperature=0, top_k=1, repeat_penalty
├── INTENT_SYSTEM_PROMPT          fixes typos, expands abbreviations
├── DSL_SYSTEM_PROMPT             field mappings + 5 few-shot examples
├── ANSWER_SYSTEM_PROMPT          plain English answer rules
│
├── normalise_input()             LLM call 1 — clean messy input
├── generate_dsl()                LLM call 2 — produce ES DSL JSON
├── generate_answer()             LLM call 3 — plain English answer
│
├── _call_ollama()                shared HTTP layer, applies OLLAMA_OPTIONS
├── _parse_json_from_llm()        strips markdown fences, extracts JSON block
├── _summarise_result()           compacts ES response before sending to LLM
│
├── run_query()                   executes DSL against Elasticsearch
├── _safe_get()                   safe nested dict traversal
└── main()                        ES ping + REPL loop</code></pre>

    <h2>Roadmap</h2>
    <ul class="checklist">
      <li class="done"><span class="check">✓</span> 3-stage LLM pipeline with intent normalisation</li>
      <li class="done"><span class="check">✓</span> Deterministic output via temperature=0</li>
      <li class="done"><span class="check">✓</span> Few-shot DSL examples for consistency</li>
      <li class="done"><span class="check">✓</span> Plain English answer generation</li>
      <li><span class="check">○</span> REST API via FastAPI for multi-user access</li>
      <li><span class="check">○</span> Auto-generate Kibana dashboards via Saved Objects API</li>
      <li><span class="check">○</span> Elasticsearch authentication (API keys, TLS)</li>
      <li><span class="check">○</span> Query history and audit log</li>
    </ul>

    <h2>What I learned</h2>
    <ul>
      <li><strong>Prompt engineering beats model size</strong> — a focused prompt with explicit field mappings and few-shot examples gives more consistent DSL than a vague prompt on a larger model</li>
      <li><strong>temperature=0 is non-negotiable for structured output</strong> — without it, the same question produces different DSL on consecutive runs</li>
      <li><strong>Pipeline decomposition beats monolithic prompts</strong> — splitting one complex task into 3 focused LLM calls is more reliable and far easier to debug</li>
    </ul>

    <hr>

    <h2>Author</h2>
    <div class="author-card">
      <div class="author-avatar">AP</div>
      <div>
        <div class="author-name">Akruti Pagar</div>
        <div class="author-meta">B.Tech Instrumentation · Cummins College, Pune &nbsp;·&nbsp; IIT Madras Data Science Diploma<br>AWS ML Engineer Associate Certified · AWS Cloud Practitioner</div>
        <div class="author-links">
          <a class="author-link" href="mailto:akruti.pagar03@gmail.com">✉ email</a>
          <a class="author-link" href="#">in/akruti-pagar</a>
          <a class="author-link" href="#">github</a>
        </div>
      </div>
    </div>

  </div>
</div>
</body>
</html>
