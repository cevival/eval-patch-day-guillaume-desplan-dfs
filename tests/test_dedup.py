from triagebot.dedup import is_usable, deduplicate_tickets
from triagebot.tickets import remove_malformed_entries


def test_empty_message_is_not_usable():
  assert is_usable({"id": 1, "player": "A", "message": "   "}) is False


def test_non_text_message_is_not_usable():
  assert is_usable({"id": 1, "player": "A", "message": 42}) is False


def test_normal_ticket_is_usable():
  assert is_usable({"id": 1, "player": "A", "message": "Le jeu crash."}) is True


def test_same_player_and_message_is_a_duplicate():
  tickets = [
    {"id": 1, "player": "A", "message": "Crash"},
    {"id": 2, "player": "B", "message": "Crash"},
    {"id": 3, "player": "A", "message": "Crash"},
  ]
  unique_tickets, duplicate_of = deduplicate_tickets(tickets)
  assert len(unique_tickets) == 2
  assert duplicate_of == {3: 1}


def test_malformed_entries_are_removed():
  tickets = [{"id": 1, "player": "A", "message": "ok"}, "texte", {"player": "B", "message": "pas d'id"}]
  valid_tickets, ignored_count = remove_malformed_entries(tickets)
  assert len(valid_tickets) == 1
  assert ignored_count == 2
