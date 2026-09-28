from .stats import get_analyzed_results, count_by_category, average_severity

ESCALATION_LABELS = {
  "moderation": "Équipe modération",
  "responsable_support": "Responsable support",
  "relecture_humaine": "Relecture humaine",
  "standard": "Traitement standard",
}


def format_ticket_line(result):
  ticket = result["ticket"]
  analysis = result["analysis"]
  if analysis is None:
    return f"- **#{ticket['id']}** ({ticket['player']}) : analyse impossible, le LLM n'a pas donné de réponse valide"
  return (
    f"- **#{ticket['id']}** ({ticket['player']}) : {analysis['summary']} "
    f"(catégorie {analysis['category']}, urgence {analysis['severity']}/5)"
  )


def write_report(results, path):
  unique_results = [result for result in results if result["duplicate_of"] is None]
  analyzed = get_analyzed_results(results)
  escalated = [result for result in unique_results if result["escalation"] in ("moderation", "responsable_support")]
  to_check = [result for result in unique_results if result["escalation"] == "relecture_humaine"]

  lines = ["# Rapport de triage - Dungeon Delivery", ""]

  lines.append("## Synthèse")
  lines.append("")
  lines.append(f"- Tickets reçus : {len(results)} (dont {len(results) - len(unique_results)} doublon(s))")
  lines.append(f"- Tickets analysés avec succès : {len(analyzed)}")
  lines.append(f"- Urgence moyenne : {average_severity(analyzed):.1f}/5")
  lines.append(f"- Tickets à escalader : {len(escalated)}")
  lines.append(f"- Tickets à vérifier par un humain : {len(to_check)}")
  lines.append("")

  lines.append("Répartition par catégorie :")
  lines.append("")
  counts = count_by_category(analyzed)
  for category in sorted(counts):
    lines.append(f"- {category} : {counts[category]}")
  lines.append("")

  lines.append("## Tickets à escalader")
  lines.append("")
  if escalated:
    for result in escalated:
      lines.append(format_ticket_line(result) + f" → **{ESCALATION_LABELS[result['escalation']]}**")
  else:
    lines.append("Aucun ticket à escalader.")
  lines.append("")

  lines.append("## Tickets à vérifier par un humain")
  lines.append("")
  if to_check:
    for result in to_check:
      lines.append(format_ticket_line(result))
  else:
    lines.append("Aucun ticket à vérifier.")
  lines.append("")

  with open(path, "w", encoding="utf-8") as file:
    file.write("\n".join(lines))
