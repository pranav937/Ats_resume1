import fitz  # PyMuPDF
import json
import re
import requests
from typing import Dict, Any, List
from io import BytesIO

try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False

DEFAULT_OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"


def _ocr_page_with_tesseract(page: fitz.Page) -> str:
    """Run OCR on a rendered PDF page image if Tesseract stack is available."""
    if not OCR_AVAILABLE:
        return ""
    try:
        # 2x scale improves OCR quality for low-resolution scans.
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        img = Image.open(BytesIO(pix.tobytes("png")))
        return pytesseract.image_to_string(img)
    except Exception:
        return ""

def extract_all_text(files):
    """Combine text from multiple uploaded PDFs with OCR fallback for scanned pages."""
    text = ""
    for file in files:
        stream = file.read()
        # stream is bytes — open directly with PyMuPDF
        doc = fitz.open(stream=stream, filetype="pdf")
        for page in doc:
            page_text = page.get_text("text") or ""

            # If direct extraction is too short, treat as scanned page and OCR it.
            if len(page_text.strip()) < 40:
                ocr_text = _ocr_page_with_tesseract(page)
                if ocr_text.strip():
                    page_text = f"{page_text}\n{ocr_text}"

            text += page_text + "\n"
        doc.close()
        # Reset pointer in case the file is reused
        if hasattr(file, "seek"):
            file.seek(0)
    return text

def _clean_lines(parsed_text: str) -> List[str]:
    lines = [line.strip() for line in parsed_text.splitlines()]
    return [line for line in lines if line]


def _find_email(text: str) -> str:
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return m.group(0) if m else ""


def _find_phone(text: str) -> str:
    m = re.search(r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{3,5}\)?[\s.-]?)?\d{3,5}[\s.-]?\d{3,5}", text)
    return m.group(0) if m else ""


def _extract_section(lines: List[str], header: str, stop_headers: List[str]) -> List[str]:
    section: List[str] = []
    in_section = False
    header_lower = header.lower()
    stop_set = {h.lower() for h in stop_headers}

    for line in lines:
        l = line.lower().strip(":")
        if l == header_lower:
            in_section = True
            continue
        if in_section and l in stop_set:
            break
        if in_section:
            section.append(line)
    return section


def parse_resume_rule_based(parsed_text: str, user_instruction: str = "") -> Dict[str, Any]:
    lines = _clean_lines(parsed_text)
    text_blob = "\n".join(lines)
    first_line = lines[0] if lines else "Your Name"

    email = _find_email(text_blob)
    phone = _find_phone(text_blob)
    contact_parts = [p for p in [email, phone] if p]
    contact = " | ".join(contact_parts) if contact_parts else "email@example.com | 9999999999"

    headers = ["summary", "experience", "skills", "projects", "education", "certifications"]
    summary_lines = _extract_section(lines, "summary", [h for h in headers if h != "summary"])
    skills_lines = _extract_section(lines, "skills", [h for h in headers if h != "skills"])
    exp_lines = _extract_section(lines, "experience", [h for h in headers if h != "experience"])
    proj_lines = _extract_section(lines, "projects", [h for h in headers if h != "projects"])
    edu_lines = _extract_section(lines, "education", [h for h in headers if h != "education"])
    cert_lines = _extract_section(lines, "certifications", [h for h in headers if h != "certifications"])

    skills_raw = ", ".join(skills_lines) if skills_lines else ""
    skills = [s.strip(" -•\t") for s in re.split(r",|\||/", skills_raw) if s.strip(" -•\t")]
    if not skills:
        skills = ["Python", "SQL", "Excel", "Communication"]

    projects = []
    for line in proj_lines:
        clean = line.strip("•- ")
        if clean:
            projects.append({"title": clean[:80], "desc": "Project details extracted from resume."})
    if not projects:
        projects = [{"title": "Resume Project", "desc": "Project details were not clearly structured in source file."}]

    experience = []
    if exp_lines:
        chunk = " ".join(exp_lines[:3])
        experience.append({"role": "Professional Experience", "company": "", "date": "", "desc": chunk[:400]})
    else:
        experience.append({"role": "Fresher / Entry Level", "company": "", "date": "", "desc": "Experience section not clearly available in source."})

    education = []
    if edu_lines:
        education.append({"inst": edu_lines[0][:120], "degree": "", "cgpa": "", "year": "", "details": " ".join(edu_lines[1:])[:240]})
    else:
        edu_keywords = ("school", "college", "university", "board", "b.tech", "bachelor", "master", "cgpa", "percentage", "%")
        inferred_edu = [line for line in lines if any(k in line.lower() for k in edu_keywords)]
        if inferred_edu:
            education.append({
                "inst": inferred_edu[0][:120],
                "degree": "",
                "cgpa": "",
                "year": "",
                "details": " ".join(inferred_edu[1:])[:240],
            })
        else:
            education.append({"inst": "Education details not found", "degree": "", "cgpa": "", "year": "", "details": ""})

    certifications = [line.strip("•- ") for line in cert_lines if line.strip("•- ")]
    if not certifications:
        cert_keywords = ("cert", "certificate", "training", "course", "workshop")
        inferred_certs = []
        for line in lines:
            if any(k in line.lower() for k in cert_keywords):
                inferred_certs.append(line.strip("•- "))
        certifications = inferred_certs

    summary = " ".join(summary_lines).strip()
    if not summary:
        summary = "Profile summary extracted using local parser."
    if user_instruction:
        summary = f"{summary} {user_instruction}".strip()

    return {
        "name": first_line,
        "contact": contact,
        "summary": summary,
        "skills": skills[:12],
        "experience": experience,
        "education": education,
        "projects": projects[:5],
        "certifications": certifications[:10],
    }


def parse_resume_with_ollama(parsed_text: str, user_instruction: str = "", model: str = DEFAULT_OLLAMA_MODEL) -> Dict[str, Any]:
    prompt = f"""
Extract resume data into valid JSON only.

SOURCE TEXT:
{parsed_text}

USER INSTRUCTION:
{user_instruction}

JSON FORMAT:
{{
"name": "",
"contact": "Email | Phone | Location",
"summary": "",
"skills": [""],
"experience": [{{"role": "", "company": "", "date": "", "desc": ""}}],
"education": [{{"inst": "", "degree": "", "cgpa": "", "year": "", "details": ""}}],
"projects": [{{"title": "", "desc": ""}}],
"certifications": [""]
}}
"""

    try:
        resp = requests.post(
            DEFAULT_OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=180,
        )
        if resp.status_code != 200:
            return {"error": f"Ollama request failed: {resp.text}", "status_code": 500}

        content = resp.json().get("response", "")
        content = re.sub(r"```json|```", "", content)
        start = content.find("{")
        end = content.rfind("}") + 1
        if start == -1 or end == 0:
            return {"error": "Ollama did not return valid JSON.", "status_code": 500}

        data = json.loads(content[start:end])
        return data
    except requests.exceptions.ConnectionError:
        return {"error": "Ollama is not running on localhost:11434. Start Ollama first.", "status_code": 503}
    except Exception as e:
        return {"error": str(e), "status_code": 500}


def get_ai_resume_data(user_instruction=None, parsed_text="", parse_mode: str = "rule_based"):
    """Backward-compatible extraction API: local rule-based or local Ollama parser."""
    if parse_mode == "ollama":
        ollama_result = parse_resume_with_ollama(parsed_text, user_instruction or "")
        if "error" not in ollama_result:
            return ollama_result
    return parse_resume_rule_based(parsed_text, user_instruction or "")
