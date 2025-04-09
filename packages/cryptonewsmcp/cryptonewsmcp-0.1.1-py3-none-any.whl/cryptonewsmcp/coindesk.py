from datetime import datetime

import dateutil.parser
from bs4 import BeautifulSoup
from pydantic import Field

from .types import News


class CoindeskNews(News):
    published_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)

    def __str__(self) -> str:
        """
        Creates a formatted string representation of the news article.

        Returns:
            str: Human-readable formatted string with the article's metadata
                 and a preview of its content
        """
        result = [f"Title: {self.title}"]

        if self.subtitle:
            result.append(f"Subtitle: {self.subtitle}")

        if self.author:
            result.append(f"By: {self.author}")

        dates = []
        if self.published_at:
            dates.append(f"Published: {self.published_at.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.updated_at:
            dates.append(f"Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")

        if dates:
            result.append(" | ".join(dates))

        if self.content:
            content_preview = self.content[:150] + "..." if len(self.content) > 150 else self.content
            result.append(f"\n{content_preview}")

        return "\n".join(result)


def extract_title(soup: BeautifulSoup) -> str | None:
    """
    Extracts the main article title from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML document

    Returns:
        str | None: The article's main headline if found, None otherwise
    """
    title_tag = soup.select_one("h1.font-headline-lg.font-medium")
    if title_tag is None:
        return None
    return title_tag.get_text().strip()


def extract_subtitle(soup: BeautifulSoup) -> str | None:
    """
    Extracts the article subtitle from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML document

    Returns:
        str | None: The article's subtitle or secondary headline if found, None otherwise
    """
    subtitle_tag = soup.select_one("h2.font-headline-xs.text-charcoal-600")
    if subtitle_tag is None:
        return None
    return subtitle_tag.get_text().strip()


def extract_content(soup: BeautifulSoup) -> str | None:
    """
    Extracts the main article content from the parsed HTML.

    Locates and combines all body text paragraphs from the article's content section.

    Args:
        soup (BeautifulSoup): Parsed HTML document

    Returns:
        str | None: The article's full text content or None if no content is found
    """
    results = soup.select("div.document-body.font-body-lg")
    return "\n".join([result.get_text().strip() for result in results])


def extract_author(soup: BeautifulSoup) -> str | None:
    """
    Extracts the author's name from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML document

    Returns:
        str | None: The article author's name if found, None otherwise
    """
    result = soup.select_one("h5.font-headline-sm.font-medium")
    if result is None:
        return None
    return result.get_text().strip()


def extract_coindesk_news(html: str) -> CoindeskNews:
    """
    Processes HTML content to extract structured news article information.

    Parses the provided HTML and extracts relevant data to construct a complete
    CoindeskNewsPage object with all available article metadata and content.

    Args:
        html (str): Raw HTML content of a CoinDesk article page

    Returns:
        CoindeskNewsPage: Structured representation of the news article
    """
    soup = BeautifulSoup(html, "html.parser")

    published_at, updated_at = extract_published_at(soup)

    return CoindeskNews(
        title=extract_title(soup),
        subtitle=extract_subtitle(soup),
        content=extract_content(soup),
        author=extract_author(soup),
        published_at=published_at,
        updated_at=updated_at,
    )


def extract_published_at(soup: BeautifulSoup) -> tuple[datetime | None, datetime | None]:
    """
    Extracts publication and update timestamps from the parsed HTML.

    Identifies and parses date strings in the article metadata section to determine
    when the article was first published and when it was last updated.

    Args:
        soup (BeautifulSoup): Parsed HTML document

    Returns:
        tuple[datetime | None, datetime | None]: A tuple containing the publication
            timestamp and update timestamp (if available), with None values for any
            timestamps that could not be extracted
    """
    tag = soup.select_one("div.font-metadata.flex.gap-4.text-charcoal-600.flex-col.md\\:block")
    if tag is None:
        return None, None

    published_at = None
    updated_at = None

    results = tag.select("span")
    for result in results:
        date_str = result.get_text().strip()
        if "Published" in date_str:
            published_at = dateutil.parser.parse(date_str.removeprefix("Published "))
        elif "Updated" in date_str:
            updated_at = dateutil.parser.parse(date_str.removeprefix("Updated "))
        else:
            published_at = dateutil.parser.parse(date_str)
    return published_at, updated_at
