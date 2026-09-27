from models.finding import Finding


def check_rds_security(database: dict) -> list[Finding]:
    findings = []

    database_id = database.get("id", "UNKNOWN")
    database_name = database.get("name", database_id)

    # -------------------------
    # Public accessibility
    # -------------------------
    if database.get("publicly_accessible") is True:
        findings.append(
            Finding(
                id=f"RDS-PUBLIC-{database_id}",
                title="RDS database is publicly accessible",
                severity="Critical",
                service="RDS",
                resource=database_name,
                description=(
                    "The RDS database is configured to allow "
                    "public accessibility."
                ),
                evidence="publicly_accessible = true",
                risk=(
                    "A publicly accessible database has increased "
                    "exposure to unauthorized network access."
                ),
                business_impact=(
                    "Unauthorized access to a production database "
                    "could expose sensitive business or customer data."
                ),
                recommendation=(
                    "Review whether public accessibility is required "
                    "and restrict network access where possible."
                ),
                remediation=(
                    "Disable public accessibility and use private "
                    "network connectivity with restricted security groups."
                ),
                compliance=[
                    "NIST CSF",
                    "ISO 27001",
                    "CIS Cloud"
                ],
                status="Open",
            )
        )

    # -------------------------
    # Encryption
    # -------------------------
    if database.get("encryption_enabled") is False:
        findings.append(
            Finding(
                id=f"RDS-NO-ENCRYPTION-{database_id}",
                title="RDS database encryption is disabled",
                severity="High",
                service="RDS",
                resource=database_name,
                description=(
                    "The RDS database is not configured for encryption "
                    "at rest."
                ),
                evidence="encryption_enabled = false",
                risk=(
                    "Data stored in the database may not receive the "
                    "protection provided by encryption at rest."
                ),
                business_impact=(
                    "Sensitive customer or business data could have "
                    "reduced protection if storage is accessed improperly."
                ),
                recommendation=(
                    "Enable encryption at rest for the database."
                ),
                remediation=(
                    "Configure the database with encryption using an "
                    "appropriate AWS KMS key."
                ),
                compliance=[
                    "NIST CSF",
                    "ISO 27001",
                    "CIS Cloud"
                ],
                status="Open",
            )
        )

    # -------------------------
    # Automated backups
    # -------------------------
    if database.get("automated_backups") is False:
        findings.append(
            Finding(
                id=f"RDS-NO-BACKUPS-{database_id}",
                title="RDS automated backups are disabled",
                severity="High",
                service="RDS",
                resource=database_name,
                description=(
                    "Automated backups are disabled for the RDS database."
                ),
                evidence="automated_backups = false",
                risk=(
                    "A lack of automated backups can reduce the ability "
                    "to recover data after an incident or failure."
                ),
                business_impact=(
                    "Data loss or prolonged service disruption could "
                    "affect business operations."
                ),
                recommendation=(
                    "Enable automated backups and define an appropriate "
                    "retention period."
                ),
                remediation=(
                    "Enable RDS automated backups and verify the "
                    "configured retention period."
                ),
                compliance=[
                    "NIST CSF",
                    "ISO 27001",
                    "CIS Cloud"
                ],
                status="Open",
            )
        )

    return findings