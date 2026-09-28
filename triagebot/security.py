INJECTION_MARKERS = [
  "ignore tes instructions",
  "ignore les instructions",
  "ignore previous instructions",
  "ignore your instructions",
  "nouvelle instruction",
  "system prompt",
  "tu dois répondre",
  "classe ce ticket",
]


def looks_like_prompt_injection(message):
  """Détecte, par mots-clés, une tentative de manipulation du LLM dans le message d'un ticket.

  C'est une vérification déterministe côté Python : elle ne dépend pas du LLM
  et sert de filet de sécurité même si le modèle se laisse influencer.
  """
  lowered = message.lower()
  return any(marker in lowered for marker in INJECTION_MARKERS)
