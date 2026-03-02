"""
Persistence layer for threat intelligence findings.
SQLite backend used by detection, scoring, GUI, and reporting.
"""

import sqlite3
from config import DB_NAME


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_url TEXT,
            finding_type TEXT,
            value TEXT,
            severity TEXT,
            threat_score INTEGER,
            risk_level TEXT,
            detected_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_finding(source_url, finding_type, value,
                 severity, threat_score, risk_level, detected_at):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO findings
        (source_url, finding_type, value, severity,
         threat_score, risk_level, detected_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        source_url,
        finding_type,
        value,
        severity,
        threat_score,
        risk_level,
        detected_at
    ))

    conn.commit()
    conn.close()


def get_findings(order_by="detected_at DESC"):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(f"""
        SELECT *
        FROM findings
        ORDER BY {order_by}
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def get_summary_by_type():
    """Used for dashboard counters."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT finding_type, COUNT(*)
        FROM findings
        GROUP BY finding_type
    """)

    data = cur.fetchall()
    conn.close()
    return data


def get_risk_overview():
    """Used for dashboard risk charts."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT risk_level, COUNT(*)
        FROM findings
        GROUP BY risk_level
    """)

    data = cur.fetchall()
    conn.close()
    return data

