import streamlit as st
from typing import Dict, List, Optional
import mimetypes

st.set_page_config(page_title="Data Help Desk", layout="centered")

# -----------------------------------------------------------------------------
# Constants and mappings
# -----------------------------------------------------------------------------
PRODUCTS = [
    "Security Data (excl. Risk Analytics)",
    "Account Data (excl. Risk Analytics)",
    "Enviro, Social, Governance",
    "Benchmark Data",
    "Product Data",
    "Asset Pricing",
    "LGR",
    "Market Data / Vendor Data",
    "Risk Analytics (Security/Account Level)",
    "Others"
]


RISK_ENGINES = ["Axioma Legacy", "Axioma STOM", "PORT+ STOM", "MARS STOM"]
DATA_SOURCE_LEGACY = ["CDP", "Snowflake", "EUCs Legacy"]
DATA_SOURCE_STOM = ["CDP", "Snowflake", "CRIMS", "EUC STOM"]

RELATED_SYSTEM: Dict[str, List[str]] = {
    "Security Data (excl. Risk Analytics)": ["CRIMS [Alpha]","Marketplace [ESM]", "Legacy Systems", "Third party vendor", "Other or N/A"],
    "Account Data (excl. Risk Analytics)": ["Pega (redirect to Pega team)", "Marketplace [EAM]", "CDP", "CRIMS/Appian (Raise Salesforce)", "Other"],
    "Enviro, Social, Governance": ["Phoenix", "Legacy - CRIMS", "State Street CRIMS"],
    "Benchmark Data": ["INDIGO", "B-ONE", "Phoenix", "Scope"],
    "Product Data": ["Marketplace [EPM]", "[EPM]", "Other"],
    "Asset Pricing": ["Quasar", "Phoenix", "Marketplace [EAPM]", "CRIMS", "Other"],
    "LGR": ["State Street CRIMS", "Legacy - CRIMS", "MDMS"],
    "Market Data / Vendor Data": ,
    "Risk Analytics (Security/Account Level)"",
    "Others": ["Phoenix", "State Street CRIMS", "Quasar", "MDMS", "Legacy - CRIMS", "ARC"]
}

CATEGORY_MAP: Dict[str, List[str]] = {
    "Security Data (excl. Risk Analytics)": ["General Query", "Data Quality Issue", "Instrument Set-Up", "Accrued Interest", "Share Class Set Up", "Wishlist Request"],
    "Account Data (excl. Risk Analytics)": ["New Account Data Attribute Request", "Change to Existing Account Data Attribute", "Access request / EAM issue", "Account Data Quality Issue", "Other"],
    "Enviro, Social, Governance": [ "Data Quality (Security Detail Incorrect)", "Ratings Request", "Other Data Issue"],
    "Benchmark Data": ["Corporate Actions Related", "Duplicate Securities", "Identifier Related", "Incomplete Data", "Data Quality Issue (Incorrect Value)", "other"],
    "Product Data": ["Access request / EPM issue", "Data Quality Issue (Data Quality Query)", "Request for new data field or dropdown option"],
    "Asset Pricing": ["Asset Pricing Enquiry", "Access Issue", "Reporting Request", "Data Quality Issue", "Other"],
    "LGR": ["General Query", "Security Set-up / Data", "Redemption / Repayment", "Classifications", "Valuation/Fund", "Issuer/Party", "Security Attributes", "RCA", "Pillar 3", "FLD", "NIC", "Intra Month Data Quality", "LGR Month End", "LGR Year End", "Data Quality Issue", "Others"],
    "Market Data / Vendor Data": ["Request for New Market Data (Onboard New Service)", "Request for Access to Market Data (Existing)", "Request to Transfer Market Data Services", "Index Related Request", "Use and Contractual Rights Queries", "Vendor-related Issue", "Other"],
    "Others": []
}

CATEGORIES_WITHOUT_SUB = {"General Query", "Share Class Set Up", "Wishlist Request", "New Account Data Attribute Request", "Change to Existing Account Data Attribute", "Access request / EAM issue", "Account Data Quality Issue", "Other", "Data Issue", "Security Detail Incorrect", "Access request / EPM issue", "Data quality query", "Request for new data field or dropdown option", "Asset Pricing enquiry", "New Asset Request", "Reporting Request", "FLD", "NIC", "Intra Month Data Quality", "RCA", "Security Attributes"}

ATTACHMENT_TYPES = ["csv", "xlsx", "jpg", "jpeg", "png", "pdf"]

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def selectbox_with_placeholder(label: str, options: List[str], placeholder: str = "Please select", key: str = None) -> Optional[str]:
    if not key: key = f"select_{label.lower().replace(' ', '_')}"
    display_options = [placeholder] + options
    choice = st.selectbox(label, display_options, index=0, key=key)
    return None if choice == placeholder else choice

def display_attachments(attachments):
    if not attachments: return
    st.markdown("**Uploaded files:**")
    for file in attachments:
        st.write(f"📄 **{file.name}** ({file.size/1024:.1f} KB)")

# -----------------------------------------------------------------------------
# Main UI
# -----------------------------------------------------------------------------
st.title("Data Help Desk")
st.subheader("Data Query Ticket (DQT) Form")

# Static Fields
cols = st.columns(4)
with cols[0]: st.text_input("Requester:", value="Olaoye, Oyedele", disabled=True)
with cols[1]: st.text_input("Location:", value="London", disabled=True)
with cols[2]: st.text_input("Cost Center:", value="1234", disabled=True)
with cols[3]: st.text_input("Division:", value="Data Ops", disabled=True)

st.divider()

# Core Metadata
c1, c2, c3, c4 = st.columns(4)
with c1:
    query_type = st.selectbox("Request Type", ["Incident", "Request"], key="query_type")
with c2:
    product = selectbox_with_placeholder("Data Category", PRODUCTS, key="product_type")

is_risk = (product == "Risk Analytics (Security/Account Level)")

with c3:
    risk_analytics_level = None
    market_type = None
    if is_risk:
        # Requirement 2 & 3: Risk Analytics Level replaces Public/Private
        risk_analytics_level = selectbox_with_placeholder("Risk Analytics Level", ["Instrument Level", "Account/Portfolio Level"], key="risk_level")
    elif product in ["Security Data (excl. Risk Analytics)", "Asset Pricing"]:
        market_type = selectbox_with_placeholder("Public/Private", ["Public", "Private"], key="market_type")

with c4:
    risk_engine = None
    related_systems = None
    if is_risk:
        # Requirement 5 & 6: Risk Engine replaces Related System
        risk_engine = selectbox_with_placeholder("Risk Engine", RISK_ENGINES, key="risk_engine")
    elif product and product != "Market Data / Vendor Data":
        related_systems = selectbox_with_placeholder("Related System", RELATED_SYSTEM.get(product, []), key="related_system")

st.divider()

# ── Risk Analytics Specific Logic (Requirement 7, 8, 9) ──
data_source = None
euc_name = None

if is_risk and risk_engine:
    rc1, rc2 = st.columns(2)
    with rc1:
        # Requirement 8: Conditional Data Source dropdowns
        ds_options = DATA_SOURCE_LEGACY if risk_engine == "Axioma Legacy" else DATA_SOURCE_STOM
        data_source = selectbox_with_placeholder("Data Source", ds_options, key="data_source")
    
    with rc2:
        # Requirement 9: EUC Name field
        if data_source in ["EUCs Legacy", "EUC STOM"]:
            euc_name = st.text_input("EUC Name", key="euc_name")

# ── Standard Category Selection (Hidden if Risk Analytics) ──
category = None
sub_category = None

if not is_risk:
    c1, c2 = st.columns(2)
    with c1:
        if product and product in CATEGORY_MAP:
            category = selectbox_with_placeholder("Category Type", CATEGORY_MAP[product], key="category")
    with c2:
        if category and category not in CATEGORIES_WITHOUT_SUB:
            # Note: Assuming SUBCATEGORY_MAP exists from your previous code
            # (Keeping logic consistent with your snippet)
            pass 

# ── Final Description Fields ──
# "Short Description and Additional Information fields should Follow the EUC Name"
if (is_risk and risk_engine) or (not is_risk and category):
    subject = st.text_input("Short Description *", key="subject")
    additional_info = st.text_area("Additional Information *", key="add_info", height=160)
    
    detail_attachments = st.file_uploader("Upload files", type=ATTACHMENT_TYPES, accept_multiple_files=True, key="detail_attachments")
    display_attachments(detail_attachments)
    
    if st.button("Submit Ticket", type="primary"):
        st.success("Ticket Submitted!")
        # Logic for processing would go here
