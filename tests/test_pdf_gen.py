from xhtml2pdf import pisa
from io import BytesIO
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT_DIR / "outputs" / "samples" / "test_api_pdf.pdf"

def test_pdf():
    html = "<h1>Hello World</h1><p>Test PDF generation.</p>"
    result_file = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result_file)
    if not pisa_status.err:
        print("PDF generated successfully")
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_FILE, "wb") as f:
            f.write(result_file.getvalue())
    else:
        print("Error generating PDF")

if __name__ == "__main__":
    test_pdf()
