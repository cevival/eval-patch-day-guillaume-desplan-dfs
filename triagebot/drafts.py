import ollama

from .config import MODEL

DRAFT_SYSTEM_PROMPT = """Tu es un membre de l'équipe support du jeu Dungeon Delivery et tu réponds AU joueur qui a écrit le ticket.
Rédige une réponse courte, polie et adaptée à son problème.
Si le joueur est insultant, reste courtois et rappelle calmement que les échanges doivent rester respectueux.
Commence par saluer le joueur. Ne dépasse pas 4 phrases et ne promets jamais de remboursement
ou de compensation précise (c'est la décision de l'équipe support)."""

EMPTY_TICKET_DRAFT = (
  "Bonjour, nous avons bien reçu votre ticket mais il semble vide. "
  "Pourriez-vous nous décrire votre problème afin que nous puissions vous aider ? "
  "L'équipe support Dungeon Delivery"
)


def ask_llm(messages, temperature):
  response = ollama.chat(model=MODEL, messages=messages, options={"temperature": temperature})
  return response.message.content.strip()


def detect_language(message):
  """Demande au LLM la langue du message (ex. "français", "allemand")."""
  question = (
    "Dans quelle langue est écrit ce texte ? Réponds uniquement par le nom de la langue, "
    f"en français (exemple : français, anglais, allemand).\n\nTexte : \"\"\"{message}\"\"\""
  )
  answer = ask_llm([{"role": "user", "content": question}], temperature=0)
  return answer.strip(" .").lower()


def generate_draft(ticket, analysis):
  try:
    language = detect_language(ticket["message"])

    prompt = f"Message du joueur : \"\"\"{ticket['message']}\"\"\"\n"
    if analysis is not None:
      prompt += f"Catégorie du ticket : {analysis['category']}\n"
    prompt += f"\nRédige le brouillon de réponse à envoyer au joueur. La réponse doit être écrite en {language}."

    return ask_llm(
      [
        {"role": "system", "content": DRAFT_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
      ],
      temperature=0.3,
    )
  except Exception:
    return "(Brouillon indisponible, à rédiger manuellement.)"
