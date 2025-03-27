import os
import requests
from bs4 import BeautifulSoup

OPENSTAX_URL = "https://openstax.org/subjects"

def get_openstax_books():
    response = requests.get(OPENSTAX_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    books = {}
    for link in soup.find_all("a", href=True):
        if "/books/" in link["href"]:
            title = link.text.strip()
            books[title] = f"https://openstax.org{link['href']}"

    return books

def get_pdfdrive_books(query):
    url = f"https://www.pdfdrive.com/search?q={query.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = {}
    for a in soup.find_all("a", href=True):
        if a["href"].startswith("/download"):
            title = a.text.strip()
            books[title] = f"https://www.pdfdrive.com{a['href']}"
    return books

def get_gutenberg_books(query):
    url = f"https://www.gutenberg.org/ebooks/search/?query={query.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = {}
    for book in soup.find_all("li", class_="booklink"):
        title_elem = book.find("span", class_="title")
        link_elem = book.find("a", href=True)
        if title_elem and link_elem:
            title = title_elem.text.strip()
            link = "https://www.gutenberg.org" + link_elem["href"]
            books[title] = link
    return books

def get_umn_books():
    url = "https://open.umn.edu/opentextbooks"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = {}
    for link in soup.find_all("a", href=True):
        if "/opentextbooks" in link["href"]:
            title = link.text.strip()
            books[title] = link["href"]
    return books

def get_archive_books(query):
    books = {}
    try:
        url = f"https://archive.org/search.php?query={query.replace(' ', '+')}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.find_all("div", class_="ttl"):
            link = item.find("a", href=True)
            if link:
                title = link.text.strip()
                books[title] = "https://archive.org" + link["href"]
    except Exception as e:
        print(f"Error fetching from archive.org: {e}")
    return books

def download_pdf(book_url):
    response = requests.get(book_url, stream=True)
    content_type = response.headers.get("Content-Type", "")

    # If the link is HTML, try to extract the actual PDF link
    if "text/html" in content_type:
        soup = BeautifulSoup(response.text, "html.parser")

        # Try common selectors for actual PDF download links
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.endswith(".pdf"):
                pdf_url = href if href.startswith("http") else os.path.join(book_url, href)
                return download_pdf(pdf_url)
        raise ValueError("No direct PDF link found on the page.")

    elif "application/pdf" not in content_type:
        raise ValueError(f"The URL does not point to a valid PDF. Content-Type: {content_type}")

    filename = "textbook.pdf"
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return filename

def get_all_sources_books(query):
    books = {}
    books.update(get_openstax_books())
    books.update(get_pdfdrive_books(query))
    books.update(get_gutenberg_books(query))
    books.update(get_umn_books())
    books.update(get_archive_books(query))
    return books