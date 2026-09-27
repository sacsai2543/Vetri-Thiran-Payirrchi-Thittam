# LegalEase — Demo Video Presentation Script 🎬⚖️

**Total Video Duration:** ~3 Minutes 15 Seconds  
- **Codebase Walkthrough (File-by-File):** ~1 Minute 30 Seconds *(~10–15 Seconds per file)*  
- **Web Dashboard Walkthrough:** ~1 Minute 45 Seconds  

---

## ⏱️ Video Structure & Master Timeline

| Section | Timestamp | Duration | Focus Area |
| :--- | :--- | :--- | :--- |
| **PART 1: FILE-BY-FILE CODEBASE EXPLANATION** | | **~1m 30s** | **Individual Code Files (10–15s each)** |
| 1. `config.py` | `0:00 - 0:12` | 12s | Environment configuration, API keys, paths & asset provisioning |
| 2. `legalEaseAPI/main.py` | `0:12 - 0:25` | 13s | FastAPI entrypoint, CORS configuration & health check routes |
| 3. `legalEaseAPI/routes.py` | `0:25 - 0:38` | 13s | Pydantic `DocumentRequest` validation & `POST /generate` endpoint |
| 4. `ai_core/gemini_generator.py` | `0:38 - 0:52` | 14s | Gemini 1.5 AI prompt engineering, clause generation & fallback engine |
| 5. `ai_core/generator.py` | `0:52 - 1:07` | 15s | Multi-format rendering engine (.DOCX, .PDF, .HTML & sanitization) |
| 6. `frontend/app.py` | `1:07 - 1:20` | 13s | Streamlit application, session state management & dark UI styles |
| 7. `image/generate_logos.py` & `run.bat` | `1:20 - 1:32` | 12s | Dynamic logo generation & 1-click startup automation |
| **PART 2: WEB DASHBOARD WALKTHROUGH** | | **~1m 45s** | **Interactive UI & Live Workflow** |
| 8. Dashboard Overview & Dark Aesthetic | `1:32 - 1:47` | 15s | Glassmorphism UI, branding & responsive layout |
| 9. Template Presets & Dynamic Form Inputs | `1:47 - 2:07` | 20s | Preset selection (NDA, Employment, Lease, Freelance) & custom inputs |
| 10. AI Document Generation in Action | `2:07 - 2:27` | 20s | Backend AI generation, loading state & success notification |
| 11. Live HTML Preview & Inline Document Editor | `2:27 - 2:50` | 23s | Structured legal styling, recitals & real-time document editing |
| 12. Multi-Format Downloads (.TXT, .DOCX, .PDF) | `2:50 - 3:10` | 20s | Court-ready PDF, branded Word document & clean text exports |
| 13. Summary & Outro | `3:10 - 3:20` | 10s | Key takeaways & conclusion |

---

## 📜 Complete Shot-by-Shot Teleprompter Script

---

### 📁 PART 1: Code Files Explanation (~10–15s per file)

#### 1️⃣ `config.py` (0:00 – 0:12 | 12s)
* **Visual on Screen:**  
  Open [`config.py`](file:///c:/Users/acer/Desktop/LegalEase/config.py) in VS Code. Highlight lines 8–29 (loading `.env`, `GEMINI_API_KEY`, `DEFAULT_MODEL`, API ports, and directory paths).
* **Voiceover:**
  > *"Starting with `config.py` — this is our centralized configuration hub. It securely loads environment variables via `python-dotenv`, configures our Google Gemini model and API keys, sets the FastAPI host and port, and manages paths for logo assets and output directories."*

---

#### 2️⃣ `legalEaseAPI/main.py` (0:12 – 0:25 | 13s)
* **Visual on Screen:**  
  Open [`legalEaseAPI/main.py`](file:///c:/Users/acer/Desktop/LegalEase/legalEaseAPI/main.py). Highlight the FastAPI app instance, CORS middleware, and the `/` & `/health` endpoints.
* **Voiceover:**
  > *"Next is `legalEaseAPI/main.py`, the core entry point for our FastAPI backend. It initializes the API server, configures CORS middleware for cross-origin communication, includes our modular router, and provides root health check endpoints."*

---

#### 3️⃣ `legalEaseAPI/routes.py` (0:25 – 0:38 | 13s)
* **Visual on Screen:**  
  Open [`legalEaseAPI/routes.py`](file:///c:/Users/acer/Desktop/LegalEase/legalEaseAPI/routes.py). Highlight the `DocumentRequest` Pydantic class (lines 17–22) and the `POST /generate` endpoint (lines 24–43).
* **Voiceover:**
  > *"In `legalEaseAPI/routes.py`, we define our REST API endpoints. It uses Pydantic's `DocumentRequest` model to validate document type, involved parties, terms, and dates, then routes the payload into our AI generation core."*

---

#### 4️⃣ `ai_core/gemini_generator.py` (0:38 – 0:52 | 14s)
* **Visual on Screen:**  
  Open [`ai_core/gemini_generator.py`](file:///c:/Users/acer/Desktop/LegalEase/ai_core/gemini_generator.py). Highlight the `GeminiDocumentGenerator` class, prompt engineering template (lines 36–48), and fallback generation method.
* **Voiceover:**
  > *"Here in `ai_core/gemini_generator.py` is the AI logic. It interfaces with Google's Gemini 1.5 model, using structured legal prompt engineering to draft formal preambles, recitals, clauses, and signature blocks, with a built-in offline template fallback."*

---

#### 5️⃣ `ai_core/generator.py` (0:52 – 1:07 | 15s)
* **Visual on Screen:**  
  Open [`ai_core/generator.py`](file:///c:/Users/acer/Desktop/LegalEase/ai_core/generator.py). Highlight `format_docx()` with Word table styling and `format_pdf()` with FPDF header/footer classes.
* **Voiceover:**
  > *"The multi-format export engine is in `ai_core/generator.py`. It provides typographic sanitization, generates standardized Microsoft Word `.DOCX` files with embedded logos and table layouts, builds court-ready `.PDF`s with dynamic page numbers, and renders styled HTML previews."*

---

#### 6️⃣ `frontend/app.py` (1:07 – 1:20 | 13s)
* **Visual on Screen:**  
  Open [`frontend/app.py`](file:///c:/Users/acer/Desktop/LegalEase/frontend/app.py). Highlight custom CSS styles, `st.session_state` initializations, and the download button group.
* **Voiceover:**
  > *"The frontend lives in `frontend/app.py`. Built with Streamlit, it provides a custom glassmorphic dark theme, session state tracking for live document editing, preset template scenarios, and one-click download handlers."*

---

#### 7️⃣ `image/generate_logos.py` & `run.bat` (1:20 – 1:32 | 12s)
* **Visual on Screen:**  
  Briefly show [`image/generate_logos.py`](file:///c:/Users/acer/Desktop/LegalEase/image/generate_logos.py) and [`run.bat`](file:///c:/Users/acer/Desktop/LegalEase/run.bat).
* **Voiceover:**
  > *"Finally, `generate_logos.py` programmatically produces branded light and dark mode logos with Pillow, while `run.bat` launches both the FastAPI backend and Streamlit frontend in a single click."*

---

### 🌐 PART 2: Web Dashboard Walkthrough (~1 to 2 mins)

#### 8️⃣ Dashboard Overview & Theme (1:32 – 1:47 | 15s)
* **Visual on Screen:**  
  Switch window to the browser displaying LegalEase (`http://localhost:8501`). Scroll down smoothly showing the dark slate background, glowing scale logo, and header cards.
* **Voiceover:**
  > *"Now let’s explore the live LegalEase web dashboard. Designed with a sleek dark glassmorphism aesthetic, it offers an intuitive workspace for drafting, customizing, and exporting high-quality legal agreements."*

---

#### 9️⃣ Presets & Dynamic Form Inputs (1:47 – 2:07 | 20s)
* **Visual on Screen:**  
  Click on the **"📋 Quick Template Presets"** dropdown. Select **"Scenario 4: Freelance Work Contract"** (or **"Scenario 1: Employment Contract"**). Watch all form fields populate instantly:
  - *Document Type:* Freelance Work Contract
  - *Parties Involved:* Jane Doe & TechNova Inc.
  - *Terms & Conditions:* Semicolon-delimited conditions
  - *Effective Date:* April 15, 2025
* **Voiceover:**
  > *"Users can pick from pre-configured legal templates like Employment Contracts, NDAs, or Lease Agreements, or type custom requirements. The form accepts participating parties, effective dates, and specific terms separated by simple semicolons."*

---

#### 🔟 AI Generation in Action (2:07 – 2:27 | 20s)
* **Visual on Screen:**  
  Click the prominent **"⚡ Generate Document"** button. Show the spinner: *"Generating professional legal document with Gemini AI..."*, followed by the green alert banner: *"✅ Document Generated Successfully!"*.
* **Voiceover:**
  > *"Clicking 'Generate Document' triggers our backend AI pipeline. In seconds, Gemini AI analyzes the inputs and structures a complete, legally sound contract with standard recitals, numbered clauses, severability terms, and dual signature blocks."*

---

#### 1️⃣1️⃣ Live Preview & Inline Document Editor (2:27 – 2:50 | 23s)
* **Visual on Screen:**  
  Scroll through the styled HTML preview box showing clauses, recitals, and signature lines.  
  Click the **"🖊️ Click to Edit Document"** toggle button to reveal the text area. Change a term (e.g. adjust payment period from 7 days to 14 days) and show how the preview updates instantly.
* **Voiceover:**
  > *"The dashboard renders a formatted, court-ready preview directly in the browser. Need quick adjustments? Toggle the in-line editor to modify clauses or add custom terms with instant live preview updates."*

---

#### 1️⃣2️⃣ Multi-Format Downloads (2:50 – 3:10 | 20s)
* **Visual on Screen:**  
  Hover over the 3 download buttons:
  - Click **"📄 Download as .TXT"**
  - Click **"📝 Download as .DOCX"** *(open Word to show 1-inch margins, header logo, and Times New Roman layout)*
  - Click **"📕 Download as .PDF"** *(open PDF to show clean header logo, bold clauses, and dynamic footer page numbering)*
* **Voiceover:**
  > *"When finalized, export your contract in one click: download as plain text, formatted Microsoft Word with embedded branding and table layouts, or a court-ready PDF complete with headers, footers, and page numbers."*

---

#### 1️⃣3️⃣ Summary & Outro (3:10 – 3:20 | 10s)
* **Visual on Screen:**  
  Scroll back to the top of the dashboard showing the logo and completed workflow.
* **Voiceover:**
  > *"LegalEase automates contract drafting with AI precision, saving hours of legal overhead. Fast, secure, and standardized legal documents at your fingertips."*

---

## 💡 Presenter & Recording Tips

1. **Resolution:** Record at **1080p (1920x1080)** at 60 FPS.
2. **Warm-up:** Run [`run.bat`](file:///c:/Users/acer/Desktop/LegalEase/run.bat) before recording so the backend server and frontend Streamlit app are already running.
3. **Cursor Pacing:** Move the mouse smoothly to guide the viewer's eye during file switches and button clicks.
