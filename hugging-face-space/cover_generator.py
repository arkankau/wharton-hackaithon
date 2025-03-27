import openai
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def generate_cover_image(subject, grade, author="AI-Generated"):
    """Generate a textbook cover using DALL·E and overlay text."""
    prompt = f"A modern, professional textbook cover for a {grade}-level subject on {subject}. The cover should include educational symbols, clean typography, and an academic feel."
    
    # Generate image using DALL·E
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    
    image_url = response["data"][0]["url"]
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    
    # Overlay Text
    draw = ImageDraw.Draw(image)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 60)
        font_subtext = ImageFont.truetype("arial.ttf", 40)
    except:
        font_title = ImageFont.load_default()
        font_subtext = ImageFont.load_default()
    
    title_text = f"{subject} Textbook"
    draw.text((100, 100), title_text, fill="white", font=font_title)

    grade_text = f"Grade: {grade}"
    draw.text((100, 180), grade_text, fill="white", font=font_subtext)

    author_text = f"Author: {author}"
    draw.text((100, 950), author_text, fill="white", font=font_subtext)

    filename = f"{subject}_{grade}_cover.png"
    image.save(filename)
    
    return filename
