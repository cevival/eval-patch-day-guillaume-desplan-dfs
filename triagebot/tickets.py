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
