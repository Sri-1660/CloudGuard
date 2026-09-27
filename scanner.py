import json
from pathlib import Path

from rules.s3_rules import check_s3_public_access
from rules.iam_rules import check_iam_security
from rules.ec2_rules import check_ec2_security
from rules.sg_rules import check_security_group
from rules.cloudtrail_rules import check_cloudtrail_security
from rules.rds_rules import check_rds_security
from rules.kms_rules import check_kms_security

from engine.risk_engine import calculate_risk
from engine.compliance_mapper import flatten_compliance_mapping
from engine.remediation_engine import create_remediation_plan


def load_configuration(config_path: str) -> dict:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def apply_risk_scoring(findings: list) -> list:

    for finding in findings:

        result = calculate_risk(
            severity=finding.severity,
            asset_criticality=finding.asset_criticality,
            internet_exposed=finding.internet_exposed,
            exploitability=finding.exploitability,
            business_impact=finding.business_impact_level,
        )

        finding.risk_score = result["score"]
        finding.risk_level = result["level"]

    return findings


def apply_compliance_mapping(
    findings: list
) -> list:

    for finding in findings:

        finding.compliance = (
            flatten_compliance_mapping(
                finding.service
            )
        )

    return findings


def scan_configuration(
    config: dict
) -> list:

    findings = []

    resources = config.get(
        "resources",
        {}
    )

    # -------------------------
    # S3
    # -------------------------
    for bucket in resources.get(
        "s3",
        []
    ):
        findings.extend(
            check_s3_public_access(
                bucket
            )
        )

    # -------------------------
    # IAM
    # -------------------------
    iam_config = resources.get(
        "iam"
    )

    if iam_config:

        findings.extend(
            check_iam_security(
                iam_config
            )
        )

    # -------------------------
    # EC2
    # -------------------------
    for instance in resources.get(
        "ec2",
        []
    ):
        findings.extend(
            check_ec2_security(
                instance
            )
        )

    # -------------------------
    # Security Groups
    # -------------------------
    for security_group in resources.get(
        "security_groups",
        []
    ):
        findings.extend(
            check_security_group(
                security_group
            )
        )

    # -------------------------
    # CloudTrail
    # -------------------------
    cloudtrail_config = resources.get(
        "cloudtrail"
    )

    if cloudtrail_config:

        findings.extend(
            check_cloudtrail_security(
                cloudtrail_config
            )
        )

    # -------------------------
    # RDS
    # -------------------------
    for database in resources.get(
        "rds",
        []
    ):
        findings.extend(
            check_rds_security(
                database
            )
        )

    # -------------------------
    # KMS
    # -------------------------
    for key in resources.get(
        "kms",
        []
    ):
        findings.extend(
            check_kms_security(
                key
            )
        )

    # -------------------------
    # Risk scoring
    # -------------------------
    findings = apply_risk_scoring(
        findings
    )

    # -------------------------
    # Compliance mapping
    # -------------------------
    findings = apply_compliance_mapping(
        findings
    )

    return findings


def run_scan(
    config_path: str
) -> list:

    config = load_configuration(
        config_path
    )

    return scan_configuration(
        config
    )


def generate_remediation_plan(
    config_path: str
) -> list:

    findings = run_scan(
        config_path
    )

    return create_remediation_plan(
        findings
    )