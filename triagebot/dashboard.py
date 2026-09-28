from .stats import get_analyzed_results, count_by_category, average_severity


def count_by_status(results, status):
  total = 0
  for result in results:
    if result["status"] == status and result["duplicate_of"] is None:
      total += 1
  return total


def print_dashboard(results):
  analyzed = get_analyzed_results(results)

  print("\n=== Tableau de bord TriageBot ===\n")

  print("Tickets par catégorie :")
  counts = count_by_category(analyzed)
  for category in sorted(counts):
    print(f"  - {category} : {counts[category]}")

  print(f"\nUrgence moyenne : {average_severity(analyzed):.1f} / 5")

  print("\nTop 3 des tickets les plus urgents :")
  most_urgent = sorted(analyzed, key=lambda result: result["analysis"]["severity"], reverse=True)[:3]
  for result in most_urgent:
    ticket = result["ticket"]
    analysis = result["analysis"]
    print(f"  - #{ticket['id']} ({ticket['player']}) sévérité {analysis['severity']} : {analysis['summary']}")

  duplicate_count = len([result for result in results if result["duplicate_of"] is not None])
  print("\nTickets mis de côté :")
  print(f"  - à vérifier par un humain : {count_by_status(results, 'to_check')}")
  print(f"  - vides ou incomplets : {count_by_status(results, 'skipped_empty')}")
  print(f"  - doublons : {duplicate_count}")
