import pandas as pd
from datetime import datetime

def format_audit_logs(audit_history: list) -> pd.DataFrame:
    """Converts session decision logs into a structured Pandas DataFrame."""
    if not audit_history:
        return pd.DataFrame(columns=["Timestamp", "Role", "Content Type", "Decision", "Notes"])
    return pd.DataFrame(audit_history)

def calculate_brand_health(findings: list) -> int:
    """Calculates overall brand safety score out of 100 based on severity weightage."""
    high_sev = sum(1 for f in findings if f["severity"] == "HIGH")
    med_sev = sum(1 for f in findings if f["severity"] == "MEDIUM")
    score = max(0, 100 - (high_sev * 25 + med_sev * 10))
    return score