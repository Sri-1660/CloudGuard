from models.finding import Finding


DANGEROUS_PORTS = {
    22: "SSH",
    3389: "RDP",
    3306: "MySQL",
    5432: "PostgreSQL",
}


def check_security_group(group: dict) -> list[Finding]:
    findings = []

    group_id = group.get("id", "UNKNOWN")
    group_name = group.get("name", group_id)

    for index, rule in enumerate(group.get("rules", []), start=1):
        port = rule.get("port")
        source = rule.get("source")
        protocol = rule.get("protocol", "unknown")

        if source != "0.0.0.0/0":
            continue

        if port in DANGEROUS_PORTS:
            service_name = DANGEROUS_PORTS[port]

            severity = "Critical" if port in (22, 3389) else "High"

            findings.append(
                Finding(
                    id=f"SG-OPEN-{group_id}-{index}",
                    title=f"{service_name} port exposed to the internet",
                    severity=severity,
                    service="Security Group",
                    resource=group_name,
                    description=(
                        f"The security group allows {service_name} "
                        f"traffic from any IPv4 address."
                    ),
                    evidence=(
                        f"protocol={protocol}, "
                        f"port={port}, "
                        f"source={source}"
                    ),
                    risk=(
                        f"Internet-wide access to {service_name} can "
                        "increase the attack surface of cloud resources."
                    ),
                    business_impact=(
                        "An exposed service may be targeted by "
                        "unauthorized users or automated attacks."
                    ),
                    recommendation=(
                        f"Restrict {service_name} access to trusted "
                        "networks or specific source addresses."
                    ),
                    remediation=(
                        "Replace the unrestricted source range with "
                        "a narrowly scoped network or approved IP range."
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