from time import sleep
import requests
from bs4 import BeautifulSoup
from googlesearch import search


DEFINITIONS = [
    {
        "name": "fetch_content",
        "description": "Get the contents of the given URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to fetch."
                },
            },
            "required": ["url"]
        }
    },
    {
        "name": "web_search",
        "description": "Get search results for a query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string."
                },
            },
            "required": ["query"],
        },
    },
]


def fetch_content(url):
    """
    Get the contents of the given URL.
    """
    print("Fetching content from {}".format(url))
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove non-content elements
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()

        def preserve_links(tag):
            """Convert a tag's contents to string, preserving <a> links."""
            if tag.name == 'a':
                return f"[{tag.get_text()}]({tag.get('href')})"
            return tag.get_text()

        # Collect all text, with links formatted
        content = []
        for element in soup.find_all(['p', 'li', 'div', 'span']):
            content.append(preserve_links(element))

        if content:
            text = '\n'.join(content)
            return (
                f"Below are the contents of the URL: {url}. "
                f"If you think it is required to extend your research, "
                f"you can request the contents of the relevant URLs mentioned in this page "
                f"by calling fetch_content function.\n\n"
                f"PAGE CONTENTS:\n\n{text}"
            )


def web_search(query):
    """
    Get Google search results for a query.
    """
    print("Searching for {}".format(query))
    results = list(search(query, num_results=100, advanced=True))  # Convert generator to list
    retry = 1
    while not results and retry < 5:
        # May be rate limited; retry
        sleep(.5 * retry)
        results = list(search(query, num_results=100, advanced=True))
        retry += 1
    if results:
        results_markdown = (
            f'Below are the list of items returned for your query: "{query}".\n'
            f'For the items you find to be relevant to your quest, '
            f'you can call the "fetch_content" function to retrieve the full content.\n\n'
        )
        for item in results:
            results_markdown += f"### [{item.title}]({item.url})\n{item.description}\n\n"
        return results_markdown
