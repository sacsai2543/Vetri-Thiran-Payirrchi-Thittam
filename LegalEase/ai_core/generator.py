import io
import re
from pathlib import Path
from typing import Optional

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from fpdf import FPDF


def sanitize_text(text: str) -> str:
    """
    Sanitizes raw text to remove typographic anomalies, non-standard quotes,
    dashes, and special characters to ensure crisp formatting across PDF and DOCX.
    """
    if not text:
        return ""
    
    replacements = {
        "\u2018": "'",   # Left single quote
        "\u2019": "'",   # Right single quote
        "\u201c": '"',   # Left double quote
        "\u201d": '"',   # Right double quote
        "\u2014": " -- ", # Em dash
        "\u2013": " - ",  # En dash
        "\u2026": "...",  # Ellipsis
        "\u00a0": " ",    # Non-breaking space
        "\u2022": "*",    # Bullet symbol
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
    }
    for old_char, new_char in replacements.items():
        text = text.replace(old_char, new_char)
    
    return text.strip()


def sanitize_for_pdf(text: str) -> str:
    """
    Cleans text specifically for standard FPDF Latin-1 font compatibility.
    """
    text = sanitize_text(text)
    # Convert unrepresentable characters
    return text.encode("latin-1", "replace").decode("latin-1")


def set_cell_background(cell, fill_hex: str):
    """Sets background color of a Word table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def format_docx(text: str, doc_type: str = "Legal Agreement", logo_path: Optional[str] = None) -> bytes:
    """
    Generates a professionally styled Microsoft Word (.docx) document
    featuring custom branding logo, Times New Roman typography, clause tables,
    and formal legal signature footers.
    """
    clean_text = sanitize_text(text)
    doc = Document()

    # Configure 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Configure Header / Footer
        footer = section.footer
        footer_p = footer.paragraphs[0]
        footer_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = footer_p.add_run("LegalEase Inc. | contact@legalease.com | Confidential & Legally Binding")
        f_run.font.name = "Times New Roman"
        f_run.font.size = Pt(8.5)
        f_run.font.italic = True
        f_run.font.color.rgb = RGBColor(128, 128, 128)

    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(26, 32, 44)

    # 1. Embed Logo if available
    if logo_path and Path(logo_path).exists():
        try:
            logo_p = doc.add_paragraph()
            logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            logo_run = logo_p.add_run()
            logo_run.add_picture(str(logo_path), width=Inches(2.4))
            logo_p.paragraph_format.space_after = Pt(14)
        except Exception:
            pass

    # 2. Document Title
    title_text = doc_type.upper()
    # Check if text already has a title heading
    lines = clean_text.splitlines()
    first_non_empty = next((l.strip() for l in lines if l.strip()), "")
    if first_non_empty.startswith("#"):
        title_text = first_non_empty.lstrip("#").strip().upper()
        # Remove the first heading line from raw processing so it doesn't duplicate
        clean_text = "\n".join(lines[1:]).strip()

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run(title_text)
    title_run.font.name = "Times New Roman"
    title_run.font.size = Pt(16)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(17, 24, 39)
    title_p.paragraph_format.space_after = Pt(18)

    # 3. Process Content Paragraphs and Sections
    paragraphs = clean_text.split("\n\n")
    terms_list = []

    for para in paragraphs:
        para_clean = para.strip()
        if not para_clean:
            continue

        # Check for Major Section Headings (e.g., "1. Scope", "WITNESSETH:", "BETWEEN:")
        is_heading = False
        if re.match(r"^(\d+\.|\bWITNESSETH\b|\bWHEREAS\b|\bBETWEEN\b|\bAND\b|\bNOW, THEREFORE\b|\bIN WITNESS WHEREOF\b)", para_clean, re.IGNORECASE):
            is_heading = True

        if is_heading and len(para_clean.splitlines()) == 1 and len(para_clean) < 80:
            h_p = doc.add_paragraph()
            h_p.paragraph_format.space_before = Pt(12)
            h_p.paragraph_format.space_after = Pt(4)
            h_p.paragraph_format.keep_with_next = True
            run = h_p.add_run(para_clean)
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 23, 42)
            continue

        # Check if this paragraph contains signature underlines
        if "_____" in para_clean:
            sig_p = doc.add_paragraph()
            sig_p.paragraph_format.space_before = Pt(10)
            sig_p.paragraph_format.space_after = Pt(4)
            for line in para_clean.splitlines():
                l_run = sig_p.add_run(line + "\n")
                l_run.font.name = "Times New Roman"
                l_run.font.size = Pt(10.5)
                if "signature" in line.lower() or "printed name" in line.lower() or "title" in line.lower():
                    l_run.font.bold = True
            continue

        # Standard Paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        
        # Check for inline bolding or clauses
        sub_lines = para_clean.splitlines()
        for idx, s_line in enumerate(sub_lines):
            line_str = s_line.strip()
            if not line_str:
                continue
            
            # Heading prefix inside multiline (e.g. "1. Services: The provider...")
            match = re.match(r"^(\d+\.\s+[^:]+:)(.*)$", line_str)
            if match:
                bold_part, rest_part = match.group(1), match.group(2)
                b_run = p.add_run(bold_part)
                b_run.font.bold = True
                b_run.font.name = "Times New Roman"
                r_run = p.add_run(rest_part + ("\n" if idx < len(sub_lines) - 1 else ""))
                r_run.font.name = "Times New Roman"
            else:
                p_run = p.add_run(line_str + ("\n" if idx < len(sub_lines) - 1 else ""))
                p_run.font.name = "Times New Roman"

    # Save to buffer
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io.getvalue()


class LegalPDF(FPDF):
    """Custom FPDF class for LegalEase with Header, Footer, and Page Numbers."""
    def __init__(self, doc_type: str, logo_path: Optional[str] = None):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.doc_type = sanitize_for_pdf(doc_type)
        self.logo_path = logo_path
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(left=20, top=20, right=20)

    def header(self):
        # Header on later pages (Page 2+)
        if self.page_no() > 1:
            self.set_font("Times", "I", 8.5)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, f"LegalEase -- {self.doc_type}", align="L", ln=0)
            self.cell(0, 6, "CONFIDENTIAL", align="R", ln=1)
            self.line(20, self.get_y() + 1, 190, self.get_y() + 1)
            self.ln(6)

    def footer(self):
        self.set_y(-16)
        self.set_font("Times", "I", 8.5)
        self.set_text_color(130, 130, 130)
        # Decorative divider line
        self.set_draw_color(210, 215, 220)
        self.line(20, self.get_y(), 190, self.get_y())
        self.ln(2)
        self.cell(0, 5, "LegalEase Inc. | contact@legalease.com | All Rights Reserved.", align="L", ln=0)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="R", ln=0)


def format_pdf(text: str, doc_type: str = "Legal Agreement", logo_path: Optional[str] = None) -> bytes:
    """
    Generates a branded, publication-ready PDF document with crisp legal layout,
    header/footer, and clean typography.
    """
    clean_text = sanitize_for_pdf(text)
    pdf = LegalPDF(doc_type=doc_type, logo_path=logo_path)
    pdf.alias_nb_pages()
    pdf.add_page()

    # 1. Front page Logo
    if logo_path and Path(logo_path).exists():
        try:
            # Center logo (A4 width = 210mm, logo width = 60mm -> x = 75mm)
            pdf.image(str(logo_path), x=75, y=18, w=60)
            pdf.set_y(44)
        except Exception:
            pdf.ln(5)
    else:
        pdf.ln(5)

    # 2. Document Title
    lines = clean_text.splitlines()
    title_text = doc_type.upper()
    first_non_empty = next((l.strip() for l in lines if l.strip()), "")
    if first_non_empty.startswith("#"):
        title_text = first_non_empty.lstrip("#").strip().upper()
        clean_text = "\n".join(lines[1:]).strip()

    pdf.set_font("Times", "B", 15)
    pdf.set_text_color(20, 25, 35)
    pdf.cell(0, 8, title_text, align="C", ln=1)
    pdf.ln(4)

    # 3. Document Body
    paragraphs = clean_text.split("\n\n")
    for para in paragraphs:
        para_clean = para.strip()
        if not para_clean:
            continue

        # Check if this is a heading
        is_heading = False
        if re.match(r"^(\d+\.|\bWITNESSETH\b|\bWHEREAS\b|\bBETWEEN\b|\bAND\b|\bNOW, THEREFORE\b|\bIN WITNESS WHEREOF\b)", para_clean, re.IGNORECASE):
            is_heading = True

        if is_heading and len(para_clean.splitlines()) == 1 and len(para_clean) < 80:
            pdf.ln(3)
            pdf.set_font("Times", "B", 11.5)
            pdf.set_text_color(15, 23, 42)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(w=pdf.epw, h=6, text=para_clean, align="L")
            pdf.ln(1)
            continue

        # Signature blocks
        if "_____" in para_clean:
            pdf.ln(4)
            pdf.set_font("Times", "", 10)
            pdf.set_text_color(30, 30, 30)
            for s_line in para_clean.splitlines():
                pdf.set_x(pdf.l_margin)
                if "signature" in s_line.lower() or "printed name" in s_line.lower() or "title" in s_line.lower():
                    pdf.set_font("Times", "B", 10)
                else:
                    pdf.set_font("Times", "", 10)
                pdf.multi_cell(w=pdf.epw, h=5, text=s_line, align="L")
            pdf.ln(2)
            continue

        # Normal Paragraph
        pdf.set_font("Times", "", 10.5)
        pdf.set_text_color(40, 45, 55)
        
        sub_lines = para_clean.splitlines()
        for idx, s_line in enumerate(sub_lines):
            line_str = s_line.strip()
            if not line_str:
                continue
            
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(w=pdf.epw, h=5.5, text=line_str, align="L")

        pdf.ln(3)

    return bytes(pdf.output())


def format_html_preview(text: str) -> str:
    """
    Converts legal markdown / plain text into a stylized dark-themed HTML preview
    matching modern UI standards.
    """
    if not text:
        return "<p style='color: #94A3B8; text-align:center;'>No document content available to preview.</p>"

    clean_text = sanitize_text(text)
    html_lines = []

    for line in clean_text.splitlines():
        line_s = line.strip()
        if not line_s:
            html_lines.append("<div style='height: 10px;'></div>")
            continue

        # Header 1/2
        if line_s.startswith("## "):
            title = line_s.lstrip("#").strip()
            html_lines.append(f"<h3 style='color: #38BDF8; font-family: Inter, sans-serif; text-align: center; margin: 16px 0 10px 0; letter-spacing: 0.5px;'>{title}</h3><hr style='border: 0; border-top: 1px solid rgba(56, 189, 248, 0.3); margin-bottom: 16px;'/>")
            continue

        if line_s.startswith("# "):
            title = line_s.lstrip("#").strip()
            html_lines.append(f"<h2 style='color: #F8FAFC; font-family: Inter, sans-serif; text-align: center; margin: 18px 0 12px 0;'>{title}</h2>")
            continue

        # Major clauses / Preamble
        if line_s in ["WITNESSETH:", "BETWEEN:", "AND:", "NOW, THEREFORE:", "IN WITNESS WHEREOF:"]:
            html_lines.append(f"<p style='color: #F1F5F9; font-weight: 700; margin-top: 14px; margin-bottom: 4px; font-family: serif; letter-spacing: 0.5px;'>{line_s}</p>")
            continue

        # Numbered headings
        if re.match(r"^\d+\.\s+", line_s):
            html_lines.append(f"<p style='color: #E2E8F0; font-weight: 600; margin-top: 12px; margin-bottom: 4px;'><span style='color: #38BDF8;'>{line_s[:line_s.find('.')+1]}</span> {line_s[line_s.find('.')+1:]}</p>")
            continue

        # Signature lines
        if "_____" in line_s:
            html_lines.append(f"<div style='font-family: monospace; color: #94A3B8; margin: 4px 0;'>{line_s}</div>")
            continue

        # Standard lines
        html_lines.append(f"<p style='color: #CBD5E1; font-size: 14.5px; line-height: 1.65; margin-bottom: 6px; font-family: \"Merriweather\", Georgia, serif;'>{line_s}</p>")

    styled_body = "\n".join(html_lines)

    return f"""
    <div style='background: linear-gradient(145deg, #0F172A 0%, #1E293B 100%);
                border: 1px solid rgba(148, 163, 184, 0.18);
                border-radius: 12px;
                padding: 24px 28px;
                color: #E2E8F0;
                max-height: 480px;
                overflow-y: auto;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;'>
        {styled_body}
    </div>
    """
