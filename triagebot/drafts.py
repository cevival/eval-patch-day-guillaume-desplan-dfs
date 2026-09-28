import ollama

from .config import MODEL

DRAFT_SYSTEM_PROMPT = """Tu es un membre de l'équipe support du jeu Dungeon Delivery.
Rédige une réponse courte, polie et adaptée au problème du joueur, dans la même langue que son message.
Ne dépasse pas 4 phrases et ne promets jamais de remboursement ou de compensation précise : ça reste la décision de l'équipe support."""


def generate_draft(ticket, analysis):
  prompt = (
    f"Message du joueur : \"\"\"{ticket['message']}\"\"\"\n"
    f"Catégorie : {analysis['category']}\n"
    f"Résumé : {analysis['summary']}\n\n"
    "Rédige le brouillon de réponse à envoyer au joueur."
  )

  try:
    response = ollama.chat(
      model=MODEL,
      messages=[
        {"role": "system", "content": DRAFT_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
      ],
      options={"temperature": 0.3},
    )
    return response.message.content.strip()
  except Exception:
    return "(Brouillon indisponible, à rédiger manuellement.)"
