def get_html_preview(data, template_id):
    name = data.get("name", "Your Name")
    contact = data.get("contact", "email@example.com | 123-456-7890 | City, State")
    summary = data.get("summary", "")
    skills = ", ".join(data.get("skills", []))
    experience = data.get("experience", [])
    education = data.get("education", [])
    projects = data.get("projects", [])
    certifications = data.get("certifications", [])

    # Common HTML Helpers
    exp_html = ""
    for exp in experience:
        exp_html += f"""
        <div class="item">
            <div class="item-header">
                <strong>{exp.get('role')}</strong> | {exp.get('company')}
                <span class="date">{exp.get('date')}</span>
            </div>
            <div class="item-desc">{exp.get('desc')}</div>
        </div>
        """

    ed_html = ""
    for ed in education:
        ed_html += f"""
        <div class="item">
            <strong>{ed.get('inst')}</strong> - {ed.get('degree')} ({ed.get('year')})
            <div style="font-size:0.9em;color:#555;">{ed.get('details', '')}</div>
        </div>
        """

    proj_html = ""
    for proj in projects:
        proj_html += f"""
        <div class="item">
            <strong>{proj.get('title')}</strong>
            <div class="item-desc">{proj.get('desc')}</div>
        </div>
        """

    cert_html = "<ul>"
    for cert in certifications:
        cert_html += f"<li>{cert}</li>"
    cert_html += "</ul>"


    if template_id == "classic":
        return f"""
        <style>
            .resume-preview {{ font-family: 'Times New Roman', Times, serif; color: #000; line-height: 1.5; padding: 20px; text-align: left; background: white; border: 1px solid #ccc; max-width: 800px; margin: 0 auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            .resume-preview h1 {{ text-align: center; font-size: 24px; margin-bottom: 5px; }}
            .resume-preview .contact {{ text-align: center; font-size: 14px; margin-bottom: 20px; }}
            .resume-preview h2 {{ font-size: 16px; border-bottom: 1px solid #000; margin-top: 15px; margin-bottom: 10px; text-transform: uppercase; }}
            .resume-preview .item {{ margin-bottom: 15px; }}
            .resume-preview .item-header {{ display: flex; justify-content: space-between; }}
            .resume-preview .item-desc {{ margin-top: 5px; font-size: 14px; }}
            .resume-preview ul {{ margin: 0; padding-left: 20px; font-size: 14px; }}
            .resume-preview p {{ font-size: 14px; margin: 0; }}
        </style>
        <div class="resume-preview">
            <h1>{name}</h1>
            <div class="contact">{contact}</div>
            
            <h2>Summary</h2>
            <p>{summary}</p>
            
            <h2>Experience</h2>
            {exp_html}
            
            <h2>Skills</h2>
            <p>{skills}</p>
            
            <h2>Projects</h2>
            {proj_html}
            
            <h2>Education</h2>
            {ed_html}
            
            <h2>Certifications</h2>
            {cert_html}
        </div>
        """
        
    elif template_id == "monochrome":
        return f"""
        <style>
            .resume-preview {{ font-family: 'Arial', sans-serif; color: #333; line-height: 1.6; padding: 20px; text-align: left; background: white; border: 1px solid #ccc; max-width: 800px; margin: 0 auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            .resume-preview h1 {{ font-size: 28px; margin-bottom: 0px; color: #111; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; }}
            .resume-preview .contact {{ font-size: 13px; color: #666; margin-bottom: 25px; }}
            .resume-preview h2 {{ font-size: 15px; background: #f0f0f0; padding: 5px 10px; margin-top: 15px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; border-left: 4px solid #333; }}
            .resume-preview .item {{ margin-bottom: 15px; }}
            .resume-preview .item-header {{ display: flex; justify-content: space-between; align-items: baseline; }}
            .resume-preview .item-desc {{ margin-top: 5px; font-size: 13px; color: #444; }}
            .resume-preview ul {{ margin: 0; padding-left: 20px; font-size: 13px; }}
            .resume-preview p {{ font-size: 13px; margin: 0; }}
        </style>
        <div class="resume-preview">
            <h1>{name}</h1>
            <div class="contact">{contact}</div>
            
            <h2>Summary</h2>
            <p>{summary}</p>
            
            <h2>Experience</h2>
            {exp_html}
            
            <h2>Skills</h2>
            <p>{skills}</p>
            
            <h2>Projects</h2>
            {proj_html}
            
            <h2>Education</h2>
            {ed_html}
            
            <h2>Certifications</h2>
            {cert_html}
        </div>
        """

    elif template_id == "sidebar":
        # Left column items
        left_html = f"""
            <div class="contact-block">
                <h3>Contact</h3>
                <p>{contact.replace(" | ", "<br>")}</p>
            </div>
            <div class="skills-block">
                <h3>Skills</h3>
                <p>{skills}</p>
            </div>
            <div class="cert-block">
                <h3>Certifications</h3>
                {cert_html}
            </div>
        """
        
        # Right column items
        right_html = f"""
            <h2>Summary</h2>
            <p style="font-size: 13px;">{summary}</p>
            
            <h2>Experience</h2>
            {exp_html}
            
            <h2>Projects</h2>
            {proj_html}
            
            <h2>Education</h2>
            {ed_html}
        """

        return f"""
        <style>
            .resume-preview {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.5; background: white; border: 1px solid #ccc; max-width: 800px; margin: 0 auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: flex; min-height: 1000px; }}
            .left-col {{ width: 30%; background: #2c3e50; color: white; padding: 30px 20px; }}
            .right-col {{ width: 70%; padding: 30px; color: #333; }}
            
            .left-col h1 {{ font-size: 24px; margin-top: 0; border-bottom: 2px solid #34495e; padding-bottom: 10px; line-height: 1.2; word-break: break-word; }}
            .left-col h3 {{ font-size: 16px; margin-top: 25px; margin-bottom: 10px; border-bottom: 1px solid #34495e; padding-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }}
            .left-col p, .left-col ul {{ font-size: 12px; color: #ecf0f1; }}
            .left-col ul {{ padding-left: 15px; margin: 0; }}
            
            .right-col h2 {{ font-size: 18px; color: #2c3e50; border-bottom: 2px solid #ecf0f1; margin-top: 20px; margin-bottom: 15px; text-transform: uppercase; padding-bottom: 5px; }}
            .right-col h2:first-child {{ margin-top: 0; }}
            .right-col .item {{ margin-bottom: 20px; }}
            .right-col .item-header {{ display: flex; justify-content: space-between; align-items: baseline; }}
            .right-col .item-header strong {{ color: #2c3e50; font-size: 15px; }}
            .right-col .date {{ font-size: 12px; color: #7f8c8d; font-weight: bold; }}
            .right-col .item-desc {{ margin-top: 5px; font-size: 13px; color: #555; }}
        </style>
        <div class="resume-preview">
            <div class="left-col">
                <h1>{name}</h1>
                {left_html}
            </div>
            <div class="right-col">
                {right_html}
            </div>
        </div>
        """
