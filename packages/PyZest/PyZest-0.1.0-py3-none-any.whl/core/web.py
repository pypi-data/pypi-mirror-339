import requests

def fetch_url(url: str, method: str = "GET", **kwargs) -> str:
    """Making an HTTP request and returning text.
    
    Example:
    >>> fetch_url("https://api.example.com/data")
    """
    response = requests.request(method, url, **kwargs)
    response.raise_for_status()
    return response.text

def scrape_links(url: str) -> list:
    """Parses all links from a web page."""
    from bs4 import BeautifulSoup
    html = fetch_url(url)
    soup = BeautifulSoup(html, "html.parser")
    return [a["href"] for a in soup.find_all("a", href=True)]