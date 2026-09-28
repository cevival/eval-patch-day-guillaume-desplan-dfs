def is_usable(ticket):
  message = ticket.get("message", "")
  return bool(message and message.strip())


def split_usable_tickets(tickets):
  """Sépare les tickets exploitables (message non vide) des autres."""
  usable = []
  unusable = []
  for ticket in tickets:
    if is_usable(ticket):
      usable.append(ticket)
    else:
      unusable.append(ticket)
  return usable, unusable


def deduplicate_tickets(tickets):
  """Regroupe les tickets qui ont le même joueur et le même message.

  Retourne la liste des tickets uniques à analyser, ainsi qu'un dictionnaire
  qui associe l'id de chaque ticket dupliqué à l'id du ticket original.
  """
  unique_tickets = []
  seen = {}
  duplicate_of = {}

  for ticket in tickets:
    key = (ticket.get("player"), ticket.get("message"))
    if key in seen:
      duplicate_of[ticket["id"]] = seen[key]
    else:
      seen[key] = ticket["id"]
      unique_tickets.append(ticket)

  return unique_tickets, duplicate_of
