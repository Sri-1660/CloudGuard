from models.finding import Finding


def check_s3_public_access(bucket: dict) -> list[Finding]:
    findings = []

    if bucket.get("block_public_access") is False:
        findings.append(
            Finding(
                id=f"S3-PUBLIC-{bucket.get('name', 'UNKNOWN')}",
                title="S3 bucket allows public access",
                severity="High",
                service="S3",
                resource=bucket.get("name", "Unknown"),
                description=(
                    "The S3 bucket has public access protection disabled."
                ),
                evidence=(
                    "Block Public Access = Disabled"
                ),
                risk=(
                    "Unauthorized users may be able to access objects "
                    "stored in the bucket."
                ),
                business_impact=(
                    "Sensitive business or customer data could be exposed."
                ),
                recommendation=(
                    "Enable S3 Block Public Access and review the "
                    "bucket policy and ACL configuration."
                ),
                remediation=(
                    "Enable all S3 Block Public Access settings and "
                    "verify that no public bucket policy or ACL remains."
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