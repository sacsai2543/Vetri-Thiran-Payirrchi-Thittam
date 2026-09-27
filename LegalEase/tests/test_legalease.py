import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from legalEaseAPI.main import app
from ai_core.generator import format_docx, format_pdf, format_html_preview, sanitize_text
from ai_core.gemini_generator import GeminiDocumentGenerator
from config import DOC_LOGO_PATH

def run_all_tests():
    print("========================================")
    print("   Starting LegalEase E2E Test Suite    ")
    print("========================================")

    # 1. Test Text Sanitization
    raw_sample = "“Agreement” – ‘Term’ … \u2014 Special"
    cleaned = sanitize_text(raw_sample)
    assert '"' in cleaned, "Sanitization failed for double quotes"
    print("[PASS] 1. Text Sanitization works properly.")

    # 2. Test Document Generator Core
    gen = GeminiDocumentGenerator()
    doc_text = gen.generate_document(
        document_type="Freelance Work Contract",
        parties="Jane Doe (Service Provider), TechNova Inc. (Client)",
        terms="Work delivered by May 15, 2025; Payment in 7 days; IP belongs to Client; 15 days notice",
        dates="April 15, 2025"
    )
    assert len(doc_text) > 100, "Generated document is too short!"
    assert "Freelance Work Contract" in doc_text
    print(f"[PASS] 2. Legal Document Generator generated {len(doc_text)} characters.")

    # 3. Test DOCX Formatting
    docx_bytes = format_docx(
        text=doc_text,
        doc_type="Freelance Work Contract",
        logo_path=str(DOC_LOGO_PATH) if DOC_LOGO_PATH.exists() else None
    )
    assert len(docx_bytes) > 1000, "DOCX output is empty or corrupted!"
    # Save test docx
    test_docx_path = BASE_DIR / "docs" / "test_contract.docx"
    test_docx_path.write_bytes(docx_bytes)
    print(f"[PASS] 3. DOCX Formatter produced valid file ({len(docx_bytes)} bytes) at {test_docx_path.name}")

    # 4. Test PDF Formatting
    pdf_bytes = format_pdf(
        text=doc_text,
        doc_type="Freelance Work Contract",
        logo_path=str(DOC_LOGO_PATH) if DOC_LOGO_PATH.exists() else None
    )
    assert len(pdf_bytes) > 1000, "PDF output is empty or corrupted!"
    # Save test pdf
    test_pdf_path = BASE_DIR / "docs" / "test_contract.pdf"
    test_pdf_path.write_bytes(pdf_bytes)
    print(f"[PASS] 4. PDF Formatter produced valid file ({len(pdf_bytes)} bytes) at {test_pdf_path.name}")

    # 5. Test HTML Preview Formatting
    html_output = format_html_preview(doc_text)
    assert "<h3" in html_output or "<h2" in html_output
    assert "Freelance Work Contract" in html_output
    print("[PASS] 5. HTML Dark Preview formatted successfully.")

    # 6. Test FastAPI Root & Generate Endpoints
    client = TestClient(app)
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert "LegalEase" in res_root.json()["message"]
    print("[PASS] 6a. FastAPI root health check passed.")

    res_gen = client.post("/generate", json={
        "document_type": "Non-Disclosure Agreement (NDA)",
        "parties": "Company A, Company B",
        "terms": "Mutual confidentiality for 2 years; Jurisdiction in California",
        "dates": "May 1, 2025"
    })
    assert res_gen.status_code == 200
    res_data = res_gen.json()
    assert "document" in res_data
    assert len(res_data["document"]) > 100
    print("[PASS] 6b. FastAPI POST /generate endpoint passed.")

    print("========================================")
    print("   ALL TESTS PASSED WITH 100% SUCCESS!  ")
    print("========================================")

if __name__ == "__main__":
    run_all_tests()
