import gradio as gr
import openai
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

OPEN_SOURCES = [
    "https://oercommons.org/",
    "http://www.digitalbookindex.org/_SEARCH/search011t-rev.asp",
    "https://cain.math.gatech.edu/textbooks/onlinebooks.html",
    "https://www.pdfdrive.com/",
    "https://openstax.org/subjects",
    "https://www.gutenberg.org/",
    "https://open.umn.edu/opentextbooks",
    "https://archive.org/search?query=precalculus"
]

def query_openai_for_textbook(subject, grade, topic, curriculum):
    prompt = f"""
    You are an expert educational content creator. Using only content that is publicly available in the following open-source textbook websites:

    {chr(10).join(OPEN_SOURCES)}

    Create a comprehensive AI-generated textbook for the subject '{subject}' at grade level '{grade}', focused on the topic '{topic}' based on the '{curriculum}' curriculum.

    The textbook should be structured as follows:
    1. Title Page
    2. Material Explanations (targeted for the grade audience)
    3. Practice Problems with Solutions (5+ problems)
    4. References (only from the listed open-source sources)

    Provide the content in structured, professional format. Use headings, numbered lists, and bullet points where appropriate.
    """

    response = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")).chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def create_pdf(text, subject):
    filename = f"{subject}_Textbook_{int(time.time())}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    margin = 50

    # Cover Page
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2, height - 150, f"{subject.title()}")
    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 180, f"Grade Level: {grade}")
    c.drawCentredString(width / 2, height - 200, "Powered by alexandria.ai")
    c.showPage()  # End cover page

    # Begin content pages
    y = height - margin
    c.setFont("Helvetica", 12)

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            y -= 10
            continue

        if line.startswith("#") or line.endswith(":"):
            c.setFont("Helvetica-Bold", 16)
            y -= 30
            c.drawCentredString(width / 2, y, line.strip("# "))
            y -= 20
            c.setFont("Helvetica", 12)
            continue

        words = line.split(' ')
        current_line = ""
        for word in words:
            if c.stringWidth(current_line + word + ' ') > (width - 2 * margin):
                c.drawString(margin, y, current_line)
                y -= 16
                if y < margin:
                    c.showPage()
                    y = height - margin
                    c.setFont("Helvetica", 12)
                current_line = word + ' '
            else:
                current_line += word + ' '

        if current_line.strip():
            c.drawString(margin, y, current_line.strip())
            y -= 16

        if y < margin:
            c.showPage()
            y = height - margin
            c.setFont("Helvetica", 12)

    c.save()
    return filename

def generate_textbook(subject, grade, topic, curriculum):
    try:
        content = query_openai_for_textbook(subject, grade, topic, curriculum)
        pdf_path = create_pdf(content, subject)
        return f"Textbook created successfully!", pdf_path
    except Exception as e:
        return f"Error: {str(e)}", None


custom_css = """
body, .gradio-container {
    background-color: #071e57 !important;
    color: white !important;
    font-family: 'Futura', sans-serif !important;
}
input, textarea, select {
    background-color: #262626 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 12px !important;
    font-size: 16px !important;
}
button {
    background-color: #c9900b !important;
    color: white !important;
    border-radius: 6px !important;
    padding: 12px 24px !important;
    border: none !important;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease-in-out;
}
button:hover {
    background-color: #f0cd55 !important;
    color: black !important;
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("Generate Your AI-Powered Textbook PDF")
    subject = gr.Textbox(label="Subject", placeholder="e.g., Calculus", elem_classes="form-input")
    grade = gr.Textbox(label="Grade Level", placeholder="e.g., 11, University, etc.", elem_classes="form-input")
    topic = gr.Textbox(label="Topic", placeholder="e.g., Derivatives", elem_classes="form-input")
    curriculum = gr.Textbox(label="Curriculum", placeholder="e.g., AP, IB, Cambridge", elem_classes="form-input")
    output = gr.Textbox(label="Status")
    file = gr.File(label="Download PDF")

    button = gr.Button("Generate Textbook")
    button.click(fn=generate_textbook, inputs=[subject, grade, topic, curriculum], outputs=[output, file])
    css=custom_css

demo.launch()