def get_analyzed_results(results):
  """Garde les tickets analysés avec succès (statut "ok") et non dupliqués.

  Un ticket "to_check" (réponse invalide ou tentative de manipulation) ne doit
  pas compter dans les statistiques ni apparaître dans le top des urgences.
  """
  analyzed = []
  for result in results:
    if result["status"] == "ok" and result["duplicate_of"] is None:
      analyzed.append(result)
  return analyzed


def count_by_category(analyzed):
  counts = {}
  for result in analyzed:
    category = result["analysis"]["category"]
    counts[category] = counts.get(category, 0) + 1
  return counts


def average_severity(analyzed):
  if not analyzed:
    return 0
  total = 0
  for result in analyzed:
    total += result["analysis"]["severity"]
  return total / len(analyzed)
