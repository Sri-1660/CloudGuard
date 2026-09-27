import os

from pathlib import Path

from typing import List



from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from groq import Groq



from engine.scanner import run_scan





# ============================================================*

# ENVIRONMENT*

# ============================================================*



BASE_DIR = Path(__file__).resolve().parent



load_dotenv(BASE_DIR / ".env")



SAMPLE_CONFIG = BASE_DIR / "data" / "sample_config.json"



GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()



GROQ_MODEL = os.getenv(

    "GROQ_MODEL",

    "llama-3.3-70b-versatile",

).strip()





# ============================================================*

# GROQ CLIENT*

# ============================================================*



groq_client = None



if GROQ_API_KEY:

    groq_client = Groq(

        api_key=GROQ_API_KEY

    )





# ============================================================*

# FASTAPI APP*

# ============================================================*



app = FastAPI(

    title="CloudGuard API",

    description="Cloud Security Misconfiguration & Compliance Scanner",

    version="2.0.0",

)





app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:5173",

        "http://127.0.0.1:5173",

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)





# ============================================================*

# REQUEST MODELS*

# ============================================================*



class ChatMessage(BaseModel):

    role: str

    content: str





class AssistantRequest(BaseModel):

    message: str

    history: List[ChatMessage] = []





# ============================================================*

# ROOT / HEALTH*

# ============================================================*



@app.get("/")

def root():



    return {

        "application": "CloudGuard",

        "status": "running",

        "ai_enabled": bool(GROQ_API_KEY),

        "model": GROQ_MODEL if GROQ_API_KEY else None,

        "message": "CloudGuard API is online",

    }





@app.get("/api/health")

def health():



    return {

        "status": "healthy",

        "backend": True,

        "groq_configured": bool(GROQ_API_KEY),

        "model": GROQ_MODEL if GROQ_API_KEY else None,

    }





# ============================================================*

# SAMPLE SCAN*

# ============================================================*



@app.get("/api/scan/sample")

def scan_sample():



    try:



        findings = run_scan(

            str(SAMPLE_CONFIG)

        )



        return {

            "organization": "CloudPay Technologies",

            "findings": [

                finding.model_dump()

                for finding in findings

            ],

            "total_findings": len(findings),

        }



    except Exception as error:



        raise HTTPException(

            status_code=500,

            detail=f"Scanner error: {error}",

        )





# ============================================================*

# GET FINDINGS*

# ============================================================*



def get_findings():



    try:



        return run_scan(

            str(SAMPLE_CONFIG)

        )



    except Exception as error:



        print(

            f"[CloudGuard Scanner Error] {error}"

        )



        return []





# ============================================================*

# GREETING HANDLER*

# ============================================================*



def greeting_response(message: str):



    text = message.lower().strip()



    greetings = {

        "hi",

        "hello",

        "hey",

        "hey there",

        "hi there",

        "yo",

        "hiya",

    }



    if text in greetings:



        return (

            "Hey! 👋 I'm CloudGuard AI. "

            "I can help with CloudGuard, cybersecurity, "

            "cloud security, SOC, SIEM, GRC, compliance, "

            "IAM, AWS, risk management, or just general "

            "security questions. What would you like to know?"

        )



    if text in {

        "good morning",

        "morning",

    }:



        return (

            "Good morning! 👋 "

            "What can I help you with today?"

        )



    if text in {

        "good afternoon",

        "afternoon",

    }:



        return (

            "Good afternoon! 👋 "

            "What can I help you with?"

        )



    if text in {

        "good evening",

        "evening",

    }:



        return (

            "Good evening! 👋 "

            "What can I help you with?"

        )



    if (

        "what's up" in text

        or "whats up" in text

        or "how are you" in text

    ):



        return (

            "Hey! 😄 I'm doing great and ready to help. "

            "Ask me anything about CloudGuard or cybersecurity."

        )



    if text in {

        "thanks",

        "thank you",

        "thx",

        "thank u",

    }:



        return (

            "You're welcome! 😊 "

            "Let me know what you'd like to explore next."

        )



    if text in {

        "bye",

        "goodbye",

        "see you",

    }:



        return (

            "Bye! 👋 Stay secure. "

            "I'll be here whenever you need me."

        )



    return None





# ============================================================*

# DETERMINE WHETHER PROJECT CONTEXT IS NEEDED*

# ============================================================*



def needs_cloudguard_context(question: str) -> bool:



    text = question.lower()



    project_keywords = [



        # CloudGuard*

        "cloudguard",

        "my scan",

        "my findings",

        "my risks",

        "my resources",

        "my assessment",

        "my cloud",



        # Findings*

        "finding",

        "findings",

        "critical",

        "high risk",

        "risk score",

        "security posture",

        "security issues",



        # Cloud resources*

        "s3",

        "bucket",

        "iam",

        "identity",

        "access key",

        "mfa",

        "ec2",

        "security group",

        "ssh",

        "rdp",

        "rds",

        "database",

        "cloudtrail",

        "cloudwatch",

        "kms",

        "encryption",

        "key rotation",



        # Remediation*

        "remediate",

        "remediation",

        "fix",

        "fixing",

        "what should i fix",

        "what should i remediate",



        # Compliance related to this project*

        "assessment coverage",

        "cloud compliance",

        "cloud security posture",

    ]



    return any(

        keyword in text

        for keyword in project_keywords

    )





# ============================================================

# BUILD CLOUDGUARD CONTEXT

# ============================================================



def build_cloudguard_context(

    question: str

) -> str:



    findings = get_findings()



    if not findings:



        return (

            "CloudGuard sample findings are currently "

            "unavailable."

        )



    text = question.lower()



    selected = findings



    # --------------------------------------------------------

    # IAM questions

    # --------------------------------------------------------



    if any(

        word in text

        for word in [

            "iam",

            "identity",

            "access key",

            "mfa",

            "password policy",

            "privilege",

            "permission",

            "wildcard",

        ]

    ):



        selected = [

            finding

            for finding in findings

            if finding.service.lower() == "iam"

        ]



    # --------------------------------------------------------*

    # S3 questions*

    # --------------------------------------------------------*



    elif any(

        word in text

        for word in [

            "s3",

            "bucket",

            "object storage",

        ]

    ):



        selected = [

            finding

            for finding in findings

            if finding.service.lower() == "s3"

        ]



    # --------------------------------------------------------*

    # EC2 questions*

    # --------------------------------------------------------*



    elif any(

        word in text

        for word in [

            "ec2",

            "server",

            "public ip",

            "internet exposed",

        ]

    ):



        selected = [

            finding

            for finding in findings

            if finding.service.lower() == "ec2"

        ]



    # --------------------------------------------------------*

    # SECURITY GROUP questions*

    # --------------------------------------------------------*



    elif any(

        word in text

        for word in [

            "security group",

            "ssh",

            "rdp",

            "3306",

            "3389",

            "5432",

            "port 22",

        ]

    ):



        selected = [

            finding

            for finding in findings

            if finding.service.lower()

            in {

                "security group",

                "security groups",

                "sg",

            }

        ]



    # --------------------------------------------------------*

    # RDS questions*

    # --------------------------------------------------------*



    elif any(

        word in text

        for word in [

            "rds",

            "database",

            "mysql",

            "postgres",

        ]

    ):



        selected = [

            finding

            for finding in findings

            if finding.service.lower() == "rds"

        ]



    # --------------------------------------------------------*

    # CLOUDTRAIL questions*

    # --------------------------------------------------------*



    elif any(

        word in text

        for word in [

            "cloudtrail",

            "logging",

            "audit logging",

            "multi region",

        ]

    ):



        selected = [

            finding

            for finding in findings

            if finding.service.lower()

            == "cloudtrail"

        ]



    # --------------------------------------------------------*

    # KMS questions*

    # --------------------------------------------------------*



    elif any(

        word in text

        for word in [

            "kms",

            "key rotation",

            "encryption key",

        ]

    ):



        selected = [

            finding

            for finding in findings

            if finding.service.lower() == "kms"

        ]



    # --------------------------------------------------------*

    # Critical findings*

    # --------------------------------------------------------*



    elif "critical" in text:



        selected = [

            finding

            for finding in findings

            if finding.severity == "Critical"

        ]



    # --------------------------------------------------------*

    # High findings*

    # --------------------------------------------------------*



    elif (

        "high" in text

        or "highest risk" in text

    ):



        selected = [

            finding

            for finding in findings

            if finding.severity == "High"

        ]



    # --------------------------------------------------------*

    # Build context*

    # --------------------------------------------------------*



    lines = [



        "CLOUDGUARD DEMO ENVIRONMENT",



        "Organization: CloudPay Technologies",



        "Important: This is fictional sample data, "

        "not a live AWS environment.",



        "",



        f"Total findings: {len(findings)}",



        f"Critical findings: "

        f"{len([x for x in findings if x.severity == 'Critical'])}",



        f"High findings: "

        f"{len([x for x in findings if x.severity == 'High'])}",



        f"Medium findings: "

        f"{len([x for x in findings if x.severity == 'Medium'])}",



        f"Low findings: "

        f"{len([x for x in findings if x.severity == 'Low'])}",



        "",



        "RELEVANT FINDINGS:",

    ]



    for finding in selected:



        lines.extend(

            [

                "",

                f"ID: {finding.id}",

                f"Title: {finding.title}",

                f"Severity: {finding.severity}",

                f"Service: {finding.service}",

                f"Resource: {finding.resource}",

                f"Risk Score: {finding.risk_score}",

                f"Risk Level: {finding.risk_level}",

                f"Description: {finding.description}",

                f"Evidence: {finding.evidence}",

                f"Business Impact: {finding.business_impact}",

                f"Recommendation: {finding.recommendation}",

                f"Remediation: {finding.remediation}",

                f"Compliance: "

                f"{', '.join(finding.compliance)}",

                f"Status: {finding.status}",

            ]

        )



    return "\n".join(lines)





# ============================================================*

# CLOUDGUARD AI SYSTEM PROMPT*

# ============================================================*



SYSTEM_PROMPT = """

You are CloudGuard AI, the intelligent cybersecurity

assistant inside the CloudGuard security application.



You are a knowledgeable, friendly, professional cybersecurity

assistant.



Your job is NOT limited to CloudGuard.



You should answer:



1\. General conversation

2\. General cybersecurity questions

3\. SOC questions

4\. GRC questions

5\. Cloud security questions

6\. AWS security questions

7\. Risk and compliance questions

8\. CloudGuard project questions

9\. Follow-up questions using conversation history



============================================================

GENERAL CONVERSATION

============================================================



Respond naturally to greetings and casual conversation.



Examples:



User: Hi

Assistant: Hey! 👋 I'm CloudGuard AI. What can I help you with?



User: What's up?

Assistant: Hey! I'm doing great and ready to help. 😄



Do not turn a simple greeting into a cybersecurity lecture.



============================================================

GENERAL CYBERSECURITY

============================================================



You can explain cybersecurity concepts such as:



\- Cybersecurity

\- Information security

\- CIA triad

\- Threats

\- Threat actors

\- Vulnerabilities

\- Exploits

\- Risk

\- Attack surface

\- Security controls

\- Defense in depth

\- Zero Trust

\- Authentication

\- Authorization

\- MFA

\- SSO

\- IAM

\- PAM

\- Least privilege

\- Encryption

\- Hashing

\- Digital signatures

\- PKI

\- Certificates

\- Malware

\- Ransomware

\- Trojans

\- Worms

\- Rootkits

\- Spyware

\- Phishing

\- Spear phishing

\- Social engineering

\- Brute force

\- Password security

\- Vulnerability management

\- Patch management

\- Penetration testing

\- Threat hunting

\- Digital forensics

\- Incident response

\- SOC operations

\- SIEM

\- EDR

\- XDR

\- SOAR

\- Log analysis

\- Detection engineering

\- MITRE ATT&CK

\- Security monitoring

\- Network security

\- Firewalls

\- IDS

\- IPS

\- VPN

\- DNS

\- TCP/IP

\- HTTP

\- HTTPS

\- TLS

\- API security

\- Web security

\- OWASP

\- Secure coding

\- DevSecOps

\- Supply-chain security

\- Data security

\- DLP

\- Business continuity

\- Disaster recovery



============================================================

SOC

============================================================



You can explain:



\- SOC analyst responsibilities

\- L1/L2/L3 SOC

\- Alert triage

\- Incident investigation

\- Incident response

\- SIEM

\- EDR

\- XDR

\- SOAR

\- Threat intelligence

\- IOC

\- IOA

\- TTPs

\- MITRE ATT&CK

\- Log analysis

\- Detection rules

\- Correlation rules

\- False positives

\- Escalation

\- Containment

\- Eradication

\- Recovery

\- Lessons learned



============================================================

GRC

============================================================



Explain:



\- Governance

\- Risk

\- Compliance

\- Risk assessment

\- Risk register

\- Risk treatment

\- Risk acceptance

\- Risk mitigation

\- Residual risk

\- Control design

\- Control effectiveness

\- Policies

\- Procedures

\- Standards

\- Guidelines

\- Evidence

\- Audits

\- Internal controls

\- Third-party risk

\- Vendor risk

\- Business impact

\- Risk appetite

\- Risk tolerance



============================================================

FRAMEWORKS

============================================================



You can explain:



\- NIST CSF

\- NIST SP 800-53

\- ISO/IEC 27001

\- CIS Controls

\- SOC 2

\- COBIT

\- PCI DSS

\- GDPR

\- OWASP



Be careful not to claim that CloudGuard itself

provides certification.



Use terms such as:



\- assessment

\- assessment coverage

\- control mapping

\- security findings

\- compliance-oriented assessment



Do not claim that CloudGuard provides:



\- ISO certification

\- SOC 2 certification

\- official audit

\- legal compliance certification



============================================================

CLOUD SECURITY

============================================================



You can explain:



\- AWS

\- Azure

\- GCP

\- S3

\- IAM

\- EC2

\- Security Groups

\- RDS

\- CloudTrail

\- CloudWatch

\- KMS

\- Encryption

\- Key rotation

\- MFA

\- Public exposure

\- Network exposure

\- Access policies

\- Logging

\- Monitoring

\- Cloud misconfiguration

\- Cloud security posture

\- Cloud compliance



============================================================

CLOUDGUARD PROJECT

============================================================



When the user asks about their CloudGuard findings,

use the supplied CloudGuard context.



Examples:



"What are my critical findings?"



"Explain my IAM risks."



"Why is my RDS database risky?"



"How do I fix open SSH?"



"How many findings do I have?"



"Summarize my CloudGuard scan."



"Which cloud services have issues?"



"Why is this finding dangerous?"



"What should I remediate?"



When answering project-specific questions:



1\. Explain what the finding means.

2\. Explain why it matters.

3\. Refer to the supplied evidence.

4\. Explain the risk.

5\. Give practical remediation.

6\. Mention compliance relevance when available.



Never invent CloudGuard findings.



Never invent evidence.



Never pretend the demo data is a real AWS environment.



============================================================

FOLLOW-UP QUESTIONS

============================================================



Use conversation history.



If the user asks:



"Why?"



"How?"



"What about that?"



"Explain that."



"Can you simplify it?"



"Give me an example."



Understand what they are referring to from the previous

conversation.



============================================================

ANSWER STYLE

============================================================



For simple questions:



Be concise.



For beginner questions:



Explain the concept in simple language first.



For technical questions:



Explain the concept, then provide a practical example.



For comparisons:



Use a table when helpful.



For security findings:



Use:



What it means

Why it matters

Evidence

Risk

Remediation



Do not unnecessarily repeat the entire CloudGuard scan.



============================================================

ACCURACY

============================================================



Do not fabricate facts.



If something depends on the user's environment,

say so.



If CloudGuard sample data is being discussed,

clearly distinguish it from a real cloud environment.



============================================================

CYBERSECURITY SAFETY

============================================================



Provide defensive, educational, and authorized security

guidance.



For potentially dangerous offensive requests, focus on:



\- authorized testing

\- labs

\- defensive analysis

\- detection

\- mitigation

\- safe demonstrations



============================================================

IMPORTANT

============================================================



You are a general cybersecurity assistant as well as a

CloudGuard project assistant.



Do not respond to every question with:



"I can only help with CloudGuard."



You can answer normal questions such as:



"What is cybersecurity?"



"What is SIEM?"



"What is GRC?"



"What is the difference between SIEM and EDR?"



"What is ISO 27001?"



"What is a firewall?"



"What is phishing?"



"What does an SOC analyst do?"



"What is IAM?"



"What is Zero Trust?"



and many other general questions.

"""





# ============================================================*

# GROQ CHAT*

# ============================================================*



def call_groq(

    message: str,

    history: List[ChatMessage],

    context: str,

) -> str:



    if not groq_client:



        raise RuntimeError(

            "GROQ_API_KEY is not configured."

        )



    messages = [



        {

            "role": "system",

            "content": (

                SYSTEM_PROMPT

                + "\n\n"

                + context

            ),

        }

    ]



    # Keep recent conversation only.

    for item in history[-12:]:



        if item.role not in {

            "user",

            "assistant",

        }:



            continue



        content = item.content.strip()



        if not content:

            continue



        messages.append(

            {

                "role": item.role,

                "content": content,

            }

        )



    messages.append(

        {

            "role": "user",

            "content": message,

        }

    )



    try:



        completion = (

            groq_client

            .chat

            .completions

            .create(

                model=GROQ_MODEL,

                messages=messages,

                temperature=0.3,

                max_tokens=1200,

            )

        )



        answer = (

            completion

            .choices[0]

            .message

            .content

        )



        if not answer:



            raise RuntimeError(

                "Groq returned an empty response."

            )



        return answer.strip()



    except Exception as error:



        print(

            f"[CloudGuard AI ERROR] {error}"

        )



        raise RuntimeError(

            f"Groq request failed: {error}"

        )





# ============================================================

# DETERMINISTIC FALLBACK

# ============================================================



def fallback_response(message: str) -> str:



    greeting = greeting_response(message)



    if greeting:



        return greeting



    return (

        "CloudGuard AI is currently unavailable because "

        "the Groq AI provider is not configured. "

        "The backend itself is running, but a valid "

        "GROQ_API_KEY is required for general AI answers."

    )





# ============================================================

# AI ASSISTANT ENDPOINT

# ============================================================



@app.post("/api/assistant")

def assistant(

    request: AssistantRequest

):



    message = request.message.strip()



    if not message:



        return {

            "answer": "Please enter a question.",

            "ai_enabled": bool(GROQ_API_KEY),

            "source": "CloudGuard",

        }



    # --------------------------------------------------------*

    # Greetings do not require Groq.*

    # --------------------------------------------------------*



    greeting = greeting_response(message)



    if greeting:



        return {

            "answer": greeting,

            "ai_enabled": bool(GROQ_API_KEY),

            "source": "CloudGuard greeting",

        }



    # --------------------------------------------------------*

    # No Groq key*

    # --------------------------------------------------------*



    if not groq_client:



        return {

            "answer": fallback_response(message),

            "ai_enabled": False,

            "source": "CloudGuard fallback",

        }



    # --------------------------------------------------------*

    # Only send CloudGuard findings when relevant.*

    # --------------------------------------------------------*



    if needs_cloudguard_context(message):



        context = build_cloudguard_context(

            message

        )



    else:



        context = (

            "No project-specific CloudGuard context "

            "is required for this question. "

            "Answer it as a general cybersecurity "

            "question."

        )



    # --------------------------------------------------------*

    # Call Groq*

    # --------------------------------------------------------*



    try:



        answer = call_groq(

            message=message,

            history=request.history,

            context=context,

        )



        return {

            "answer": answer,

            "ai_enabled": True,

            "source": "CloudGuard AI / Groq",

        }



    except Exception as error:



        # IMPORTANT:*

        # Do not pretend the API key is missing.*

        # Return the real provider error so the frontend*

        # can display a meaningful problem.*



        print(

            f"[CloudGuard AI ERROR] {error}"

        )



        return {

            "answer": (

                "I reached the CloudGuard backend, "

                "but the Groq AI request failed.\n\n"

                f"Reason: {error}"

            ),

            "ai_enabled": True,

            "source": "CloudGuard AI error",

            "error": str(error),

        }