import streamlit as st
from typing import Dict, List, Optional
import mimetypes

st.set_page_config(page_title="Data Help Desk", layout="centered")

# =============================================================================
# CONSTANTS & MAPPINGS
# =============================================================================

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
    "Security Data (excl. Risk Analytics)": [
        "CRIMS [Alpha]",
        "Marketplace [ESM]",
        "Legacy Systems",
        "Third party vendor",
        "Other or N/A"
    ],
    "Account Data (excl. Risk Analytics)": [
        "Pega (redirect to Pega team)",
        "Marketplace [EAM]",
        "CDP",
        "CRIMS/Appian (Raise Salesforce)",
        "Other"
    ],
    "Enviro, Social, Governance": [
        "Phoenix",
        "Legacy - CRIMS",
        "State Street CRIMS"
    ],
    "Benchmark Data": [
        "INDIGO",
        "B-ONE",
        "Phoenix",
        "Scope"
    ],
    "Product Data": [
        "Marketplace [EPM]",
        "[EPM]",
        "Other"
    ],
    "Asset Pricing": [
        "Quasar",
        "Phoenix",
        "Marketplace [EAPM]",
        "CRIMS",
        "Other"
    ],
    "LGR": [
        "State Street CRIMS",
        "Legacy - CRIMS",
        "MDMS"
    ],
    "Market Data / Vendor Data": [
        "Phoenix",
        "State Street CRIMS",
        "Quasar",
        "MDMS",
        "Legacy - CRIMS",
        "ARC"
    ],
    "Others": [
        "Phoenix",
        "State Street CRIMS",
        "Quasar",
        "MDMS",
        "Legacy - CRIMS",
        "ARC"
    ]
}

CATEGORY_MAP: Dict[str, List[str]] = {
    "Security Data (excl. Risk Analytics)": [
        "General Query",
        "Data Quality Issue",
        "Instrument Set-Up",
        "Share Class Set Up",
        "Wishlist Request"
    ],
    "Account Data (excl. Risk Analytics)": [
        "New Account Data Attribute Request",
        "Change to Existing Account Data Attribute",
        "Access request / EAM issue",
        "Account Data Quality Issue",
        "Other"
    ],
    "Enviro, Social, Governance": [
        "Data Quality (Security Detail Incorrect)",
        "Ratings Request",
        "Other Data Issue"
    ],
    "Benchmark Data": [
        "Corporate Actions Related",
        "Duplicate Securities",
        "Identifier Related",
        "Incomplete Data",
        "Data Quality Issue (Incorrect Value)",
        "Other"
    ],
    "Product Data": [
        "Access request / EPM issue",
        "Data Quality Query",
        "Request for new data field or dropdown option"
    ],
    "Asset Pricing": [
        "Asset Pricing Enquiry",
        "Access Issue",
        "Reporting Request",
        "Data Quality Issue",
        "Other"
    ],
    "LGR": [
        "General Query",
        "Security Set-up / Data",
        "Redemption / Repayment",
        "Classifications",
        "Valuation/Fund",
        "Issuer/Party",
        "Security Attributes",
        "RCA",
        "Pillar 3",
        "FLD",
        "NIC",
        "Intra Month Data Quality",
        "LGR Month End",
        "LGR Year End",
        "Data Quality Issue",
        "Others"
    ],
    "Market Data / Vendor Data": [
        "Request for New Market Data (Onboard New Service)",
        "Request for Access to Market Data (Existing)",
        "Request to Transfer Market Data Services",
        "Index Related Request",
        "Use and Contractual Rights Queries",
        "Vendor-related Issue",
        "Other"
    ],
    "Others": []
}

SUBCATEGORY_MAP: Dict[str, List[str]] = {
    "Instrument Set-Up": [
        "Accrued Interest",
        "Bond",
        "Asset Reporting",
        "Derivatives",
        "Equity",
        "Fund",
        "Money Market",
        "Mortgage",
        "Unlisted",
        "Corporate Action",
        "TBA",
        "Other instrument"
    ],
    "Index Data": [
        "Corporate Actions Related",
        "Duplicate Securities",
        "Identifier Related",
        "Incomplete Data",
        "Incorrect Value",
        "Index and Constituent Data Discrepancy",
        "Preview Data Related",
        "Stale Value",
        "Other"
    ]
}

CATEGORIES_WITHOUT_SUB = {
    "General Query",
    "Share Class Set Up",
    "Wishlist Request",
    "New Account Data Attribute Request",
    "Change to Existing Account Data Attribute",
    "Access request / EAM issue",
    "Account Data Quality Issue",
    "Other",
    "Data Quality (Security Detail Incorrect)",
    "Ratings Request",
    "Other Data Issue",
    "Access request / EPM issue",
    "Data Quality Query",
    "Request for new data field or dropdown option",
    "Asset Pricing Enquiry",
    "Access Issue",
    "Reporting Request",
    "Data Quality Issue",
    "General Query",
    "Security Set-up / Data",
    "Redemption / Repayment",
    "Classifications",
    "Valuation/Fund",
    "Issuer/Party",
    "Security Attributes",
    "RCA",
    "Pillar 3",
    "FLD",
    "NIC",
    "Intra Month Data Quality",
    "LGR Month End",
    "LGR Year End",
}

VENDOR_CATEGORIES = [
    "Request for New Market Data (Onboard New Service)",
    "Request for Access to Market Data (Existing)",
    "Request to Transfer Market Data Services",
    "Index Related Request",
    "Use and Contractual Rights Queries",
    "Vendor-related Issue",
    "Other"
]

ATTACHMENT_TYPES = ["csv", "xlsx", "jpg", "jpeg", "png", "pdf"]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def selectbox_with_placeholder(
    label: str,
    options: List[str],
    placeholder: str = "Please select",
    key: str = None
) -> Optional[str]:
    """Selectbox with placeholder option"""
    if not key:
        key = f"select_{label.lower().replace(' ', '_')}"
    display_options = [placeholder] + options
    choice = st.selectbox(label, display_options, index=0, key=key)
    return None if choice == placeholder else choice


def should_show_details(category: Optional[str]) -> bool:
    """Check if we should show subject/additional info fields"""
    if not category:
        return False
    if category == "Wishlist Request":
        return False  # Has its own special block
    return True


def display_attachments(attachments):
    """Display uploaded files in a nice format"""
    if not attachments:
        return

    st.markdown("**Uploaded files:**")
    for file in attachments:
        file_type, _ = mimetypes.guess_type(file.name)
        
        col_icon, col_info = st.columns([1, 5])
        
        with col_icon:
            if file_type and file_type.startswith("image/"):
                try:
                    st.image(file, width=90)
                except:
                    st.write("🖼️")
            elif file_type and "pdf" in file_type:
                st.write("📕")
            elif file_type and any(x in file_type for x in ["spreadsheet", "excel", "csv"]):
                st.write("📊")
            else:
                st.write("📄")
        
        with col_info:
            st.write(f"**{file.name}**")
            size_kb = file.size / 1024
            st.caption(f"{size_kb:.1f} KB  •  {file.type or 'unknown type'}")


# =============================================================================
# MAIN UI
# =============================================================================

st.title("Data Help Desk", text_alignment="center")
st.subheader("Data Query Ticket (DQT) Form", text_alignment="center")

# ─── Pre-filled / read-only fields ───
cols = st.columns(4)
with cols[0]:
    st.text_input("Requester:", value="Olaoye, Oyedele", disabled=True)
with cols[1]:
    st.text_input("Location:", value="London", disabled=True)
with cols[2]:
    st.text_input("Cost Center:", value="1234", disabled=True)
with cols[3]:
    st.text_input("Division:", value="Data Ops", disabled=True)

st.divider()

# ─── Core metadata ───
c1, c2, c3, c4 = st.columns(4)

with c1:
    request_type = st.selectbox("Request Type", ["Incident", "Request"], key="request_type")

with c2:
    product = selectbox_with_placeholder("Data Category", PRODUCTS, key="product_type")

is_risk = product == "Risk Analytics (Security/Account Level)"
is_vendor = product == "Market Data / Vendor Data"

with c3:
    risk_analytics_level = None
    market_type = None
    
    if is_risk:
        # Risk Analytics: Show Risk Analytics Level instead of Public/Private
        risk_analytics_level = selectbox_with_placeholder(
            "Risk Analytics Level",
            ["Instrument Level", "Account/Portfolio Level"],
            key="risk_level"
        )
    elif product in ["Security Data (excl. Risk Analytics)", "Asset Pricing"]:
        # Standard products: Show Public/Private
        market_type = selectbox_with_placeholder(
            "Public/Private",
            ["Public", "Private"],
            key="market_type"
        )

with c4:
    risk_engine = None
    related_systems = None
    
    if is_risk:
        # Risk Analytics: Show Risk Engine instead of Related System
        risk_engine = selectbox_with_placeholder(
            "Risk Engine",
            RISK_ENGINES,
            key="risk_engine"
        )
    elif product and not is_vendor:
        # Standard products: Show Related System
        related_systems = selectbox_with_placeholder(
            "Related System",
            RELATED_SYSTEM.get(product, []),
            key="related_system"
        )

st.divider()

# ─── Risk Analytics Specific Logic ───
data_source = None
euc_name = None

if is_risk and risk_engine:
    rc1, rc2 = st.columns(2)
    
    with rc1:
        # Conditional Data Source dropdown based on Risk Engine
        ds_options = DATA_SOURCE_LEGACY if risk_engine == "Axioma Legacy" else DATA_SOURCE_STOM
        data_source = selectbox_with_placeholder(
            "Data Source",
            ds_options,
            key="data_source"
        )
    
    with rc2:
        # EUC Name field appears only for specific data sources
        if data_source in ["EUCs Legacy", "EUC STOM"]:
            euc_name = st.text_input("EUC Name *", key="euc_name")

# ─── Standard Category Selection (Hidden if Risk Analytics) ───
category = None
sub_category = None

if not is_risk:
    c1, c2 = st.columns(2)
    
    with c1:
        if product and product in CATEGORY_MAP:
            category = selectbox_with_placeholder(
                "Category Type",
                CATEGORY_MAP[product],
                key="category"
            )
    
    with c2:
        if category and category not in CATEGORIES_WITHOUT_SUB and category in SUBCATEGORY_MAP:
            sub_category = selectbox_with_placeholder(
                "Sub Category Type",
                SUBCATEGORY_MAP[category],
                key="sub_category"
            )

st.divider()

# ─── Conditional Content Sections ───

# Initialize variables
subject = None
additional_info = None
detail_attachments = None
submitted = False

# WISHLIST REQUEST SECTION
if category == "Wishlist Request":
    st.info(
        "Use this template to request securities to be added to the LGIM State Street "
        "security universe for overnight Bloomberg enrichment (30 days)."
    )
    
    st.download_button(
        label="Download Security Wishlist request template",
        data=b"excel-template-placeholder",
        file_name="Security_Wishlist_Template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="wishlist_template_dl"
    )
    
    st.markdown(
        "Please fill out the template and attach it below with business justification.\n\n"
        "**Note:** There are costs associated with requesting Bloomberg data. "
        "Requests will be assessed and may be rejected or additional justification required."
    )
    
    wishlist_justification = st.text_area(
        "Business Justification *",
        key="wishlist_justification",
        height=120
    )
    
    st.markdown("##### Attachments")
    st.caption("Drag & drop files here (completed template + supporting images/documents) or click to browse")
    
    wishlist_attachments = st.file_uploader(
        label="Upload files",
        type=ATTACHMENT_TYPES,
        accept_multiple_files=True,
        key="wishlist_attachments",
        label_visibility="collapsed"
    )
    
    display_attachments(wishlist_attachments)
    
    st.divider()
    
    left, right = st.columns([3, 1])
    with right:
        with st.form("wishlist_submit_form", clear_on_submit=False):
            submitted = st.form_submit_button("Submit Ticket", use_container_width=False, type="primary")
    
    if submitted:
        errors = []
        if not wishlist_justification:
            errors.append("Business Justification is required.")
        if not wishlist_attachments:
            errors.append("Please attach at least the filled template.")
        
        if errors:
            for msg in errors:
                st.error(msg)
        else:
            st.success("Wishlist ticket submitted successfully!")
            with st.expander("Submission Summary", expanded=True):
                st.json({
                    "Requester": "Olaoye, Oyedele",
                    "Location": "London",
                    "Cost Center": "1234",
                    "Division": "Data Ops",
                    "Request Type": request_type,
                    "Product": product,
                    "Category": category,
                    "Justification": wishlist_justification[:100] + "...",
                    "Attachments": [f.name for f in wishlist_attachments] if wishlist_attachments else [],
                })

# VENDOR DATA SECTION
elif category in VENDOR_CATEGORIES:
    vendor_justification = st.text_area(
        "Business Justification *",
        key="vendor_justification",
        height=120
    )
    
    st.markdown("##### Attachments")
    st.caption("Drag & drop files here (completed template + supporting images/documents) or click to browse")
    
    vendor_attachments = st.file_uploader(
        label="Upload files",
        type=ATTACHMENT_TYPES,
        accept_multiple_files=True,
        key="vendor_attachments",
        label_visibility="collapsed"
    )
    
    display_attachments(vendor_attachments)
    
    st.divider()
    
    left, right = st.columns([3, 1])
    with right:
        with st.form("vendor_submit_form", clear_on_submit=False):
            submitted = st.form_submit_button("Submit Ticket", use_container_width=False, type="primary")
    
    if submitted:
        errors = []
        if not vendor_justification:
            errors.append("Business Justification is required.")
        if not vendor_attachments:
            errors.append("Please attach the required documents.")
        
        if errors:
            for msg in errors:
                st.error(msg)
        else:
            st.success("Vendor ticket submitted successfully!")
            with st.expander("Submission Summary", expanded=True):
                st.json({
                    "Requester": "Olaoye, Oyedele",
                    "Location": "London",
                    "Cost Center": "1234",
                    "Division": "Data Ops",
                    "Request Type": request_type,
                    "Product": product,
                    "Category": category,
                    "Justification": vendor_justification[:100] + "...",
                    "Attachments": [f.name for f in vendor_attachments] if vendor_attachments else [],
                })

# RISK ANALYTICS SECTION
elif is_risk and risk_engine:
    subject = st.text_input("Short Description *", key="subject")
    additional_info = st.text_area("Additional Information *", key="add_info", height=160)
    
    st.markdown("##### Attachments (optional)")
    st.caption("Drag & drop images, documents, spreadsheets…")
    
    detail_attachments = st.file_uploader(
        label="Upload files",
        type=ATTACHMENT_TYPES,
        accept_multiple_files=True,
        key="detail_attachments",
        label_visibility="collapsed"
    )
    
    display_attachments(detail_attachments)
    
    st.divider()
    
    left, right = st.columns([3, 1])
    with right:
        with st.form("risk_submit_form", clear_on_submit=False):
            submitted = st.form_submit_button("Submit Ticket", use_container_width=False, type="primary")
    
    if submitted:
        errors = []
        if not subject:
            errors.append("Short Description is required.")
        if not additional_info:
            errors.append("Additional Information is required.")
        if data_source in ["EUCs Legacy", "EUC STOM"] and not euc_name:
            errors.append("EUC Name is required for the selected Data Source.")
        
        if errors:
            for msg in errors:
                st.error(msg)
        else:
            st.success("Risk Analytics ticket submitted successfully!")
            with st.expander("Submission Summary", expanded=True):
                st.json({
                    "Requester": "Olaoye, Oyedele",
                    "Location": "London",
                    "Cost Center": "1234",
                    "Division": "Data Ops",
                    "Request Type": request_type,
                    "Product": product,
                    "Risk Analytics Level": risk_analytics_level,
                    "Risk Engine": risk_engine,
                    "Data Source": data_source,
                    "EUC Name": euc_name,
                    "Subject": subject,
                    "Additional Info": additional_info[:100] + "...",
                    "Attachments": [f.name for f in detail_attachments] if detail_attachments else [],
                })

# STANDARD SECTION (Category with details)
elif should_show_details(category):
    subject = st.text_input("Subject *", key="subject")
    additional_info = st.text_area("Additional Information *", key="add_info", height=160)
    
    st.markdown("##### Attachments (optional)")
    st.caption("Drag & drop images, documents, spreadsheets…")
    
    detail_attachments = st.file_uploader(
        label="Upload files",
        type=ATTACHMENT_TYPES,
        accept_multiple_files=True,
        key="detail_attachments",
        label_visibility="collapsed"
    )
    
    display_attachments(detail_attachments)
    
    st.divider()
    
    left, right = st.columns([3, 1])
    with right:
        with st.form("detail_submit_form", clear_on_submit=False):
            submitted = st.form_submit_button("Submit Ticket", use_container_width=False, type="primary")
    
    if submitted:
        errors = []
        if not product:
            errors.append("Data Category is required.")
        if not related_systems:
            errors.append("Related System is required.")
        if not category:
            errors.append("Category is required.")
        if not subject:
            errors.append("Subject is required.")
        if not additional_info:
            errors.append("Additional Information is required.")
        
        if errors:
            for msg in errors:
                st.error(msg)
        else:
            st.success("Ticket submitted successfully!")
            with st.expander("Submission Summary", expanded=True):
                st.json({
                    "Requester": "Olaoye, Oyedele",
                    "Location": "London",
                    "Cost Center": "1234",
                    "Division": "Data Ops",
                    "Request Type": request_type,
                    "Market Type": market_type,
                    "Product": product,
                    "Related System": related_systems,
                    "Category": category,
                    "Sub Category": sub_category,
                    "Subject": subject,
                    "Additional Info": additional_info[:100] + "...",
                    "Attachments": [f.name for f in detail_attachments] if detail_attachments else [],
                })

# PROMPT TO SELECT OPTIONS
elif product and not category and not is_risk:
    st.info("👆 Please select a **Category Type** above to continue.")
elif product and is_risk and not risk_engine:
    st.info("👆 Please select a **Risk Engine** above to continue.")
elif not product:
    st.info("👆 Please select a **Data Category** above to continue.")
