from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from io import BytesIO

def build_classic_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    # Times New Roman like built-in fonts
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontName='Times-Roman', fontSize=24, alignment=TA_CENTER, spaceAfter=5)
    contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, alignment=TA_CENTER, spaceAfter=20)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontName='Times-Bold', fontSize=14, spaceBefore=15, spaceAfter=5, textTransform='uppercase')
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=14)
    item_title_style = ParagraphStyle('ItemTitle', parent=styles['Normal'], fontName='Times-Bold', fontSize=10, leading=14)
    
    elements = []
    
    elements.append(Paragraph(data.get('name', 'Your Name'), title_style))
    elements.append(Paragraph(data.get('contact', ''), contact_style))
    
    sections = [
        ("Summary", data.get('summary', '')),
        ("Experience", data.get('experience', [])),
        ("Skills", ", ".join(data.get('skills', []))),
        ("Projects", data.get('projects', [])),
        ("Education", data.get('education', [])),
        ("Certifications", data.get('certifications', []))
    ]
    
    for title, content in sections:
        if content:
            elements.append(Paragraph(title.upper(), heading_style))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=1, spaceAfter=10))
            
            if isinstance(content, str):
                elements.append(Paragraph(content, body_style))
            elif title == "Certifications":
                for c in content: elements.append(Paragraph(f"• {c}", body_style))
            else:
                for item in content:
                    if title == "Experience":
                        elements.append(Paragraph(f"<b>{item.get('role')}</b> | {item.get('company')} <font color='gray'>({item.get('date')})</font>", item_title_style))
                        elements.append(Paragraph(item.get('desc', ''), body_style))
                    elif title == "Projects":
                        elements.append(Paragraph(f"<b>{item.get('title')}</b>", item_title_style))
                        elements.append(Paragraph(item.get('desc', ''), body_style))
                    elif title == "Education":
                        elements.append(Paragraph(f"<b>{item.get('inst')}</b> - {item.get('degree')} ({item.get('year')})", item_title_style))
                        if item.get('details'):
                            elements.append(Paragraph(item.get('details'), body_style))
                    elements.append(Spacer(1, 8))

    doc.build(elements)
    buffer.seek(0)
    return buffer

def build_monochrome_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    # Arial/Helvetica like built-in fonts
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, alignment=TA_LEFT, spaceAfter=2, textTransform='uppercase', textColor=colors.HexColor('#111111'))
    contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontName='Helvetica', fontSize=9, alignment=TA_LEFT, spaceAfter=25, textColor=colors.HexColor('#666666'))
    
    # Custom heading with background doesn't work well natively in simple ParagraphStyle without custom flows,
    # but we can simulate the thick left border and background via formatting or just keep it simple bold
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, spaceBefore=15, spaceAfter=10, textTransform='uppercase', textColor=colors.black, backColor=colors.HexColor('#f0f0f0'), borderPadding=(4,4,4,10), leftIndent=0)
    
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=colors.HexColor('#333333'))
    item_title_style = ParagraphStyle('ItemTitle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14)
    desc_style = ParagraphStyle('Desc', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#444444'))
    
    elements = []
    
    elements.append(Paragraph(data.get('name', 'Your Name').upper(), title_style))
    elements.append(Paragraph(data.get('contact', ''), contact_style))
    
    sections = [
        ("Summary", data.get('summary', '')),
        ("Experience", data.get('experience', [])),
        ("Skills", ", ".join(data.get('skills', []))),
        ("Projects", data.get('projects', [])),
        ("Education", data.get('education', [])),
        ("Certifications", data.get('certifications', []))
    ]
    
    for title, content in sections:
        if content:
            elements.append(Paragraph(title.upper(), heading_style))
            
            if isinstance(content, str):
                elements.append(Paragraph(content, body_style))
            elif title == "Certifications":
                for c in content: elements.append(Paragraph(f"• {c}", desc_style))
            else:
                for item in content:
                    if title == "Experience":
                        # We use a table to align role/company left and date right
                        data_row = [[Paragraph(f"<b>{item.get('role')}</b> | {item.get('company')}", item_title_style), 
                                     Paragraph(f"<font color='#666'>{item.get('date')}</font>", ParagraphStyle('R', parent=item_title_style, alignment=TA_RIGHT))]]
                        from reportlab.platypus import Table, TableStyle
                        t = Table(data_row, colWidths=[doc.width*0.7, doc.width*0.3])
                        t.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 2), ('TOPPADDING', (0,0), (-1,-1), 0)]))
                        elements.append(t)
                        elements.append(Paragraph(item.get('desc', ''), desc_style))
                    elif title == "Projects":
                        elements.append(Paragraph(f"<b>{item.get('title')}</b>", item_title_style))
                        elements.append(Paragraph(item.get('desc', ''), desc_style))
                    elif title == "Education":
                        elements.append(Paragraph(f"<b>{item.get('inst')}</b> - {item.get('degree')} ({item.get('year')})", item_title_style))
                        if item.get('details'):
                            elements.append(Paragraph(item.get('details'), desc_style))
                    elements.append(Spacer(1, 10))

    doc.build(elements)
    buffer.seek(0)
    return buffer

def draw_sidebar_bgIndicators(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor('#2c3e50'))
    # Draw left sidebar background
    canvas.rect(0, 0, A4[0]*0.35, A4[1], fill=True, stroke=False)
    canvas.restoreState()

def build_sidebar_pdf(data):
    buffer = BytesIO()
    doc = BaseDocTemplate(buffer, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    
    # 35% left, 65% right
    frame_left = Frame(0, 0, A4[0]*0.35, A4[1], leftPadding=20, rightPadding=20, topPadding=30, bottomPadding=30, id='left')
    frame_right = Frame(A4[0]*0.35, 0, A4[0]*0.65, A4[1], leftPadding=30, rightPadding=30, topPadding=30, bottomPadding=30, id='right')
    
    template = PageTemplate(id='TwoCol', frames=[frame_left, frame_right], onPage=draw_sidebar_bgIndicators)
    doc.addPageTemplates([template])
    
    styles = getSampleStyleSheet()
    
    # Left styles (White text)
    left_title = ParagraphStyle('LTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=20, textColor=colors.white, spaceAfter=20, leading=22)
    left_h3 = ParagraphStyle('LH3', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=12, textColor=colors.white, spaceBefore=15, spaceAfter=8, textTransform='uppercase')
    left_body = ParagraphStyle('LBody', parent=styles['Normal'], fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#ecf0f1'), leading=13)
    
    # Right styles (Dark text)
    right_h2 = ParagraphStyle('RH2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#2c3e50'), spaceBefore=15, spaceAfter=10, textTransform='uppercase')
    right_body = ParagraphStyle('RBody', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, textColor=colors.HexColor('#555555'), leading=14)
    right_item_title = ParagraphStyle('RItemTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#2c3e50'))
    right_date = ParagraphStyle('RDate', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#7f8c8d'), alignment=TA_RIGHT)

    elements = []
    
    # --- LEFT COLUMN ---
    elements.append(Paragraph(data.get('name', 'Your Name'), left_title))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#34495e'), spaceBefore=0, spaceAfter=15))
    
    elements.append(Paragraph("CONTACT", left_h3))
    # Replace separators with breaklines for left column fit
    contact_parts = data.get('contact', '').split('|')
    for part in contact_parts:
        elements.append(Paragraph(part.strip(), left_body))
        
    elements.append(Paragraph("SKILLS", left_h3))
    elements.append(Paragraph(", ".join(data.get('skills', [])), left_body))
    
    if data.get('certifications'):
        elements.append(Paragraph("CERTIFICATIONS", left_h3))
        for c in data.get('certifications', []):
            elements.append(Paragraph(f"• {c}", left_body))
            
    # Force frame break to move to right column
    from reportlab.platypus import FrameBreak
    elements.append(FrameBreak())
    
    # --- RIGHT COLUMN ---
    if data.get('summary'):
        elements.append(Paragraph("SUMMARY", right_h2))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#ecf0f1'), spaceBefore=0, spaceAfter=10))
        elements.append(Paragraph(data.get('summary', ''), right_body))
        elements.append(Spacer(1, 10))
        
    if data.get('experience'):
        elements.append(Paragraph("EXPERIENCE", right_h2))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#ecf0f1'), spaceBefore=0, spaceAfter=10))
        for item in data.get('experience', []):
            from reportlab.platypus import Table, TableStyle
            data_row = [[Paragraph(f"{item.get('role')} | {item.get('company')}", right_item_title), 
                         Paragraph(item.get('date', ''), right_date)]]
            t = Table(data_row, colWidths=[frame_right._width*0.7, frame_right._width*0.3])
            t.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 2), ('TOPPADDING', (0,0), (-1,-1), 0), ('VALIGN',(0,0),(-1,-1),'BOTTOM')]))
            elements.append(t)
            elements.append(Paragraph(item.get('desc', ''), right_body))
            elements.append(Spacer(1, 12))
            
    if data.get('projects'):
        elements.append(Paragraph("PROJECTS", right_h2))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#ecf0f1'), spaceBefore=0, spaceAfter=10))
        for item in data.get('projects', []):
            elements.append(Paragraph(item.get('title', ''), right_item_title))
            elements.append(Paragraph(item.get('desc', ''), right_body))
            elements.append(Spacer(1, 12))
            
    if data.get('education'):
        elements.append(Paragraph("EDUCATION", right_h2))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#ecf0f1'), spaceBefore=0, spaceAfter=10))
        for item in data.get('education', []):
            elements.append(Paragraph(f"{item.get('inst')} - {item.get('degree')} ({item.get('year')})", right_item_title))
            if item.get('details'):
                 elements.append(Paragraph(item.get('details'), right_body))
            elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer
