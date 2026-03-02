"""
Reporting for Dark Web Monitoring & Threat Intelligence System.
Exports TXT and CSV reports aligned with the final database schema.
"""

import csv
from datetime import datetime
from storage import get_findings

REPORT_TITLE = "Dark Web Monitoring & Threat Intelligence — Findings Report"


def format_findings_text(findings=None):
    """Format findings as a plain-text report."""
    if findings is None:
        findings = get_findings()

    lines = [
        "",
        "=" * 72,
        REPORT_TITLE,
        "=" * 72,
        "Generated: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "Purpose: SDP demo, report submission, and viva.",
        "=" * 72,
        "",
    ]

    if not findings:
        lines.append("No findings detected.")
        return "\n".join(lines)

    for row in findings:
        r = dict(row)

        lines.append(f"Source URL   : {r.get('source_url', '')}")
        lines.append(f"Finding Type : {r.get('finding_type', '')}")
        lines.append(f"Value        : {r.get('value', '')}")
        lines.append(
            f"Severity     : {r.get('severity', '')} | "
            f"Threat Score : {r.get('threat_score', '')} | "
            f"Risk Level   : {r.get('risk_level', '')}"
        )
        lines.append(f"Detected At  : {r.get('detected_at', '')}")
        lines.append("-" * 50)

    return "\n".join(lines)


def export_report(filepath="threat_intel_report.txt"):
    """Export findings as a text report."""
    text = format_findings_text()
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    return filepath


CSV_COLUMNS = [
    "id",
    "source_url",
    "finding_type",
    "value",
    "severity",
    "threat_score",
    "risk_level",
    "detected_at",
]


def export_report_csv(filepath="threat_intel_report.csv"):
    """Export findings as CSV."""
    findings = get_findings()
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in findings:
            writer.writerow(dict(row))
    return filepath

