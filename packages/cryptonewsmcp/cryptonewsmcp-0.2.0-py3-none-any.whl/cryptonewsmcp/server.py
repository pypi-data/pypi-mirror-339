from typing import Final
from typing import Literal

import feedparser
from markdownify import markdownify as md
from mcp.server.fastmcp import FastMCP

from cryptonewsmcp.utils import fetch_text_from_url

RSS_URLS = {
    "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss",
    "decrypt": "https://decrypt.co/feed",
}

INSTRUCTIONS: Final[str] = """
Crypto news MCP server for CoinDesk and Decrypt content.

Tools:
- recent_news: Fetches latest news from RSS feeds
- read_news: Fetches article HTML from URL and converts it to Markdown

Usage:
1. Get headlines with recent_news
2. Get and convert articles with read_news
3. Cite sources when republishing
"""


mcp = FastMCP("MCP Server Coindesk", instructions=INSTRUCTIONS, log_level="ERROR")


@mcp.tool()
async def read_news(url: str) -> str:
    """
    Fetches article HTML from URL and converts it to Markdown.

    Args:
        url: Article URL to retrieve

    Returns:
        Markdown-formatted article content
    """
    html = await fetch_text_from_url(url)
    markdown = md(html, strip=["a", "img"])
    return markdown


@mcp.tool()
async def recent_news(site: Literal["coindesk", "decrypt"]) -> str:
    """
    Gets latest crypto news from specified site.

    Args:
        site: Site to fetch news from ("coindesk" or "decrypt")

    Returns:
        Formatted list of news entries with titles, links, dates and summaries
    """
    url = RSS_URLS.get(site)
    if url is None:
        raise ValueError(f"Unsupported site: {site}")

    text = await fetch_text_from_url(url)
    feed = feedparser.parse(text)
    return "\n---\n".join(
        f"{entry['title']}\n{entry['link']}\n{entry['updated']}\n{entry['summary']}" for entry in feed["entries"]
    )


def main() -> None:
    mcp.run()
