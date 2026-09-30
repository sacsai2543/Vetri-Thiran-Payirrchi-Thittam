# Data Flow Diagram & User Stories

| Field | Details |
|---|---|
| Team ID | SWTID-2026-8639 |
| Project Name | LegalEase AI: Your Smart Legal Document Assistant |
| Team Leader | Santhiya |

## Data Flow (Level 0)

```
User -> Uploads legal document (PDF / DOCX / text)
     -> Text extraction and cleaning
     -> Splitting into chunks and creating embeddings
     -> Vector store (retrieval of relevant clauses)
     -> LLM: summary, risk flags, glossary and answers
     -> Results displayed to User
```

## User Stories

| User Type | Story No. | User Story | Acceptance Criteria | Priority |
|---|---|---|---|---|
| Customer | USN-1 | As a user, I can upload a legal document | File is accepted and text is extracted | High |
| Customer | USN-2 | As a user, I want a simple summary of the document | Summary in plain language is displayed | High |
| Customer | USN-3 | As a user, I want risky clauses highlighted | Risky clauses shown with a reason | High |
| Customer | USN-4 | As a user, I want to ask questions about my document | Relevant answer based on the document | High |
| Customer | USN-5 | As a user, I want legal terms explained | Glossary of terms is displayed | Medium |
| Customer | USN-6 | As a user, I want to know this is not legal advice | Disclaimer visible on results | Medium |
