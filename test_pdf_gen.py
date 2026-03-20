from xhtml2pdf import pisa
from io import BytesIO

def test_pdf():
    html = "<h1>Hello World</h1><p>Test PDF generation.</p>"
    result_file = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result_file)
    if not pisa_status.err:
        print("PDF generated successfully")
        with open("test_api_pdf.pdf", "wb") as f:
            f.write(result_file.getvalue())
    else:
        print("Error generating PDF")

if __name__ == "__main__":
    test_pdf()
