# ATS Resume Builder

## 📌 Project Overview

ATS Resume Builder is a web-based application that helps job seekers easily create professional and ATS-friendly resumes.

In this system, users can provide their information such as marksheets, certificates, skills, education, experience, and other personal details. The user can also write a prompt or command, based on which the system automatically generates a structured resume.

The generated resume is optimized for Applicant Tracking Systems (ATS) to increase the chances of being shortlisted for job applications.

---

## 🚀 Features

* 📄 Create a resume by entering personal details
* 🎓 Add marksheet and education details
* 📜 Add certificates and achievements
* 💡 Generate resume using prompts or commands
* 📝 ATS-friendly professional resume format
* ⬇️ Download the generated resume as a PDF
* ⚡ Fast and automated resume generation system

---

## 🛠️ Technologies Used

* Python
* FastAPI
* Streamlit
* ReportLab (PDF generation)
* AI Prompt Processing
* Regular Expressions (Regex)

---

## 📂 Project Structure

ats_resume_builder/
│
├── main.py
├── api.py
├── resume_generator.py
├── templates/
├── static/
├── requirements.txt
└── README.md

---

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/ats-resume-builder.git
```

2. Navigate to the project folder

```bash
cd ats-resume-builder
```

3. Install the required packages

```bash
pip install -r requirements.txt
```

4. Run the server

```bash
python -m uvicorn api:app --reload
```

---

## ▶️ Usage

1. Start the application.
2. Enter personal details, education, marksheets, and certificates.
3. Write a prompt or command.
4. The system will generate an ATS-friendly resume.
5. Download the resume as a PDF.

---

## 📈 Future Improvements

* Multiple resume templates
* AI skill suggestions
* LinkedIn profile import
* Direct job application integration

---

## 👨‍💻 Author

Pranav Pipaliya
