
import streamlit as st
from typing import Dict, List, Optional
import mimetypes

st.set_page_config(page_title="Data Help Desk", layout="centered")

# -----------------------------------------------------------------------------
# Constants and mappings
# -----------------------------------------------------------------------------
PRODUCTS = [
    "Security Data [ESM]",
    "Account Data [EAM]",
    "Enviro, Social, Governance [ESG]",
    "Benchmark Data [EBM]",
    "Product Data [EPM]",
    "Pricing [EAPM]",
    "LGR",
    "Market Data / Vendor Data",
    "Others",
]


RELATED_SYSTEM: Dict[str, List[str]] = {
    
    "Security Data [ESM]": [
        "Azure - State Street CRIMS",
        "Legacy - CRIMS",
        "MDMS2"
        ],
    "Account Data [EAM]":[
        "Pega (redirect to Pega team)",
        "EAM",
        "CDP",
        "CRIMS/Appian (Raise Salesforce)",
        "Other"
        ],
    "ESG":[
        "Phoenix",
        "Legacy - CRIMS",
        "Azure - State Street CRIMS",
        ],
    "Benchmark Data [EBM]":[
        "Axioma",
        "Guideline Monitoring",
        "iLID",
        "INDIGO Equities",
        "INDIGO Fixed Income",
        "Performance (B-ONE)",
        "Phoenix",
        "Scope"
        ],
    "Product Data [EPM]":[
        "EPM",
        "CDP",
        "Other"
        ],
    "Pricing [EAPM]":[
        "Quasar",
        "CDP",
        "CRIMS",
        "Other"
        ],
    "LGR":[
        "Azure - State Street CRIMS",
        "Legacy - CRIMS",
        "MDMS"
        ],
    "Private Credit":[
        "Phoenix",
        "Azure - State Street CRIMS",
        "Quasar"
        ],
    "Vendor Data":[
        "Phoenix",
        "Azure - State Street CRIMS",
        "Quasar"
        ],
    "Others": [
        "Phoenix",
        "Azure - State Street CRIMS",
        "Quasar",
        "MDMS",
        "Legacy - CRIMS",
        "ARC"
        ]

}

CATEGORY_MAP: Dict[str, List[str]] = {
    "Security Data [ESM]": [
        "General Query",
        "Instrument Set-Up",
        "Share Class Set Up",
        "Wishlist Security",
    ],
    "Account Data [EAM]":[
        "New Account Data Attribute Request - L2", 
        "Change to Existing Account Data Attribute - L2",
        "Access request / EAM issue -L1",
        "EAM Development (Enhancement/Functionality) Request - L2",
        "Account Data Quality Issue - L1",
        "Account Data Report Request - L2",
        "Other - L1"
        ],
    "ESG":[
        "Data Issue", 
        "Security Detail Incorrect"
        ],
    "Benchmark Data [EBM]":[
        "Index Data"
        ],
    "Product Data [EPM]":[
        "Access request / EPM issue - L1",
        "Data quality query - L1",	
        "Request for new data field or dropdown option - L1"
        ],
    "Pricing [EAPM]":[
        "Data Query",	
        "Vendor Data Request",	
        "Access request / EPM issue",	
        "Reporting Request",	
        "Other"
        ],
    "LGR":[
        "RCA - L2",	
        "Pillar 3 - L1", 
        "FLD",	
        "NIC",
        "Intra Month Data Quality - L2",
        "LGR Month End", 
        "LGR Year End", 	
        "Others"
        ],
    "Vendor Data":[
        "Request for New Market Data (Onboard New Service)",
        "Request for Access to Market Data (Existing)",
        "Request to Transfer Market Data Services",
        "Index Related Request",
        "Use and Contractual Rights Queries",
        "Other"
        ],
    "Others": [
    #placeholder   
    ]
    
        
    # Add more products → categories when needed
}


SUBCATEGORY_MAP: Dict[str, List[str]] = {
    "Instrument Set-Up": [
        "Accrued Interest", "Bond", "Asset Reporting", "Derivatives",
        "Equity", "Fund", "Money Market", "Mortgage", "Unlisted",
        "Corporate Action", "TBA", "Other instrument",
    ],
    "Index Data":[
        "Corporate Actions Related", 
        "Duplicate Securities",
        "Identifier Related",
        "Incomplete Data",
        "Incorrect Value",
        "Index and Constituent Data Discrepancy",
        "Preview Data Related",
        "Stale Value",
        "other"
        ]
}

CATEGORIES_WITHOUT_SUB = {"General Query", "Share Class Set Up", "Wishlist Security",  "New Account Data Attribute Request - L2", 
        "Change to Existing Account Data Attribute - L2",
        "Access request / EAM issue -L1",
        "EAM Development (Enhancement/Functionality) Request - L2",
        "Account Data Quality Issue - L1",
        "Account Data Report Request - L2",
        "Other - L1", "Data Issue", 
        "Security Detail Incorrect", "Access request / EPM issue - L1",
        "Data quality query - L1",	
        "Request for new data field or dropdown option - L1", "Data Query",	
        "Vendor Data Request",	
        "Access request / EPM issue",	
        "Reporting Request",	
        "Other", "FLD",	
        "NIC",
        "Intra Month Data Quality - L2",	
        "RCA - L2",	
        "Pillar 3 - L1" }

ATTACHMENT_TYPES = ["csv", "xlsx", "jpg", "jpeg", "png", "pdf"]

Vendor_category = [
        "Request for New Market Data (Onboard New Service)",
        "Request for Access to Market Data (Existing)",
        "Request to Transfer Market Data Services",
        "Index Related Request",
        "Use and Contractual Rights Queries",
        "Other"
        ]

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def selectbox_with_placeholder(
    label: str,
    options: List[str],
    placeholder: str = "Please select",
    key: str = None
) -> Optional[str]:
    if not key:
        key = f"select_{label.lower().replace(' ', '_')}"
    display_options = [placeholder] + options
    choice = st.selectbox(label, display_options, index=0, key=key)
    return None if choice == placeholder else choice

def should_show_details(category: Optional[str], sub_category: Optional[str]) -> bool:
    if not category:
        return False
    if category == "Wishlist Security":
        return False  # has its own special block
    if sub_category:
        return True
    if category in CATEGORIES_WITHOUT_SUB:
        return True
    return False

def display_attachments(attachments):
    """Show nice preview/list of uploaded files"""
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









#-----------------------------------------------------------------------------
# Main UI ─────────────────────────────────────────────────────────────────────
# -----------------------------------------------------------------------------
st.title("Data Help Desk", text_alignment="center")
st.subheader("Data Query Ticket (DQT) Form", text_alignment="center")

# ── Pre-filled / read-only fields ──
cols = st.columns(4)
with cols[0]: st.text_input("Requester:", value="Olaoye, Oyedele", disabled=True)
with cols[1]: st.text_input("Location:", value="London", disabled=True)
with cols[2]: st.text_input("Cost Center:", value="1234", disabled=True)
with cols[3]: st.text_input("Division:", value="Data Ops", disabled=True)

st.divider()

# ── Core metadata ──
c1, c2, c3, c4 = st.columns(4)
with c1:
    request_type = st.selectbox("Request Type", ["Incident", "Request"], key="request_type")
    
with c2:
    product = selectbox_with_placeholder("Data Category", PRODUCTS, key="product_type")

with c3:
    market_type = None
    if product == "Security Data [ESM]" or product ==  "Pricing [EAPM]":
        market_type = selectbox_with_placeholder("Market Type", ["Public", "Private"], key="market_type")

with c4:
    if product:
    # Show related systems based on the selected product type
        related_systems = selectbox_with_placeholder("Related System",RELATED_SYSTEM.get(product, []),key="related_system")

st.divider()

# ── Category ────────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)
with c1:
    category = None
    if product and product in CATEGORY_MAP:
        category = selectbox_with_placeholder("Category Type", CATEGORY_MAP[product], key="category")

# ── Sub-category (only shown when relevant) ────────────────────────────────
with c2:
    sub_category = None
    if (
        category
        and category not in CATEGORIES_WITHOUT_SUB
        and category in SUBCATEGORY_MAP
        and SUBCATEGORY_MAP[category]  # not empty
    ):
        sub_category = selectbox_with_placeholder(
            "Sub Category Type",
            SUBCATEGORY_MAP[category],
            key="sub_category"
    )

# ── Conditional content ─────────────────────────────────────────────────────

subject = None
additional_info = None
vendor_justification = None
vendor_attachments = None
wishlist_justification = None
wishlist_attachments = None
detail_attachments = None
template_downloaded = False
submitted = False 


if category in Vendor_category:
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
    
    # Submit ─ compact & right-aligned
    left, right = st.columns([3, 1])
    
    with right:
        with st.form("submit_form", clear_on_submit=False):
            submitted = st.form_submit_button(
                "Submit Ticket",
                use_container_width=False,
                type="primary"
            )


if category == "Wishlist Security":
    st.info(
        "Use this template to request securities to be added to the LGIM State Street "
        "security universe for overnight Bloomberg enrichment (30 days)." 
    )

    st.download_button(
        label="Download Security Wishlist request template",
        data=b"excel-template-placeholder",  # ← replace with real bytes / file content
        file_name="Security_Wishlist_Template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="wishlist_template_dl"
    )
    template_downloaded = True

    st.markdown(
        "Please fill the template, attach it below, and provide business justification."   
        "\nPlease download the request template below."
        "Please, provide the necessary information on the securities required to be enriched." 
        "\n\nFurther guidance can be found in the template." " Once filled in please attach it to this request and submit it.\n"
    )
    st.info("There are costs associated with requesting Bloomberg data, therefore requests will be assessed and may be rejected or additional justification required."
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
    
    # Submit ─ compact & right-aligned
    left, right = st.columns([3, 1])
    
    with right:
        with st.form("submit_form", clear_on_submit=False):
            submitted = st.form_submit_button(
                "Submit Ticket",
                use_container_width=False,
                type="primary"
            )
    

    
elif should_show_details(category, sub_category):
    subject = st.text_input("Subject *", key="subject")
    
    additional_info = st.text_area(
        "Additional Information *", key="add_info", height=160
    )
    
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
    
    # Submit ─ compact & right-aligned
    left, right = st.columns([3, 1])
    
    with right:
        with st.form("submit_form", clear_on_submit=False):
            submitted = st.form_submit_button(
                "Submit Ticket",
                use_container_width=False,
                type="primary"
            )
    
    # ── Validation & result ─────────────────────────────────────────────────────
if submitted:
    errors = []

    if not product:
        errors.append("Product Type is required.")
    if product == "Security Data [ESM]" and not category:
        errors.append("Category is required for Security Data [ESM].")
    
    if not related_systems:
        errors.append("Related System is required.")
    if related_systems and not category:
        errors.append("Category is required.")

    if category == "Wishlist Security":
        if not wishlist_justification:
            errors.append("Business Justification is required for Wishlist Security.")
        if not wishlist_attachments:
            errors.append("Please attach at least the filled template for Wishlist Security.")
    
    if category in Vendor_category:
        if not vendor_justification:
            errors.append("Business Justification is required for Vendor Data.")
        if not vendor_attachments:
            errors.append("Please attach the completed template for Vendor Data.")
    
    elif should_show_details(category, sub_category):
        if not subject:
            errors.append("Subject is required.")
        if not additional_info:
            errors.append("Additional Information is required.")

    if errors:
        for msg in errors:
            st.error(msg)
    else:
        st.success("Ticket submitted successfully!")

        attachments_count = 0
        attachment_names = []

        if category == "Wishlist Security" and wishlist_attachments:
            attachments_count = len(wishlist_attachments)
            attachment_names = [f.name for f in wishlist_attachments]
        elif detail_attachments:
            attachments_count = len(detail_attachments)
            attachment_names = [f.name for f in detail_attachments]
            
        if category in Vendor_category and vendor_attachments:
            attachments_count = len(vendor_attachments)
            attachment_names = [f.name for f in vendor_attachments]
        elif detail_attachments:
            attachments_count = len(detail_attachments)
            attachment_names = [f.name for f in detail_attachments]

        with st.expander("Submission Summary", expanded=True):
            st.json({
                "Requester": "Olaoye, Oyedele",
                "Location": "London",
                "Cost Center": "1234",
                "Division": "Data Ops",
                "Request Type": request_type,
                "Market Type": market_type,
                "Product": product,
                "Category": category,
                "Sub Category": sub_category,
                "Subject": subject,
                "Additional Info": additional_info,
                "Wishlist Justification": wishlist_justification,
                "Attachments Count": attachments_count,
                "Attachment Names": attachment_names,
                "Template Downloaded": template_downloaded,
        })
