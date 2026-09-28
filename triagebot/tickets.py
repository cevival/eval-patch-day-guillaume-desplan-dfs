import json


class TicketLoadError(Exception):
  """Erreur levée quand le fichier de tickets ne peut pas être chargé."""


def load_tickets(path):
  try:
    with open(path, "r", encoding="utf-8") as file:
      tickets = json.load(file)
  except FileNotFoundError:
    raise TicketLoadError(f"Le fichier de tickets '{path}' est introuvable.")
  except json.JSONDecodeError as error:
    raise TicketLoadError(f"Le fichier de tickets '{path}' contient du JSON invalide : {error}")

  if not isinstance(tickets, list):
    raise TicketLoadError("Le fichier de tickets doit contenir une liste de tickets.")

  return tickets


def remove_malformed_entries(tickets):
  """Écarte les entrées qui ne sont pas des tickets (pas un objet JSON, ou pas d'id)."""
  valid_tickets = []
  for ticket in tickets:
    if isinstance(ticket, dict) and "id" in ticket:
      valid_tickets.append(ticket)

  ignored_count = len(tickets) - len(valid_tickets)
  return valid_tickets, ignored_count
