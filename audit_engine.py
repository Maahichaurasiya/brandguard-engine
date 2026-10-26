import re

def run_brand_audit(text: str, rules: dict) -> list:
    issues = []
    
    if not text:
        return issues
        
    # 1. Prohibited Terms
    for word in rules.get("prohibited_terms", []):
        if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE):
            issues.append({
                "severity": "HIGH",
                "category": "Prohibited Claim / Term",
                "flagged": word,
                "explanation": f"The term '{word}' violates strict marketing compliance policies.",
                "remediation": f"Remove '{word}' or replace with compliant, approved phrasing."
            })
            
    # 2. Mandatory Disclaimers
    for disclaimer in rules.get("mandatory_disclaimers", []):
        if disclaimer.lower() not in text.lower():
            issues.append({
                "severity": "MEDIUM",
                "category": "Missing Legal Disclaimer",
                "flagged": "Document Scope",
                "explanation": f"Mandatory disclosure omitted: '{disclaimer}'",
                "remediation": f"Append disclaimer: '{disclaimer}' at the bottom of the copy."
            })
            
    # 3. Unverified Claims
    for claim, note in rules.get("unverified_metrics", {}).items():
        if claim.lower() in text.lower():
            issues.append({
                "severity": "MEDIUM",
                "category": "Unverified Metric / Claim",
                "flagged": claim,
                "explanation": f"Unsupported claim flagged: {note}",
                "remediation": "Attach verified citation link or update to qualified metric statement."
            })
            
    return issues