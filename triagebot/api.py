from flask import Flask, request, jsonify

from .dedup import is_usable
from .llm_client import OllamaUnavailableError
from .cache import init_cache
from .triage import triage_ticket
from .escalation import get_escalation

app = Flask(__name__)


@app.post("/triage")
def triage():
  ticket = request.get_json(silent=True)

  if not is_usable(ticket):
    return jsonify({"error": "Le ticket doit contenir un 'player' et un 'message' texte non vide."}), 400

  cache_connection = init_cache()
  try:
    analysis, status, draft = triage_ticket(ticket, cache_connection)
  except OllamaUnavailableError as error:
    return jsonify({"error": str(error)}), 503
  finally:
    cache_connection.close()

  return jsonify({
    "status": status,
    "analysis": analysis,
    "escalation": get_escalation(status, analysis),
    "draft": draft,
  })


if __name__ == "__main__":
  app.run(debug=True)
