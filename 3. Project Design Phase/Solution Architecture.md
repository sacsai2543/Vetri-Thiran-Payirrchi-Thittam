# Solution Architecture

| Field | Details |
|---|---|
| Team ID | SWTID-2026-8639 |
| Project Name | LegalEase AI: Your Smart Legal Document Assistant |
| Team Leader | Santhiya |

## Architecture Flow

```
[User] -> [Streamlit Frontend] -> [Python Backend]
                                     |-> [Text Extraction: pdfplumber / python-docx]
                                     |-> [Chunking + Embeddings -> FAISS Vector Store]
                                     |-> [Gemini API: summary, risk analysis, Q&A]
[Backend] -> [Summary, risk report, glossary, answers] -> [User]
```

## Components

| Component | Responsibility |
|---|---|
| Frontend | Upload, display of summary, risk report and chat |
| Backend | Coordinates extraction, retrieval and AI calls |
| Text Extraction | Converts documents into clean text |
| Vector Store | Retrieves the clauses most relevant to a question |
| Gemini API | Produces simplified text, risk explanations and answers |
| Disclaimer Layer | Adds a notice that output is guidance, not legal advice |
