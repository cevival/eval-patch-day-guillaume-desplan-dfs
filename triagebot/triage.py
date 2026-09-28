from .llm_client import analyze_ticket
from .cache import get_cached_analysis, save_analysis
from .security import looks_like_prompt_injection
from .drafts import generate_draft


def analyze_with_cache(ticket, cache_connection):
  cached_analysis = get_cached_analysis(cache_connection, ticket["player"], ticket["message"])
  if cached_analysis is not None:
    return cached_analysis, "ok"

  analysis, status = analyze_ticket(ticket)
  if status == "ok":
    save_analysis(cache_connection, ticket["player"], ticket["message"], analysis)

  return analysis, status


def triage_ticket(ticket, cache_connection):
  """Traite un ticket exploitable : analyse (cache ou LLM), contrôle anti-manipulation et brouillon."""
  analysis, status = analyze_with_cache(ticket, cache_connection)

  if looks_like_prompt_injection(ticket["message"]):
    status = "to_check"

  draft = generate_draft(ticket, analysis)
  return analysis, status, draft
