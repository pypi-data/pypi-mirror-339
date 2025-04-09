import json

from bs4 import BeautifulSoup

from .types import News


def extract_news_from_decrypt(html: str) -> News:
    """
    Extracts structured news information from a Decrypt article HTML.

    Parses the HTML content to extract the article title, subtitle, content,
    and author information.

    Args:
        html (str): Raw HTML content of a Decrypt article page

    Returns:
        News: Structured representation of the news article
    """
    soup = BeautifulSoup(html, "html.parser")

    # Try to extract data from JSON-LD first (most reliable method)
    json_ld = extract_json_ld(soup)
    if json_ld:
        title = json_ld.get("headline")
        subtitle = json_ld.get("description")
        author = extract_author_from_json_ld(json_ld)
        # Content needs to be extracted from the HTML as it's not in the JSON-LD
        content = extract_content_from_decrypt(soup)

        return News(title=title, subtitle=subtitle, content=content, author=author)

    # Fallback to HTML extraction if JSON-LD fails
    title = extract_title_from_decrypt(soup)
    subtitle = extract_subtitle_from_decrypt(soup)
    content = extract_content_from_decrypt(soup)
    author = extract_author_from_decrypt(soup)

    return News(title=title, subtitle=subtitle, content=content, author=author)


def extract_json_ld(soup: BeautifulSoup) -> dict:
    """
    Extracts and parses JSON-LD data from article head.

    Args:
        soup (BeautifulSoup): Parsed HTML document

    Returns:
        dict: JSON-LD data or empty dict if not found
    """
    json_ld_tag = soup.find("script", {"type": "application/ld+json"})
    if not json_ld_tag:
        return {}

    try:
        data = json.loads(json_ld_tag.string)
        return data
    except (json.JSONDecodeError, AttributeError):
        return {}


def extract_author_from_json_ld(json_ld: dict) -> str | None:
    """
    Extracts author name from JSON-LD data.

    Args:
        json_ld (dict): JSON-LD data structure

    Returns:
        str | None: Author name if found, None otherwise
    """
    author_data = json_ld.get("author", {})
    if isinstance(author_data, dict):
        return author_data.get("name")
    return None


def extract_title_from_decrypt(soup: BeautifulSoup) -> str | None:
    """
    Extracts article title from HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML document

    Returns:
        str | None: Article title if found, None otherwise
    """
    # Try meta tags first
    meta_title = soup.find("meta", property="og:title")
    if meta_title and meta_title.get("content"):
        title = meta_title.get("content")
        # Remove site name suffix if present
        if " - Decrypt" in title:
            title = title.split(" - Decrypt")[0]
        return title

    # Fallback to title tag
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.get_text()
        if " - Decrypt" in title:
            title = title.split(" - Decrypt")[0]
        return title

    return None


def extract_subtitle_from_decrypt(soup: BeautifulSoup) -> str | None:
    """
    Extracts article subtitle from HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML document

    Returns:
        str | None: Article subtitle if found, None otherwise
    """
    meta_desc = soup.find("meta", property="og:description") or soup.find("meta", {"name": "description"})
    if meta_desc and meta_desc.get("content"):
        return meta_desc.get("content")

    return None


def extract_content_from_decrypt(soup: BeautifulSoup) -> str | None:
    """
    Extracts article content from HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML document

    Returns:
        str | None: Article content if found, None otherwise
    """
    # Look for article body paragraphs
    # This might need adjustment based on actual HTML structure
    article_body = soup.select("article p")
    if article_body:
        return "\n\n".join([p.get_text().strip() for p in article_body if p.get_text().strip()])

    return None


def extract_author_from_decrypt(soup: BeautifulSoup) -> str | None:
    """
    Extracts article author from HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML document

    Returns:
        str | None: Author name if found, None otherwise
    """
    # Look for meta author tag
    meta_author = soup.find("meta", {"name": "author"})
    if meta_author and meta_author.get("content"):
        author = meta_author.get("content")
        if "Decrypt / " in author:
            author = author.split("Decrypt / ")[1]
        return author

    return None
