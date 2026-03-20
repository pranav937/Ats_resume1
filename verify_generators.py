import os
import json
from pdf_generator import build_classic_pdf, build_monochrome_pdf, build_sidebar_pdf
from docx_generator import build_classic_docx, build_monochrome_docx, build_sidebar_docx

sample_data = {
    "name": "John Doe",
    "contact": "john.doe@example.com | 123-456-7890 | New York, NY",
    "summary": "Experienced Software Engineer with a passion for building AI-powered applications.",
    "skills": ["Python", "JavaScript", "React", "FastAPI", "Docker"],
    "experience": [
        {
            "role": "Senior Software Engineer",
            "company": "Tech Corp",
            "date": "Jan 2020 - Present",
            "desc": "Leading the development of a scalable resume parsing system using Gemini AI."
        },
        {
            "role": "Software Engineer",
            "company": "Startup Inc",
            "date": "Jun 2017 - Dec 2019",
            "desc": "Developed several client-facing web applications using React and Node.js."
        }
    ],
    "education": [
        {
            "inst": "University of Technology",
            "degree": "B.S. in Computer Science",
            "year": "2017",
            "details": "Major in Artificial Intelligence."
        }
    ],
    "projects": [
        {
            "title": "AI Resume Builder Pro",
            "desc": "Developed an AI-powered resume builder that generates ATS-friendly resumes."
        }
    ],
    "certifications": [
        "AWS Certified Solutions Architect - 2021",
        "Google Cloud Professional Data Engineer - 2022"
    ],
    "languages": ["English (Native)", "Spanish (Fluent)"]
}

def test_pdf_generators():
    print("Testing PDF Generators...")
    builders = [
        ("classic", build_classic_pdf),
        ("monochrome", build_monochrome_pdf),
        ("sidebar", build_sidebar_pdf)
    ]
    for name, builder in builders:
        try:
            buffer = builder(sample_data)
            with open(f"test_{name}.pdf", "wb") as f:
                f.write(buffer.getvalue())
            print(f"  [OK] {name} PDF generated.")
        except Exception as e:
            print(f"  [FAIL] {name} PDF: {str(e)}")

def test_docx_generators():
    print("Testing DOCX Generators...")
    builders = [
        ("classic", build_classic_docx),
        ("monochrome", build_monochrome_docx),
        ("sidebar", build_sidebar_docx)
    ]
    for name, builder in builders:
        try:
            buffer = builder(sample_data)
            with open(f"test_{name}.docx", "wb") as f:
                f.write(buffer.getvalue())
            print(f"  [OK] {name} DOCX generated.")
        except Exception as e:
            print(f"  [FAIL] {name} DOCX: {str(e)}")

if __name__ == "__main__":
    test_pdf_generators()
    test_docx_generators()
    print("Verification complete. Check test_*.pdf and test_*.docx files.")
