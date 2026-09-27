SEVERITY_SCORES = {
    "Critical": 10,
    "High": 7,
    "Medium": 4,
    "Low": 2,
    "Informational": 1,
}


def calculate_risk_score(
    severity: str,
    asset_criticality: str = "Medium",
    internet_exposed: bool = False,
    exploitability: str = "Medium",
    business_impact: str = "Medium",
) -> int:

    severity_score = SEVERITY_SCORES.get(
        severity,
        SEVERITY_SCORES["Medium"]
    )

    criticality_scores = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4,
    }

    exploitability_scores = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
    }

    impact_scores = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4,
    }

    criticality_score = criticality_scores.get(
        asset_criticality,
        2
    )

    exploitability_score = exploitability_scores.get(
        exploitability,
        2
    )

    impact_score = impact_scores.get(
        business_impact,
        2
    )

    exposure_score = 3 if internet_exposed else 1

    raw_score = (
        severity_score
        + criticality_score
        + exploitability_score
        + impact_score
        + exposure_score
    )

    # Normalize to a 0–100 range.
    max_score = 10 + 4 + 3 + 4 + 3

    risk_score = round(
        (raw_score / max_score) * 100
    )

    return risk_score


def get_risk_level(score: int) -> str:

    if score >= 80:
        return "Critical"

    if score >= 60:
        return "High"

    if score >= 35:
        return "Medium"

    return "Low"


def calculate_risk(
    severity: str,
    asset_criticality: str = "Medium",
    internet_exposed: bool = False,
    exploitability: str = "Medium",
    business_impact: str = "Medium",
) -> dict:

    score = calculate_risk_score(
        severity=severity,
        asset_criticality=asset_criticality,
        internet_exposed=internet_exposed,
        exploitability=exploitability,
        business_impact=business_impact,
    )

    return {
        "score": score,
        "level": get_risk_level(score),
    }