from typing import List


COMPLIANCE_MAPPINGS = {
    "S3": {
        "NIST CSF": [
            "Protect data and access"
        ],
        "ISO 27001": [
            "Information protection and access control"
        ],
        "CIS Cloud": [
            "Cloud storage security"
        ]
    },

    "IAM": {
        "NIST CSF": [
            "Identity management and access control"
        ],
        "ISO 27001": [
            "Identity and access management"
        ],
        "CIS Cloud": [
            "Identity and permissions management"
        ]
    },

    "EC2": {
        "NIST CSF": [
            "Infrastructure protection"
        ],
        "ISO 27001": [
            "Network and infrastructure security"
        ],
        "CIS Cloud": [
            "Compute security"
        ]
    },

    "Security Group": {
        "NIST CSF": [
            "Network security"
        ],
        "ISO 27001": [
            "Network security controls"
        ],
        "CIS Cloud": [
            "Network access control"
        ]
    },

    "CloudTrail": {
        "NIST CSF": [
            "Security monitoring"
        ],
        "ISO 27001": [
            "Logging and monitoring"
        ],
        "CIS Cloud": [
            "Cloud audit logging"
        ]
    },

    "RDS": {
        "NIST CSF": [
            "Data security"
        ],
        "ISO 27001": [
            "Data protection"
        ],
        "CIS Cloud": [
            "Database security"
        ]
    },

    "KMS": {
        "NIST CSF": [
            "Data security"
        ],
        "ISO 27001": [
            "Cryptographic controls"
        ],
        "CIS Cloud": [
            "Key management"
        ]
    }
}


def get_compliance_mapping(service: str) -> dict:
    return COMPLIANCE_MAPPINGS.get(
        service,
        {
            "NIST CSF": [],
            "ISO 27001": [],
            "CIS Cloud": []
        }
    )


def flatten_compliance_mapping(service: str) -> List[str]:
    mapping = get_compliance_mapping(service)

    result = []

    for framework, controls in mapping.items():
        for control in controls:
            result.append(
                f"{framework}: {control}"
            )

    return result