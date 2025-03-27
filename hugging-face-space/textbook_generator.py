import openai

def summarize_textbook_content(text):
    """Summarizes and structures the textbook content using GPT-4."""
    prompt = f"""
    Summarize the following textbook content into structured sections with bullet points, key takeaways, and practice questions.

    {text[:10000]}  # Only process first 10,000 characters to prevent overload
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]
