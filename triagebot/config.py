import os

# ------ Config générale ------ #
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:3b")

TICKETS_PATH = "data/tickets.json"
RESULTS_PATH = "results.json"
REPORT_PATH = "report.md"

CATEGORIES = ["bug", "payment", "account", "suggestion", "toxicity", "autre"]
SENTIMENTS = ["positive", "neutral", "negative"]
MIN_SEVERITY = 1
MAX_SEVERITY = 5
MAX_ATTEMPTS = 2
