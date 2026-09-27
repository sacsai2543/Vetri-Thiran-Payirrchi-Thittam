import os
from typing import Optional
from config import GEMINI_API_KEY, DEFAULT_MODEL

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    genai = None
    HAS_GENAI = False


class GeminiDocumentGenerator:
    """
    Core AI Generator using Google Gemini API to produce professional,
    customized legal documents.
    """

    def __init__(self, model_name: Optional[str] = None):
        self.api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
        self.model_name = model_name or DEFAULT_MODEL
        self.model = None

        if HAS_GENAI and self.api_key and self.api_key.strip() != "your_gemini_api_key_here":
            try:
                genai.configure(api_key=self.api_key.strip())
                self.model = genai.GenerativeModel(self.model_name)
            except Exception as e:
                print(f"[Warning] Failed to configure Gemini model '{self.model_name}': {e}")
                self.model = None

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        """
        Generate a structured, formal legal document based on user inputs.
        """
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions: {terms}\n"
            "Ensure formal legal structure with multiple sections and legal clauses.\n"
            "Requirements:\n"
            "- Begin with the title in markdown format: '## [Document Title]'\n"
            "- Include an Opening Preamble and Recitals ('WITNESSETH:')\n"
            "- Numbered legal sections (e.g., 1. Definitions / Scope of Work, 2. Term and Termination, 3. Payment / Consideration, 4. Confidentiality, 5. Intellectual Property Rights, 6. Governing Law, 7. Entire Agreement, 8. Severability)\n"
            "- Explicitly incorporate all the user's specified terms & conditions clearly into dedicated clauses\n"
            "- Conclude with formal IN WITNESS WHEREOF clause and structured signature blocks for both parties, including signature lines, names, titles, and dates."
        )

        # Attempt generation with Google Gemini
        if self.model is not None:
            try:
                response = self.model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print(f"[Warning] Gemini generation error: {e}. Falling back to structured template engine.")

        # Fallback generator if API key is not configured or network error occurs
        return self._generate_fallback_document(document_type, parties, terms, dates)

    def _generate_fallback_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        """
        Provides a comprehensive, professionally styled fallback legal document
        when Gemini API is not configured or temporarily unreachable.
        """
        doc_title = document_type.strip() if document_type else "Legal Agreement"
        date_str = dates.strip() if dates else "the Effective Date"
        parties_str = parties.strip() if parties else "[Party A] and [Party B]"
        terms_list = [t.strip() for t in terms.split(";") if t.strip()] if terms else [
            "Parties agree to fulfill obligations in good faith",
            "Confidentiality must be maintained at all times",
            "Either party may terminate with 30 days written notice"
        ]

        # Parse parties
        party_parts = [p.strip() for p in parties_str.split(",") if p.strip()]
        if len(party_parts) >= 2:
            party_a = party_parts[0]
            party_b = ", ".join(party_parts[1:])
        else:
            party_a = party_parts[0] if party_parts else "Party A (Service Provider)"
            party_b = "Party B (Client)"

        terms_clauses = ""
        for i, term in enumerate(terms_list, start=1):
            terms_clauses += f"{i}. {term.capitalize()}\n   Each party expressly agrees and covenants to abide by the provisions set forth in this clause without deviation.\n\n"

        document = f"""## {doc_title}

Agreement made and entered into this {date_str}, by and between:

BETWEEN:
{party_a}, hereinafter referred to as the "First Party",

AND:
{party_b}, hereinafter referred to as the "Second Party".

WITNESSETH:
WHEREAS, the parties desire to enter into this {doc_title} to define their respective rights, duties, and covenants in connection with their commercial engagement; and
WHEREAS, both parties acknowledge and agree that the terms and conditions outlined herein reflect the full and mutual understanding of the parties;

NOW, THEREFORE, in consideration of the mutual covenants and promises contained herein, and other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the parties agree as follows:

1. Purpose and Scope of Agreement
The purpose of this {doc_title} is to formally govern the relationship, responsibilities, and deliverables between {party_a} and {party_b}.

2. Agreed Terms and Obligations
{terms_clauses}
3. Confidentiality
Each party agrees to preserve the confidentiality of all proprietary, financial, operational, and technical information disclosed during the term of this Agreement. Neither party shall disclose such information to any third party without prior written consent.

4. Term and Termination
This Agreement shall commence upon the Effective Date ({date_str}) and shall remain in full force and effect until terminated by mutual agreement, expiration of agreed obligations, or by either party giving thirty (30) days prior written notice.

5. Governing Law and Jurisdiction
This Agreement shall be construed, interpreted, and governed in accordance with the substantive laws of the applicable jurisdiction, without regard to conflict of law principles. Any dispute arising out of or in connection with this Agreement shall be resolved through good faith negotiation or competent courts of law.

6. Severability
If any provision of this Agreement is held to be invalid, illegal, or unenforceable by any court of competent jurisdiction, the remaining provisions shall continue in full force and effect.

7. Entire Agreement
This Agreement constitutes the entire understanding between the parties concerning the subject matter hereof and supersedes all prior negotiations, discussions, or agreements, whether written or oral.

IN WITNESS WHEREOF, the parties hereto have executed this {doc_title} as of the Effective Date written above.

_______________________________________
{party_a}
Authorized Signature: __________________
Printed Name: _________________________
Title: ________________________________
Date: {date_str}

_______________________________________
{party_b}
Authorized Signature: __________________
Printed Name: _________________________
Title: ________________________________
Date: {date_str}
"""
        return document.strip()
