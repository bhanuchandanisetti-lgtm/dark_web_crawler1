"""
Threat Intelligence Scoring Engine.
Computes threat_score (0–100) and risk_level from finding type and repetition.
Aligned with detection.py finding types.
"""

# Base score by finding type (explainable & viva-safe)
THREAT_TYPE_WEIGHTS = {
    "LEAKED_CREDENTIAL": 70,     # strongest signal
    "RANSOMWARE_MENTION": 80,    # critical threat
    "LEAKED_EMAIL": 40,
    "DOMAIN_MENTION": 15,
}

# Bonus per repeated finding on same URL (1st=0, 2nd=+8, 3rd=+16, cap +20)
REPETITION_BONUS_CAP = 20
REPETITION_BONUS_PER_RANK = 8


def _repetition_bonus(repetition_rank):
    """Bonus for repeated findings on the same URL (1-based)."""
    if repetition_rank <= 1:
        return 0
    return min(REPETITION_BONUS_CAP, (repetition_rank - 1) * REPETITION_BONUS_PER_RANK)


def score_to_risk(score):
    """Map threat_score (0–100) to risk level."""
    if score <= 25:
        return "LOW"
    if score <= 50:
        return "MEDIUM"
    if score <= 75:
        return "HIGH"
    return "CRITICAL"


def compute_threat_score(finding_type, repetition_rank=1):
    """
    Compute threat_score (0–100) and risk_level.
    Inputs:
      - finding_type: one of detection.py types
      - repetition_rank: 1-based count of same-type findings on same URL
    Returns:
      (threat_score, risk_level)
    """
    base = THREAT_TYPE_WEIGHTS.get(finding_type, 20)
    bonus = _repetition_bonus(repetition_rank)
    score = min(100, max(0, base + bonus))
    return score, score_to_risk(score)

