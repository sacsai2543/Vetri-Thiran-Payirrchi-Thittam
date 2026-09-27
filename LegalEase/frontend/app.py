import os
import sys
from pathlib import Path
import streamlit as st
import requests

# Set path to include project root
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import (
    API_URL,
    DOC_LOGO_PATH,
    WEB_LOGO_PATH,
    IMAGE_DIR,
    DOCS_DIR
)
from ai_core.generator import (
    format_docx,
    format_pdf,
    format_html_preview,
    sanitize_text
)
from ai_core.gemini_generator import GeminiDocumentGenerator
from image.generate_logos import generate_all_logos

# Ensure logos and directories are generated
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)
if not DOC_LOGO_PATH.exists() or not WEB_LOGO_PATH.exists():
    generate_all_logos()

# Page configuration
st.set_page_config(
    page_title="LegalEase - AI Legal Document Generator",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling for premium legal AI aesthetic
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #0F172A;
        color: #F1F5F9;
    }
    
    /* Header Card */
    .header-container {
        text-align: center;
        padding-bottom: 20px;
    }
    
    .header-subtext {
        color: #94A3B8;
        font-size: 15px;
        margin-top: -8px;
        margin-bottom: 20px;
    }
    
    /* Form Inputs */
    .stTextInput > label, .stTextArea > label, .stSelectbox > label {
        color: #E2E8F0 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 1px #38BDF8 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.45) !important;
        transform: translateY(-1px);
    }
    
    /* Download Buttons */
    .download-btn-group {
        display: flex;
        gap: 10px;
        margin-top: 15px;
    }
    
    /* Footer */
    .footer-bar {
        text-align: center;
        color: #64748B;
        font-size: 13px;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "show_edit" not in st.session_state:
    st.session_state.show_edit = False
if "doc_type" not in st.session_state:
    st.session_state.doc_type = "Freelance Work Contract"
if "parties_val" not in st.session_state:
    st.session_state.parties_val = "Jane Doe (Service Provider), TechNova Inc. (Client)"
if "terms_val" not in st.session_state:
    st.session_state.terms_val = "Work must be delivered by May 15, 2025; Payment will be made within 7 days of invoice; The client retains intellectual property rights; Confidentiality must be maintained at all times; Either party may terminate with 15 days notice"
if "dates_val" not in st.session_state:
    st.session_state.dates_val = "April 15, 2025"

# PRESET TEMPLATES FOR CONVENIENCE
PRESET_TEMPLATES = {
    "Select a preset template or enter custom details": {
        "doc_type": "",
        "parties": "",
        "terms": "",
        "dates": ""
    },
    "Scenario 1: Employment Contract": {
        "doc_type": "Employment Contract",
        "parties": "Acme Ventures Corp. (Employer), Johnathan Miller (Employee)",
        "terms": "Position: Senior Software Engineer; Annual Salary: $120,000 paid semi-monthly; 20 days annual paid time off; Comprehensive health and 401(k) benefits; Standard non-disclosure and invention assignment clauses apply; Employment is at-will with 2 weeks standard termination notice",
        "dates": "May 1, 2025"
    },
    "Scenario 2: Non-Disclosure Agreement (NDA)": {
        "doc_type": "Non-Disclosure Agreement (NDA)",
        "parties": "Apex Innovations LLC (Disclosing Party), Sarah Connor (Receiving Party)",
        "terms": "Information disclosed regarding project 'CyberCore' is strictly confidential; Non-disclosure obligations remain in effect for 3 years; Receiving party agrees to take reasonable security precautions; Exceptions apply only to publicly available information or court subpoenas",
        "dates": "April 20, 2025"
    },
    "Scenario 3: Residential Lease Agreement": {
        "doc_type": "Residential Lease Agreement",
        "parties": "Robert Sterling (Landlord), Alice Johnson (Tenant)",
        "terms": "Premises located at 742 Evergreen Terrace, Springfield; Monthly rent of $1,800 due on the 1st of each month; Security deposit of $1,800 held in escrow; No pets permitted without written approval; Landlord responsible for structural maintenance; Tenant responsible for utility bills",
        "dates": "June 1, 2025"
    },
    "Scenario 4: Freelance Work Contract": {
        "doc_type": "Freelance Work Contract",
        "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
        "terms": "Work must be delivered by May 15, 2025; Payment will be made within 7 days of invoice; The client retains intellectual property rights; Confidentiality must be maintained at all times; Either party may terminate with 15 days notice",
        "dates": "April 15, 2025"
    }
}

# --- HEADER SECTION ---
col1, col2, col3 = st.columns([1, 2.2, 1])
with col2:
    if WEB_LOGO_PATH.exists():
        st.image(str(WEB_LOGO_PATH), use_container_width=True)
    elif DOC_LOGO_PATH.exists():
        st.image(str(DOC_LOGO_PATH), use_container_width=True)

st.markdown("<h2 style='text-align: center; color: #F8FAFC; margin-top: -10px; font-weight: 700;'>AI Legal Document Generator</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 14.5px;'>Generate customized, court-ready contracts, NDAs, and agreements powered by Gemini AI</p>", unsafe_allow_html=True)

# Preset dropdown selector
preset_choice = st.selectbox(
    "📋 Quick Template Presets (Optional):",
    options=list(PRESET_TEMPLATES.keys()),
    index=0
)

if preset_choice != "Select a preset template or enter custom details":
    chosen = PRESET_TEMPLATES[preset_choice]
    st.session_state.doc_type = chosen["doc_type"]
    st.session_state.parties_val = chosen["parties"]
    st.session_state.terms_val = chosen["terms"]
    st.session_state.dates_val = chosen["dates"]

# --- INPUT FORM ---
with st.container():
    doc_type_input = st.text_input(
        "Document Type (Ex. Agreement, Contract, NDA)",
        value=st.session_state.doc_type,
        placeholder="e.g. Freelance Work Contract"
    )
    
    parties_input = st.text_area(
        "Parties Involved",
        value=st.session_state.parties_val,
        height=75,
        placeholder="e.g. Jane Doe (Service Provider), TechNova Inc. (Client)"
    )
    
    terms_input = st.text_area(
        "Terms & Conditions (Use semicolons for bullet points)",
        value=st.session_state.terms_val,
        height=110,
        placeholder="e.g. Work must be delivered by May 15, 2025; Payment within 7 days of invoice; IP transferred upon full payment;"
    )
    
    dates_input = st.text_input(
        "Effective Date",
        value=st.session_state.dates_val,
        placeholder="e.g. April 15, 2025"
    )

# --- ACTION BUTTON ---
col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    generate_clicked = st.button("⚡ Generate Document", use_container_width=True)

if generate_clicked:
    if not doc_type_input.strip():
        st.error("Please provide a Document Type to proceed.")
    else:
        with st.spinner("Generating professional legal document with Gemini AI..."):
            doc_result = None
            
            # Try contacting FastAPI Backend
            try:
                payload = {
                    "document_type": doc_type_input.strip(),
                    "parties": parties_input.strip(),
                    "terms": terms_input.strip(),
                    "dates": dates_input.strip()
                }
                res = requests.post(f"{API_URL}/generate", json=payload, timeout=25)
                if res.status_code == 200:
                    doc_result = res.json().get("document", "")
            except Exception:
                # Direct AI fallback if FastAPI backend is not active
                fallback_gen = GeminiDocumentGenerator()
                doc_result = fallback_gen.generate_document(
                    document_type=doc_type_input.strip(),
                    parties=parties_input.strip(),
                    terms=terms_input.strip(),
                    dates=dates_input.strip()
                )

            if doc_result:
                st.session_state.generated_text = sanitize_text(doc_result)
                st.session_state.current_doc_type = doc_type_input.strip()
                st.session_state.show_edit = False

# --- OUTPUT AND PREVIEW SECTION ---
if st.session_state.generated_text:
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.success("✅ Document Generated Successfully!")

    # Styled HTML Preview
    st.markdown("### 📄 Document Preview")
    html_rendered = format_html_preview(st.session_state.generated_text)
    st.markdown(html_rendered, unsafe_allow_html=True)

    # Edit Toggle & Editor
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    edit_col1, edit_col2 = st.columns([1, 3])
    with edit_col1:
        if st.button("🖊️ Click to Edit Document"):
            st.session_state.show_edit = not st.session_state.show_edit

    if st.session_state.show_edit:
        st.markdown("#### Edit Document Below:")
        edited_content = st.text_area(
            label="Document Editor",
            value=st.session_state.generated_text,
            height=320,
            label_visibility="collapsed"
        )
        if edited_content != st.session_state.generated_text:
            st.session_state.generated_text = edited_content
            st.rerun()

    # Export & Download Section
    st.markdown("### 💾 Download Options")
    
    current_doc_type = getattr(st.session_state, "current_doc_type", "legal_document")
    file_prefix = current_doc_type.lower().replace(" ", "_").replace("/", "_")
    logo_for_export = str(DOC_LOGO_PATH) if DOC_LOGO_PATH.exists() else None

    # Prepare document formats
    txt_data = st.session_state.generated_text.encode("utf-8")
    
    try:
        docx_data = format_docx(
            text=st.session_state.generated_text,
            doc_type=current_doc_type,
            logo_path=logo_for_export
        )
    except Exception as e:
        docx_data = None
        st.warning(f"DOCX formatting notice: {e}")

    try:
        pdf_data = format_pdf(
            text=st.session_state.generated_text,
            doc_type=current_doc_type,
            logo_path=logo_for_export
        )
    except Exception as e:
        pdf_data = None
        st.warning(f"PDF formatting notice: {e}")

    # 3 Download Buttons
    dcol1, dcol2, dcol3 = st.columns(3)
    
    with dcol1:
        st.download_button(
            label="📄 Download as .TXT",
            data=txt_data,
            file_name=f"{file_prefix}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
    with dcol2:
        if docx_data:
            st.download_button(
                label="📝 Download as .DOCX",
                data=docx_data,
                file_name=f"{file_prefix}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        else:
            st.button("📝 DOCX Unavailable", disabled=True, use_container_width=True)

    with dcol3:
        if pdf_data:
            st.download_button(
                label="📕 Download as .PDF",
                data=pdf_data,
                file_name=f"{file_prefix}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.button("📕 PDF Unavailable", disabled=True, use_container_width=True)

# Footer
st.markdown("""
<div class='footer-bar'>
    <strong>LegalEase</strong> &copy; 2026 &bull; AI-Powered Legal Document Automation System &bull; Fast, Secure & Standardized
</div>
""", unsafe_allow_html=True)
