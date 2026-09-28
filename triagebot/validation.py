from .config import CATEGORIES, SENTIMENTS, MIN_SEVERITY, MAX_SEVERITY

REQUIRED_FIELDS = ["category", "severity", "sentiment", "summary"]


def validate_analysis(analysis):
  if not isinstance(analysis, dict):
    return False

  for field in REQUIRED_FIELDS:
    if field not in analysis:
      return False

  if analysis["category"] not in CATEGORIES:
    return False

  if analysis["sentiment"] not in SENTIMENTS:
    return False

  severity = analysis["severity"]
  if not isinstance(severity, int) or isinstance(severity, bool):
    return False
  if severity < MIN_SEVERITY or severity > MAX_SEVERITY:
    return False

  if not isinstance(analysis["summary"], str) or not analysis["summary"].strip():
    return False

  return True
