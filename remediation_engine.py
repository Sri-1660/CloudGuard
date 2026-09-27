from datetime import date, timedelta


def get_priority(severity: str) -> str:
    """
    Convert finding severity into remediation priority.
    """

    priority_map = {
        "Critical": "Critical",
        "High": "High",
        "Medium": "Medium",
        "Low": "Low",
        "Informational": "Low",
    }

    return priority_map.get(
        severity,
        "Medium"
    )


def get_due_days(severity: str) -> int:
    """
    Define the default remediation target window
    based on finding severity.
    """

    due_days = {
        "Critical": 7,
        "High": 14,
        "Medium": 30,
        "Low": 60,
        "Informational": 90,
    }

    return due_days.get(
        severity,
        30
    )


def calculate_due_date(severity: str) -> str:
    """
    Calculate a default remediation due date.
    """

    days = get_due_days(severity)

    due_date = date.today() + timedelta(
        days=days
    )

    return due_date.isoformat()


def create_remediation_item(finding) -> dict:
    """
    Convert a security finding into a remediation item.
    """

    priority = get_priority(
        finding.severity
    )

    return {
        "finding_id": finding.id,
        "finding": finding.title,
        "service": finding.service,
        "resource": finding.resource,
        "severity": finding.severity,
        "risk_score": finding.risk_score,
        "risk_level": finding.risk_level,
        "recommendation": finding.recommendation,
        "remediation": finding.remediation,
        "owner": "Cloud Security Team",
        "priority": priority,
        "due_date": calculate_due_date(
            finding.severity
        ),
        "status": "Open",
        "completion_date": None,
        "notes": "",
    }


def create_remediation_plan(
    findings: list
) -> list:

    remediation_items = []

    for finding in findings:
        remediation_items.append(
            create_remediation_item(
                finding
            )
        )

    return remediation_items