import httpx


async def fetch_text_from_url(url: str) -> str:
    """
    Asynchronously retrieves text content from a specified URL.

    Makes an HTTP GET request to the provided URL and returns the response
    content as text. Handles connection setup and cleanup automatically.

    Args:
        url (str): The URL to fetch content from

    Returns:
        str: The text content received from the URL

    Raises:
        HTTPStatusError: If the HTTP request returns a non-2xx status code
        RequestError: If a network-related error occurs during the request
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
