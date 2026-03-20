import fitz  # PyMuPDF
from openai import OpenAI
import json
import re
import os

API_KEY = os.environ.get("OPENROUTER_API_KEY", "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")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

def extract_all_text(files):
    """Combine text from multiple uploaded PDFs."""
    text = ""
    for file in files:
        stream = file.read()
        # stream is bytes — open directly with PyMuPDF
        doc = fitz.open(stream=stream, filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        # Reset pointer in case the file is reused
        if hasattr(file, "seek"):
            file.seek(0)
    return text

def get_ai_resume_data(user_instruction=None, parsed_text=""):
    """Generate professional resume data using AI based on user instructions and optional extracted text."""
    
    prompt = f"""
You are an expert ATS Resume Builder.
Generate a complete, professional, and realistic resume in JSON format based on the provided instructions and source text.
If instructions/text are limited, invent reasonable and professional details for a strong tech/corporate resume.

SOURCE DOCUMENT TEXT:
{parsed_text if parsed_text else "No source document provided."}

USER INSTRUCTIONS:
{user_instruction if user_instruction else "Create a standard professional software engineer resume. Extract applicable data from the source document perfectly."}

RULES:
1. Return ONLY valid JSON.
2. CRITICAL: Provide realistic, plausible data for every section to make a complete resume. Extract info accurately from the SOURCE DOCUMENT TEXT.
3. For each certification, format it as a single string: "Certification Name — Year". 
4. Include at least 5-8 relevant professional skills.
5. Education must include College degree details.
6. YOU MUST include these EXACT 2 projects as the first two items in the projects array:
   - Title: "AI Resume Builder Pro", Desc: "Developed an AI-powered resume builder that generates ATS-friendly resumes based on user input. Implemented document analysis and live preview features for better customization. Enhanced user experience with dynamic section editing."
   - Title: "ATS Resume Analyzer", Desc: "Built a system that evaluates resumes based on ATS standards and provides a score with improvement suggestions. Used keyword matching and formatting analysis to increase job selection chances. Enabled instant resume feedback after upload."
7. Experience should have 2-3 detailed and realistic professional roles.
8. Follow the USER INSTRUCTIONS strictly to flavor the output.

JSON FORMAT:
{{
"name": "",
"contact": "Email | Phone | Location",
"summary": "Professional summary optimized for ATS",
"skills": ["Skill 1", "Skill 2"],
"experience": [
  {{ "role": "", "company": "", "date": "", "desc": "" }}
],
"education": [
  {{ "inst": "", "degree": "", "cgpa": "", "year": "", "details": "" }}
],
"projects": [   
  {{ "title": "", "tech": [], "desc": "" }}
],
"certifications": [
  "Certification Name 1 - Year",
  "Certification Name 2 - Year",
  "Certification Name 3 - Year"
]
}}
"""

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-lite-001",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()
        content = re.sub(r"```json|```", "", content)
        start = content.find("{")
        end = content.rfind("}") + 1
        
        if start == -1 or end == -1: return {"error": "AI failed to return JSON structure."}
        
        json_text = content[start:end]
        json_text = re.sub(r',\s*}', '}', json_text)
        json_text = re.sub(r',\s*]', ']', json_text)
        
        return json.loads(json_text)
    except Exception as e:
        error_str = str(e)
        if "401" in error_str:
            return {"error": "Invalid OpenRouter API Key. Please update the API_KEY variable in ai_parser.py or set the OPENROUTER_API_KEY environment variable with a valid key."}
        return {"error": error_str}
