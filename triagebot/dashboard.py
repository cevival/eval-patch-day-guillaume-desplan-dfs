def print_dashboard(results):
  analyzed = [result for result in results if result["analysis"] is not None]

  print("\n=== Tableau de bord TriageBot ===\n")

  print("Tickets par catégorie :")
  counts_by_category = {}
  for result in analyzed:
    category = result["analysis"]["category"]
    counts_by_category[category] = counts_by_category.get(category, 0) + 1
  for category in sorted(counts_by_category):
    print(f"  - {category} : {counts_by_category[category]}")

  if analyzed:
    average_severity = sum(result["analysis"]["severity"] for result in analyzed) / len(analyzed)
    print(f"\nUrgence moyenne : {average_severity:.1f} / 5")

  print("\nTop 3 des tickets les plus urgents :")
  most_urgent = sorted(analyzed, key=lambda result: result["analysis"]["severity"], reverse=True)[:3]
  for result in most_urgent:
    ticket = result["ticket"]
    analysis = result["analysis"]
    print(f"  - #{ticket['id']} ({ticket['player']}) sévérité {analysis['severity']} : {analysis['summary']}")

  unresolved_count = len(results) - len(analyzed)
  if unresolved_count:
    print(f"\n{unresolved_count} ticket(s) sans analyse exploitable (vide ou à vérifier).")
