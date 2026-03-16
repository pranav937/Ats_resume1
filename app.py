import streamlit as st
import requests
import json
import streamlit.components.v1 as components
from html_generator import get_html_preview

# -----------------------------
# CONFIGURATION
# -----------------------------
st.set_page_config(page_title="AI Resume Builder Pro", layout="wide", page_icon="📄")

API_URL = "http://localhost:8001/api"

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    .btn-primary>button {
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    .btn-primary>button:hover { background-color: #45a049; }
    
    .template-card {
        padding: 20px;
        border-radius: 12px;
        background: white;
        border: 1px solid #e0e0e0;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .template-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #333;
    }
    .selected-card {
        border: 2px solid #2196f3;
        box-shadow: 0 4px 15px rgba(33,150,243,0.3);
    }
    .preview-container {
        border: 1px solid #ddd;
        border-radius: 8px;
        background: white;
        padding: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None

# -----------------------------
# UI COMPONENTS
# -----------------------------
st.title("🧙‍♂️ Professional AI Resume Builder Pro")
st.markdown("---")

col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    st.subheader("1. Setup & Upload")
    uploaded_files = st.file_uploader("Upload PDFs (Resume/Certificates)", type="pdf", accept_multiple_files=True)
    user_prompt = st.text_area("2. Tailor Instructions", placeholder="e.g. Focus on Python projects for a Senior role.", height=150)
    
    if st.button("🚀 Analyze Documents", type="primary"):
        if not uploaded_files:
            st.error("Please upload PDFs first.")
        else:
            with st.spinner("AI Analysis in progress via API..."):
                try:
                    files_to_send = [("files", (f.name, f.getvalue(), "application/pdf")) for f in uploaded_files]
                    data = {"user_instruction": user_prompt}
                    
                    response = requests.post(f"{API_URL}/extract", files=files_to_send, data=data)
                    
                    if response.status_code == 200:
                        st.session_state.resume_data = response.json()
                        st.session_state.selected_template = "classic" # Default selection
                        st.success("Analysis Complete!")
                    else:
                        st.error(f"API Error: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Failed to connect to API. Is the FastAPI server running on port 8001?")

    if st.session_state.resume_data:
        with st.expander("👀 View/Edit Extracted JSON Data"):
            edited_data = st.text_area("JSON Data", value=json.dumps(st.session_state.resume_data, indent=2), height=400)
            if st.button("Update Data"):
                try:
                    st.session_state.resume_data = json.loads(edited_data)
                    st.success("Data updated successfully!")
                except json.JSONDecodeError:
                    st.error("Invalid JSON format.")

with col_right:
    st.subheader("3. Choose Your Template")
    
    # 3 Templates Grid
    import os
    templates = [
        {"id": "classic", "name": "Classic Single Column", "desc": "Clean, traditional, and ATS-friendly.", "img": "templates/img1.jpg"},
        {"id": "monochrome", "name": "Professional Monochrome", "desc": "Modern borders, sharp fonts, high contrast.", "img": "templates/img2.jpg"},
        {"id": "sidebar", "name": "Two Column Sidebar", "desc": "Creative layout with a colored left sidebar.", "img": "templates/img3.jpg"}
    ]
    
    t_cols = st.columns(3)
    for i, t in enumerate(templates):
        with t_cols[i]:
            is_selected = st.session_state.selected_template == t["id"]
            card_class = "template-card selected-card" if is_selected else "template-card"
            
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            if 'img' in t and os.path.exists(t['img']):
                st.image(t['img'], use_container_width=True)
            else:
                st.info("No preview image")
            
            st.markdown(f"""
                <div class="template-title" style="margin-top: 15px;">{t["name"]}</div>
                <div style="font-size: 13px; color: #666; margin-bottom: 15px; height: 40px;">{t["desc"]}</div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button(f"Use {t['name']}", key=f"use_{t['id']}", use_container_width=True):
                if not st.session_state.resume_data:
                    st.warning("Please Analyze Documents first.")
                else:
                    st.session_state.selected_template = t["id"]
            
            if st.session_state.resume_data and is_selected:
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Download Buttons side by side
                dl_col1, dl_col2 = st.columns(2)
                with dl_col1:
                    try:
                        pdf_resp = requests.post(f"{API_URL}/generate/pdf", json={"data": st.session_state.resume_data, "template_id": t["id"]})
                        if pdf_resp.status_code == 200:
                            st.download_button("📥 PDF", data=pdf_resp.content, file_name=f"resume_{t['id']}.pdf", mime="application/pdf", use_container_width=True, key=f"pdf_{t['id']}")
                    except:
                        st.error("API offline")
                with dl_col2:
                    try:
                        docx_resp = requests.post(f"{API_URL}/generate/docx", json={"data": st.session_state.resume_data, "template_id": t["id"]})
                        if docx_resp.status_code == 200:
                            st.download_button("📥 DOCX", data=docx_resp.content, file_name=f"resume_{t['id']}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True, key=f"docx_{t['id']}")
                    except:
                        pass

    # Preview Area
    if st.session_state.resume_data and st.session_state.selected_template:
        st.markdown("### Live Preview")
        st.markdown(f"*Viewing Template: {st.session_state.selected_template.title()}*")
        
        # We render HTML here exactly how it would look
        html_content = get_html_preview(st.session_state.resume_data, st.session_state.selected_template)
        
        st.markdown('<div class="preview-container">', unsafe_allow_html=True)
        components.html(html_content, height=1000, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)