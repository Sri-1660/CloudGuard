from models.finding import Finding


def check_kms_security(key: dict) -> list[Finding]:
    findings = []

    key_id = key.get("id", "UNKNOWN")
    key_name = key.get("name", key_id)

    # -------------------------
    # Key usage
    # -------------------------
    if key.get("used_for_encryption") is False:
        findings.append(
            Finding(
                id=f"KMS-NOT-USED-{key_id}",
                title="KMS key is not used for encryption",
                severity="Low",
                service="KMS",
                resource=key_name,
                description=(
                    "The supplied configuration indicates that the "
                    "KMS key is not currently used for encryption."
                ),
                evidence="used_for_encryption = false",
                risk=(
                    "An unused encryption key may indicate incomplete "
                    "encryption coverage or unnecessary key material."
                ),
                business_impact=(
                    "Security controls relying on encryption may not "
                    "provide the intended protection."
                ),
                recommendation=(
                    "Review the purpose and usage of the KMS key."
                ),
                remediation=(
                    "Use the key for the intended encryption workload "
                    "or retire it according to the organization's process."
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
    # Key rotation
    # -------------------------
    if key.get("key_rotation_enabled") is False:
        findings.append(
            Finding(
                id=f"KMS-NO-ROTATION-{key_id}",
                title="KMS key rotation is disabled",
                severity="Medium",
                service="KMS",
                resource=key_name,
                description=(
                    "Automatic key rotation is disabled for the "
                    "supplied KMS key configuration."
                ),
                evidence="key_rotation_enabled = false",
                risk=(
                    "Long-lived cryptographic keys can increase the "
                    "impact of key compromise or prolonged key exposure."
                ),
                business_impact=(
                    "Weak key-management practices can reduce the "
                    "overall strength of data protection controls."
                ),
                recommendation=(
                    "Review the key-management policy and enable "
                    "automatic rotation where appropriate."
                ),
                remediation=(
                    "Enable automatic KMS key rotation according to "
                    "the organization's cryptographic key-management policy."
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