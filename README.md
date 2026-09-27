# 🛡️ CloudGuard

### Cloud Security Misconfiguration & Compliance Scanner

CloudGuard is a cybersecurity application designed to identify common cloud security misconfigurations, assess security risk, map findings to compliance-oriented frameworks, track remediation, and provide AI-assisted cybersecurity analysis.

The project focuses primarily on AWS security services and provides a safe demonstration environment using sample cloud configuration data.

---

## 🚀 Features

### 🔍 Cloud Security Scanning

CloudGuard analyzes cloud configuration data and identifies security weaknesses across common AWS services.

Supported areas include:

- Amazon S3
- AWS IAM
- Amazon EC2
- Security Groups
- AWS CloudTrail
- Amazon RDS
- AWS KMS

---

### ⚠️ Security Findings

Each finding includes information such as:

- Finding ID
- Title
- Severity
- Cloud service
- Resource
- Description
- Evidence
- Risk score
- Business impact
- Recommendation
- Remediation guidance
- Compliance relevance
- Status

Severity levels include:

- Critical
- High
- Medium
- Low
- Informational

---

## ☁️ Cloud Security Checks

### S3

CloudGuard can identify configuration issues related to:

- Public access
- Encryption
- Versioning
- Logging
- ACLs
- Bucket policies

### IAM

Checks include:

- Root account MFA
- Password policy
- Administrative MFA
- Old access keys
- Unused credentials
- Excessive permissions
- Wildcard permissions

### EC2

Checks include:

- Public exposure
- Public IP addresses
- Security group exposure

### Security Groups

CloudGuard checks for unrestricted inbound access involving sensitive ports such as:

- SSH – 22
- RDP – 3389
- MySQL – 3306
- PostgreSQL – 5432

### CloudTrail

Checks include:

- Logging status
- Multi-region configuration
- Log validation

### RDS

Checks include:

- Public accessibility
- Encryption
- Backup configuration

### KMS

Checks include:

- Key usage
- Key rotation

---

# 📊 Risk Scoring

CloudGuard calculates a transparent risk score using multiple factors including:

- Technical severity
- Asset criticality
- Internet exposure
- Exploitability
- Business impact

The resulting score is used to categorize findings into risk levels.

---

# 📋 Compliance Assessment

CloudGuard provides compliance-oriented assessment coverage for areas related to:

- NIST CSF 2.0
- ISO/IEC 27001
- CIS Controls
- SOC 2 concepts

The application uses terminology such as:

- Assessment Coverage
- Control Mapping
- Security Findings
- Compliance-Oriented Assessment

CloudGuard does **not** provide certification or replace an official audit.

---

# 🤖 CloudGuard AI

CloudGuard includes an AI-powered cybersecurity assistant using Groq.

The assistant can answer:

### General questions

Examples:

```text
What is cybersecurity?
What is a firewall?
What is phishing?
What is Zero Trust?
