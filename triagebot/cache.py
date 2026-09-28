import sqlite3

from .config import CACHE_PATH


def init_cache(path=CACHE_PATH):
  connection = sqlite3.connect(path)
  connection.execute("""
    CREATE TABLE IF NOT EXISTS analysis_cache (
      player TEXT NOT NULL,
      message TEXT NOT NULL,
      category TEXT NOT NULL,
      severity INTEGER NOT NULL,
      sentiment TEXT NOT NULL,
      summary TEXT NOT NULL,
      PRIMARY KEY (player, message)
    )
  """)
  connection.commit()
  return connection


def get_cached_analysis(connection, player, message):
  row = connection.execute(
    "SELECT category, severity, sentiment, summary FROM analysis_cache WHERE player = ? AND message = ?",
    (player, message),
  ).fetchone()

  if row is None:
    return None

  category, severity, sentiment, summary = row
  return {"category": category, "severity": severity, "sentiment": sentiment, "summary": summary}


def save_analysis(connection, player, message, analysis):
  connection.execute(
    """
    INSERT OR REPLACE INTO analysis_cache (player, message, category, severity, sentiment, summary)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (player, message, analysis["category"], analysis["severity"], analysis["sentiment"], analysis["summary"]),
  )
  connection.commit()
