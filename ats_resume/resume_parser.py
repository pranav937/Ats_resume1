import fitz  # PyMuPDF
from openai import OpenAI
import json
import re
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env"


def _get_openrouter_api_key() -> str:
  load_dotenv(dotenv_path=ENV_FILE, override=True)
  return os.environ.get("OPENROUTER_API_KEY", "").strip()



def get_ai_resume_data(user_instruction=None):
    """Generate professional resume data using AI based on user instructions."""
  api_key = _get_openrouter_api_key()
  if not api_key:
        return {"error": "Missing OPENROUTER_API_KEY environment variable."}

  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
  )
    prompt = f"""
You are an expert ATS Resume Builder.
Generate a complete, professional, and realistic resume in JSON format based on the user's instructions.
If the instructions are limited, invent reasonable and professional details for a strong tech/corporate resume.

USER INSTRUCTIONS:
{user_instruction if user_instruction else "Create a standard professional software engineer resume."}

RULES:
1. Return ONLY valid JSON.
2. CRITICAL: Provide realistic, plausible data for every section to make a complete resume.
3. For each certification, format it as a single string: "Certification Name — Year". 
4. Include at least 5-8 relevant professional skills.
5. Education must include College degree details.
6. Include EXACTLY 2 projects with 3-4 professional lines of description.
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
            return {"error": "Invalid OpenRouter API Key. Please update the API_KEY variable in resume_parser.py or set the OPENROUTER_API_KEY environment variable with a valid key."}
        return {"error": error_str}
