import json
import sys

from .config import TICKETS_PATH, RESULTS_PATH
from .tickets import load_tickets, TicketLoadError
from .dedup import split_usable_tickets, deduplicate_tickets
from .llm_client import analyze_ticket, OllamaUnavailableError
from .dashboard import print_dashboard
from .drafts import generate_draft


def build_empty_ticket_analysis():
  return {
    "category": "autre",
    "severity": 1,
    "sentiment": "neutral",
    "summary": "Message vide, rien à analyser.",
  }


def process_tickets(tickets):
  usable, unusable = split_usable_tickets(tickets)
  unique_tickets, duplicate_of = deduplicate_tickets(usable)

  analysis_by_id = {}
  status_by_id = {}

  for ticket in unique_tickets:
    analysis, status = analyze_ticket(ticket)
    analysis_by_id[ticket["id"]] = analysis
    status_by_id[ticket["id"]] = status

  for duplicate_id, original_id in duplicate_of.items():
    analysis_by_id[duplicate_id] = analysis_by_id[original_id]
    status_by_id[duplicate_id] = status_by_id[original_id]

  results = []
  for ticket in tickets:
    if ticket["id"] in analysis_by_id:
      analysis = analysis_by_id[ticket["id"]]
      status = status_by_id[ticket["id"]]
    else:
      analysis = build_empty_ticket_analysis()
      status = "skipped_empty"

    draft = generate_draft(ticket, analysis) if status == "ok" else None

    results.append({"ticket": ticket, "analysis": analysis, "status": status, "draft": draft})

  return results


def main():
  try:
    tickets = load_tickets(TICKETS_PATH)
  except TicketLoadError as error:
    print(f"Erreur : {error}")
    sys.exit(1)

  try:
    results = process_tickets(tickets)
  except OllamaUnavailableError as error:
    print(f"Erreur : {error}")
    sys.exit(1)

  with open(RESULTS_PATH, "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False, indent=2)

  print_dashboard(results)
  print(f"\nRésultats enregistrés dans {RESULTS_PATH}")


if __name__ == "__main__":
  main()
