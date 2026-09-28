import json
import sys

from .config import TICKETS_PATH, RESULTS_PATH, REPORT_PATH
from .tickets import load_tickets, remove_malformed_entries, TicketLoadError
from .dedup import split_usable_tickets, deduplicate_tickets
from .llm_client import analyze_ticket, OllamaUnavailableError
from .dashboard import print_dashboard
from .drafts import generate_draft
from .escalation import get_escalation
from .report import write_report


def build_empty_ticket_analysis():
  return {
    "category": "autre",
    "severity": 1,
    "sentiment": "neutral",
    "summary": "Ticket vide ou incomplet, rien à analyser.",
  }


def process_tickets(tickets):
  usable, _ = split_usable_tickets(tickets)
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

    escalation = get_escalation(status, analysis)
    draft = generate_draft(ticket, analysis) if status == "ok" else None

    results.append({
      "ticket": ticket,
      "analysis": analysis,
      "status": status,
      "escalation": escalation,
      "draft": draft,
    })

  return results


def main():
  tickets_path = sys.argv[1] if len(sys.argv) > 1 else TICKETS_PATH

  try:
    tickets = load_tickets(tickets_path)
  except TicketLoadError as error:
    print(f"Erreur : {error}")
    sys.exit(1)

  tickets, ignored_count = remove_malformed_entries(tickets)
  if ignored_count:
    print(f"Attention : {ignored_count} entrée(s) mal formée(s) ignorée(s) (pas un ticket ou pas d'id).")

  try:
    results = process_tickets(tickets)
  except OllamaUnavailableError as error:
    print(f"Erreur : {error}")
    sys.exit(1)

  with open(RESULTS_PATH, "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False, indent=2)

  write_report(results, REPORT_PATH)
  print_dashboard(results)
  print(f"\nRésultats enregistrés dans {RESULTS_PATH}")
  print(f"Rapport enregistré dans {REPORT_PATH}")


if __name__ == "__main__":
  main()
