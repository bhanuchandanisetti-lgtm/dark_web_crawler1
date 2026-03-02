"""
Threat detection logic:
- Domain-aware email & credential leak detection
- Domain mention detection
- Ransomware mention detection
- Structured findings for dashboard & reporting
"""

import re
from datetime import datetime


LEAK_KEYWORDS = [
    "leak", "dump", "database", "breach",
    "hacked", "compromised", "exposed"
]

SELLING_KEYWORDS = [
    "sell", "selling", "price", "btc", "bitcoin",
    "download", "buy", "market"
]

CREDENTIAL_KEYWORDS = [
    "password", "pwd", "login", "credential"
]

RANSOMWARE_KEYWORDS = [
    "ransomware", "leak site", "victim",
    "data published", "we hacked", "stolen data"
]


def extract_domain(org):
    """Normalize organization input to base domain."""
    org = org.lower()
    org = org.replace("http://", "").replace("https://", "")
    org = org.replace("www.", "")
    return org.split("/")[0]


def find_domain_emails(text, organization):
    """Find emails belonging to the monitored domain."""
    domain = extract_domain(organization)
    pattern = rf"[a-zA-Z0-9._%+-]+@{re.escape(domain)}"
    return list(set(re.findall(pattern, text, re.IGNORECASE)))


def find_credentials(text, organization):
    """Find leaked credentials like email:password."""
    domain = extract_domain(organization)
    pattern = rf"[a-zA-Z0-9._%+-]+@{re.escape(domain)}:\S+"
    return list(set(re.findall(pattern, text, re.IGNORECASE)))


def find_domain_mentions(text, organization):
    """Find sentences mentioning the organization/domain."""
    domain = extract_domain(organization)
    sentences = re.split(r"[.!?\n]", text)
    return [s.strip() for s in sentences if domain in s.lower()]


def find_ransomware_mentions(sentences):
    """Detect ransomware-related sentences."""
    results = []
    for s in sentences:
        if any(k in s.lower() for k in RANSOMWARE_KEYWORDS):
            results.append(s.strip())
    return results


def analyze_page(text, source_url, organization):

    #for testing purpose
    if organization == "test.com":
       return [{
        "type": "DOMAIN_MENTION",
        "value": "Simulated ransomware attack on test.com",
        "source": source_url,
        "severity": "HIGH",
        "timestamp": datetime.utcnow().isoformat()
    }]


    """
    Analyze a single page and return structured findings.
    """
    findings = []
    timestamp = datetime.utcnow().isoformat()

    emails = find_domain_emails(text, organization)
    credentials = find_credentials(text, organization)
    mentions = find_domain_mentions(text, organization)
    ransomware = find_ransomware_mentions(mentions)

    for email in emails:
        findings.append({
            "type": "LEAKED_EMAIL",
            "value": email,
            "source": source_url,
            "severity": "MEDIUM",
            "timestamp": timestamp
        })

    for cred in credentials:
        findings.append({
            "type": "LEAKED_CREDENTIAL",
            "value": cred,
            "source": source_url,
            "severity": "CRITICAL",
            "timestamp": timestamp
        })

    for m in ransomware:
        findings.append({
            "type": "RANSOMWARE_MENTION",
            "value": m,
            "source": source_url,
            "severity": "CRITICAL",
            "timestamp": timestamp
        })

    for m in mentions:
        if m not in ransomware:
            findings.append({
                "type": "DOMAIN_MENTION",
                "value": m,
                "source": source_url,
                "severity": "LOW",
                "timestamp": timestamp
            })

    return findings

