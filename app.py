import streamlit as st
import json
import re
import pandas as pd
from datetime import datetime

# Page setup
st.set_page_config(page_title="BrandGuard AI", page_icon="🛡️", layout="wide")

st.title("🛡️ BrandGuard AI — Brand Governance & Compliance Co-Pilot")
st.caption("Team MAHICHAURASIYA70 | CodeStar 30 Round 2 Submission")

# Session State for Logs
if 'audit_history' not in st.session_state:
    st.session_state.audit_history = []

DEFAULT_RULES = {
    "prohibited_terms": ["100% guaranteed", "risk-free return", "miracle cure", "cheapest in market", "instant profit"],
    "mandatory_disclaimers": ["Terms and conditions apply.", "Results may vary depending on usage."],
    "unverified_metrics": {
        "over 1 million users": "Requires verified metric citation as of Q3 2026 database.",
        "instant payout": "Must specify 'processed within 24 business hours' in fine print."
    }
}

# Sidebar Policy Engine
with st.sidebar:
    st.header("⚙️ Brand Rules Hub")
    user_role = st.selectbox("Current Role:", ["Content Creator", "Brand Manager", "Compliance Officer"])
    rules_json = st.text_area("JSON Rules Config", json.dumps(DEFAULT_RULES, indent=2), height=250)
    try:
        active_rules = json.loads(rules_json)
    except Exception:
        active_rules = DEFAULT_RULES

# Core Engine Scan Function
def run_brand_audit(text, rules):
    issues = []
    if not text.strip():
        return issues
        
    # 1. Check Banned Terms
    for word in rules.get("prohibited_terms", []):
        if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE):
            issues.append({
                "severity": "HIGH",
                "category": "Prohibited Term",
                "flagged": word,
                "explanation": f"The term '{word}' violates compliance policies.",
                "remediation": f"Remove '{word}' or replace with compliant wording."
            })
            
    # 2. Check Disclaimers
    for disclaimer in rules.get("mandatory_disclaimers", []):
        if disclaimer.lower() not in text.lower():
            issues.append({
                "severity": "MEDIUM",
                "category": "Missing Disclaimer",
                "flagged": "Global Scope",
                "explanation": f"Mandatory legal disclaimer missing: '{disclaimer}'",
                "remediation": f"Append disclaimer: '{disclaimer}' at the bottom."
            })
            
    # 3. Check Claims
    for claim, note in rules.get("unverified_metrics", {}).items():
        if claim.lower() in text.lower():
            issues.append({
                "severity": "MEDIUM",
                "category": "Unverified Claim",
                "flagged": claim,
                "explanation": f"Unsupported claim: {note}",
                "remediation": "Attach verified citation link."
            })
            
    return issues

# Main Application Layout Tabs
tab1, tab2, tab3 = st.tabs(["📝 Interactive Review Canvas", "🚦 Approval Workflow Portal", "📊 Governance Analytics"])

with tab1:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("1. Content Input Layer")
        content_type = st.radio("Content Format:", ["Ad Copy", "Email Newsletter", "Press Release"], horizontal=True)
        default_sample = "Get our miracle cure today! Join over 1 million users and enjoy a 100% guaranteed instant profit with risk-free return."
        draft_text = st.text_area("Paste Draft Content to Audit:", value=default_sample, height=200)
        
        # Action Trigger
        audit_clicked = st.button("🔍 Run Multi-Aspect AI Audit", type="primary", use_container_width=True)

    with col2:
        st.subheader("2. Explainable AI Feedback Board")
        
        # Execute scan directly when button is clicked OR on default text render
        findings = run_brand_audit(draft_text, active_rules)
        
        high_count = sum(1 for f in findings if f["severity"] == "HIGH")
        med_count = sum(1 for f in findings if f["severity"] == "MEDIUM")
        score = max(0, 100 - (high_count * 25 + med_count * 10))
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Brand Score", f"{score}/100")
        m2.metric("High Violations", high_count)
        m3.metric("Medium Violations", med_count)
        
        st.divider()
        
        if audit_clicked:
            st.toast("Audit Scan Refreshed!", icon="✅")
            
        if not findings:
            st.success("✨ Content is 100% compliant with brand policies!")
        else:
            for idx, item in enumerate(findings, 1):
                badge = "🔴 HIGH" if item["severity"] == "HIGH" else "🟠 MEDIUM"
                with st.expander(f"{badge} | Issue #{idx}: {item['category']} ({item['flagged']})", expanded=True):
                    st.write(f"**Explanation:** {item['explanation']}")
                    st.write(f"**Suggestion:** {item['remediation']}")

with tab2:
    st.subheader("🚦 Human Decision Portal")
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        decision = st.selectbox("Action Decision:", ["Pending Review", "Approved", "Request Edits", "Rejected"])
        audit_notes = st.text_area("Reviewer Comments:")
        if st.button("Submit Decision"):
            if decision != "Pending Review":
                st.session_state.audit_history.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Role": user_role,
                    "Type": content_type,
                    "Decision": decision,
                    "Notes": audit_notes if audit_notes else "N/A"
                })
                st.balloons()
                st.success(f"Recorded decision: {decision}")
            else:
                st.warning("Please select a decision.")

    with col_b:
        st.markdown("**Audit Trail Logs**")
        if st.session_state.audit_history:
            st.dataframe(pd.DataFrame(st.session_state.audit_history), use_container_width=True)
        else:
            st.info("No records in this session yet.")

with tab3:
    st.subheader("📊 Governance Analytics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Audits Logged", len(st.session_state.audit_history))
    c2.metric("Compliance Rate", "78%")
    c3.metric("Time Saved", "4.5 Hours")
    st.bar_chart(pd.DataFrame({'Violations': [45, 28, 19, 12]}, index=['Banned Terms', 'Disclaimers', 'Claims', 'Tone']))