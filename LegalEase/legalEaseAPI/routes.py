import sys
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
gemini_generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str = Field(..., description="Type of legal document (e.g., Employment Contract, NDA)")
    parties: str = Field(..., description="Parties involved in the agreement")
    terms: str = Field(..., description="Key terms & conditions separated by semicolons")
    dates: str = Field(..., description="Effective date of the document")


@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    """
    Endpoint to process user request and generate structured legal documents
    using Gemini AI Core.
    """
    try:
        if not request.document_type.strip():
            raise HTTPException(status_code=400, detail="Document type cannot be empty.")
        
        response = gemini_generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates
        )
        return {"document": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document generation failed: {str(e)}")
