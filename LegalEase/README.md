# LegalEase: AI-Powered Legal Document Generator ⚖️

**LegalEase** is an end-to-end intelligent legal document generation platform built with **FastAPI**, **Google Gemini AI**, and **Streamlit**. It allows individuals, freelancers, startup founders, and businesses to generate customized, structured, and legally sound documents (employment contracts, NDAs, lease agreements, freelance contracts, etc.) with rich multi-format export capabilities (.TXT, .DOCX, .PDF).

---

## 🚀 Key Features

1. **AI-Powered Clause & Document Drafting**:
   - Integrated with Google Gemini 1.5 Pro / Flash models via Google Generative AI.
   - Generates formal legal structures with preambles, recitals (*WITNESSETH*), customized numbered clauses, severability, governing law, and dual-party signature blocks.

2. **Custom Branding & Output Formatting**:
   - **Microsoft Word (.DOCX)**: Standardized 1-inch margins, embedded header logos, Times New Roman typography, clause tables, and formal signature blocks.
   - **Adobe PDF (.PDF)**: Clean layout via FPDF with centered header logo, bold section headings, bulleted terms, and standardized footers with dynamic page numbering (*Page X of Y*).
   - **Plain Text (.TXT)**: Clean raw text export for quick drafting or pasting into other tools.

3. **Interactive Dark-Themed UI (Streamlit)**:
   - Modern glassmorphism dark aesthetic.
   - Pre-loaded template scenarios (Employment Contract, NDA, Residential Lease, Freelance Work Contract).
   - Interactive styled HTML document preview.
   - In-line live document editor with instant update.

4. **Modular FastAPI Backend**:
   - Modular structure (`legalEaseAPI/main.py`, `legalEaseAPI/routes.py`).
   - Pydantic schema validation (`DocumentRequest`).
   - RESTful endpoint `POST /generate` and health check `GET /`.

---

## 📁 Project Architecture

```
LEGALEASE/
├── ai_core/
│   ├── __init__.py
│   ├── gemini_generator.py      # Core Gemini 1.5 AI document generation logic
│   └── generator.py             # DOCX, PDF, and HTML formatting utilities
├── frontend/
│   └── app.py                   # Streamlit interactive UI & editor
├── image/
│   ├── Logo.png                 # Light-mode logo (Word & PDF export)
│   ├── inverseLogo.png          # Dark-mode logo (Streamlit UI)
│   └── generate_logos.py        # Branded logo generator script
├── legalEaseAPI/
│   ├── __init__.py
│   ├── main.py                  # FastAPI entry point & CORS configuration
│   └── routes.py                # REST API routes & Pydantic request models
├── config.py                    # Central configuration & path management
├── .env                         # API key & environment settings
├── .env.example                 # Sample configuration template
├── requirements.txt             # Python dependencies
├── run.bat                      # 1-Click Windows launcher
└── run.sh                       # 1-Click Linux/macOS launcher
```

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.10+
- Google Gemini API Key (get one free at [Google AI Studio](https://aistudio.google.com/))

### 1. Clone & Configure Environment
```bash
# Copy example configuration to .env
copy .env.example .env

# Edit .env and enter your Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application

#### Option A: 1-Click Launcher (Windows)
Double-click `run.bat` or run:
```cmd
run.bat
```

#### Option B: Manual Execution
**Terminal 1: Start FastAPI Backend Server**
```bash
uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2: Start Streamlit Frontend Application**
```bash
streamlit run frontend/app.py --server.port 8501
```

Open your browser at: **`http://localhost:8501`**

---

## 📡 API Reference

### `POST /generate`
Generates a structured legal document based on input parameters.

**Request Payload:**
```json
{
  "document_type": "Freelance Work Contract",
  "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
  "terms": "Work delivered by May 15, 2025; Payment within 7 days of invoice; Client owns IP; 15 days termination notice",
  "dates": "April 15, 2025"
}
```

**Response (200 OK):**
```json
{
  "document": "## Freelance Work Contract\n\nAgreement made and entered into this April 15, 2025...\n"
}
```

---

## ⚖️ Example Scenarios

- **Scenario 1 (Startup Founder):** Selects *Employment Contract*, specifies compensation, equity vesting, confidentiality, and downloads branded PDF.
- **Scenario 2 (Freelancer):** Generates *Non-Disclosure Agreement (NDA)* to protect proprietary source code and client discussions.
- **Scenario 3 (Landlord):** Generates *Residential Lease Agreement* with custom maintenance responsibilities and security deposit terms, exporting to .DOCX for client signing.
