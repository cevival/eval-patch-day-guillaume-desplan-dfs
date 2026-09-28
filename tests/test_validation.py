from triagebot.validation import validate_analysis


def test_valid_analysis_is_accepted():
  analysis = {"category": "bug", "severity": 3, "sentiment": "negative", "summary": "Le jeu crash."}
  assert validate_analysis(analysis) is True


def test_unknown_category_is_rejected():
  analysis = {"category": "invalide", "severity": 3, "sentiment": "negative", "summary": "Le jeu crash."}
  assert validate_analysis(analysis) is False


def test_severity_out_of_range_is_rejected():
  analysis = {"category": "bug", "severity": 8, "sentiment": "negative", "summary": "Le jeu crash."}
  assert validate_analysis(analysis) is False


def test_missing_field_is_rejected():
  analysis = {"category": "bug", "severity": 3, "sentiment": "negative"}
  assert validate_analysis(analysis) is False


def test_non_integer_severity_is_rejected():
  analysis = {"category": "bug", "severity": "3", "sentiment": "negative", "summary": "Le jeu crash."}
  assert validate_analysis(analysis) is False


def test_empty_summary_is_rejected():
  analysis = {"category": "bug", "severity": 3, "sentiment": "negative", "summary": "   "}
  assert validate_analysis(analysis) is False
