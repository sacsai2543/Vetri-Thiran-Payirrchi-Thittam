# Project Development

| Field | Details |
|---|---|
| Team ID | SWTID-2026-8639 |
| Project Name | LegalEase AI: Your Smart Legal Document Assistant |
| Team Leader | Santhiya |

## Modules Developed

| Module | Description | Technology | Developed By |
|---|---|---|---|
| Upload and Extraction | Accepts PDF, DOCX or text and extracts clean text | pdfplumber, python-docx | Safiya Begum I |
| Retrieval | Splits text into chunks and finds relevant clauses | Embeddings, FAISS | Suvedha |
| Risk Detection | Flags risky clauses and explains why | Gemini API | Suvedha |
| Summary and Glossary | Creates plain-language summary and term explanations | Gemini API | Akshaya E |
| Frontend and Chat | Screens for upload, results and questions | Streamlit | Deepak D |
| Integration | Connects all modules into one application | Python | Santhiya |

## Project Files

| File | Purpose |
|---|---|
| app.py | Main Streamlit application |
| requirements.txt | List of Python libraries used |
| data/sample_rental_agreement.txt | Sample document used for testing and demo |
