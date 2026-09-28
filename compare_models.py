"""Compare deux modèles Ollama sur le même jeu de tickets : temps de traitement
et nombre de réponses invalides (avant retry). Résultats et conclusions dans le README."""

import time

from triagebot.config import TICKETS_PATH
from triagebot.tickets import load_tickets
from triagebot.dedup import split_usable_tickets, deduplicate_tickets
from triagebot.llm_client import ask_llm_for_analysis
from triagebot.validation import validate_analysis

MODELS_TO_COMPARE = ["qwen2.5:3b", "qwen2.5:0.5b"]


def compare(tickets):
  results = {}
  for model in MODELS_TO_COMPARE:
    invalid_count = 0
    start = time.perf_counter()
    for ticket in tickets:
      analysis = ask_llm_for_analysis(ticket, model)
      if analysis is None or not validate_analysis(analysis):
        invalid_count += 1
    duration = time.perf_counter() - start
    results[model] = {"duration": duration, "invalid_count": invalid_count}
  return results


if __name__ == "__main__":
  tickets = load_tickets(TICKETS_PATH)
  usable, _ = split_usable_tickets(tickets)
  unique_tickets, _ = deduplicate_tickets(usable)

  results = compare(unique_tickets)

  print(f"Comparaison sur {len(unique_tickets)} tickets uniques :\n")
  for model, stats in results.items():
    print(f"- {model} : {stats['duration']:.1f}s, {stats['invalid_count']} réponse(s) invalide(s)")
