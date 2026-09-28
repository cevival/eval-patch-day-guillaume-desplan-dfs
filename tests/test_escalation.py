from triagebot.escalation import get_escalation


def test_to_check_status_goes_to_human_review():
  assert get_escalation("to_check", None) == "relecture_humaine"


def test_toxicity_goes_to_moderation():
  analysis = {"category": "toxicity", "severity": 2, "sentiment": "negative", "summary": "Insultes"}
  assert get_escalation("ok", analysis) == "moderation"


def test_urgent_payment_goes_to_support_lead():
  analysis = {"category": "payment", "severity": 4, "sentiment": "negative", "summary": "Débit multiple"}
  assert get_escalation("ok", analysis) == "responsable_support"


def test_non_urgent_payment_stays_standard():
  analysis = {"category": "payment", "severity": 2, "sentiment": "negative", "summary": "Question de facturation"}
  assert get_escalation("ok", analysis) == "standard"


def test_standard_ticket_goes_to_standard_flow():
  analysis = {"category": "bug", "severity": 2, "sentiment": "negative", "summary": "Petit bug"}
  assert get_escalation("ok", analysis) == "standard"
