from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import os
import uvicorn
import tempfile
import json
from resume_parser import extract_all_text, get_ai_resume_data
from pdf_generator import build_classic_pdf, build_monochrome_pdf, build_sidebar_pdf
from docx_generator import build_classic_docx, build_monochrome_docx, build_sidebar_docx

app = FastAPI(title="Resume Builder API")

# Allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Resume Builder API is running"}

@app.post("/api/extract")
async def extract_resume(
    files: List[UploadFile] = File(...),
    user_instruction: str = Form(None)
):
    try:
        temp_files = []
        for file in files:
            contents = await file.read()
            temp_files.append(contents)
        
        import io
        file_objs = [io.BytesIO(f) for f in temp_files]
        
        raw_text = extract_all_text(file_objs)
        data = get_ai_resume_data(raw_text, user_instruction)
        
        if "error" in data:
            raise HTTPException(status_code=500, detail=data["error"])
            
        return data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate/pdf")
async def generate_pdf(payload: Dict[str, Any]):
    try:
        data = payload.get("data", {})
        template_id = payload.get("template_id", "classic")
        
        if template_id == "classic":
            buffer = build_classic_pdf(data)
        elif template_id == "monochrome":
            buffer = build_monochrome_pdf(data)
        elif template_id == "sidebar":
            buffer = build_sidebar_pdf(data)
        else:
            buffer = build_classic_pdf(data)
            
        return Response(
            content=buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=resume_{template_id}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate/docx")
async def generate_docx(payload: Dict[str, Any]):
    try:
        data = payload.get("data", {})
        template_id = payload.get("template_id", "classic")
        
        if template_id == "classic":
            buffer = build_classic_docx(data)
        elif template_id == "monochrome":
            buffer = build_monochrome_docx(data)
        elif template_id == "sidebar":
            buffer = build_sidebar_docx(data)
        else:
            buffer = build_classic_docx(data)
            
        return Response(
            content=buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename=resume_{template_id}.docx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8001, reload=True)

