def get_escalation(status, analysis):
  """Détermine qui doit traiter le ticket, de façon déterministe (sans LLM)."""
  if status == "to_check":
    return "relecture_humaine"

  if analysis["category"] == "toxicity":
    return "moderation"

  if analysis["category"] == "payment" and analysis["severity"] >= 4:
    return "responsable_support"

  return "standard"
