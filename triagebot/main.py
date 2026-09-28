import json

from .config import TICKETS_PATH, RESULTS_PATH
from .tickets import load_tickets
from .llm_client import ask_llm_for_analysis


def main():
  tickets = load_tickets(TICKETS_PATH)

  results = []
  for ticket in tickets:
    analysis = ask_llm_for_analysis(ticket)
    results.append({"ticket": ticket, "analysis": analysis})

  with open(RESULTS_PATH, "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False, indent=2)

  print(f"{len(results)} tickets analysés. Résultats enregistrés dans {RESULTS_PATH}")


if __name__ == "__main__":
  main()
