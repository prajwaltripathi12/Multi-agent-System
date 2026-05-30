from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()   


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str)->str:
    """Search the web for recent and reliable information on a topic. Returns Titles and URLs and snippets of the search results."""
    response = tavily_client.search(query=query,max_results=5)
    
    out= []
    for r in response['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
            )
    return "\n----\n".join(out)   

@tool
def web_scrape(url: str)->str:
    """Scrape and returns clean text content from a given URL for deeper reading the content."""

    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'footer', 'nav']):
            tag.decompose()
        return soup.get_text(separator='\n', strip=True)[:2000]  # Return the first 2000 characters of clean text
    except Exception as e:
        return f"Error scraping the web page: {str(e)}"
    


