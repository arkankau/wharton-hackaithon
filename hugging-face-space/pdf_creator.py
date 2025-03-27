from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def create_pdf_with_cover(text, cover_image, filename="textbook.pdf"):
    """Creates a textbook PDF with a cover page."""
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Add cover image
    cover = ImageReader(cover_image)
    c.drawImage(cover, 50, 500, width=500, height=500)

    c.showPage()

    # Add text content
    text_lines = text.split("\n")
    y_position = 750
    for line in text_lines:
        c.drawString(100, y_position, line[:100])
        y_position -= 20
        if y_position < 50:
            c.showPage()
            y_position = 750
    
    c.save()
    return filename
