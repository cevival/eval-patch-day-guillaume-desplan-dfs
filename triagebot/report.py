def _format_ticket_line(result):
  ticket = result["ticket"]
  analysis = result["analysis"]
  if analysis is None:
    return f"- **#{ticket['id']}** ({ticket['player']}) — analyse indisponible"
  return (
    f"- **#{ticket['id']}** ({ticket['player']}) — {analysis['category']}, "
    f"sévérité {analysis['severity']}/5 : {analysis['summary']}"
  )


def write_report(results, path):
  analyzed = [result for result in results if result["analysis"] is not None]
  escalated = [result for result in results if result["escalation"] in ("moderation", "responsable_support")]
  to_check = [result for result in results if result["escalation"] == "relecture_humaine"]

  lines = ["# Rapport de triage - Dungeon Delivery", ""]
  lines.append(f"- Tickets traités : {len(results)}")
  lines.append(f"- Tickets analysés par le LLM : {len(analyzed)}")
  if analyzed:
    average_severity = sum(result["analysis"]["severity"] for result in analyzed) / len(analyzed)
    lines.append(f"- Urgence moyenne : {average_severity:.1f}/5")
  lines.append(f"- Tickets à escalader : {len(escalated)}")
  lines.append(f"- Tickets à vérifier manuellement : {len(to_check)}")
  lines.append("")

  lines.append("## Tickets à escalader")
  lines.append("")
  if escalated:
    for result in escalated:
      lines.append(_format_ticket_line(result) + f" → {result['escalation']}")
  else:
    lines.append("Aucun ticket à escalader.")
  lines.append("")

  lines.append("## Tickets à vérifier manuellement")
  lines.append("")
  if to_check:
    for result in to_check:
      lines.append(_format_ticket_line(result))
  else:
    lines.append("Aucun ticket à vérifier manuellement.")
  lines.append("")

  with open(path, "w", encoding="utf-8") as file:
    file.write("\n".join(lines))
