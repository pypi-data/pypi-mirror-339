#!/usr/bin/env python3
# server.py

from mcp.server.fastmcp import FastMCP
import re
import json
from urllib.request import urlopen, Request
from urllib.parse import quote
from bs4 import BeautifulSoup
from src.model.response.wikipedia_detail import WikipediaDetailResult
from src.model.response.wikipedia_search_result import WikipediaSearchResults, WikipediaSearchResultItem
from src.model.request.wikipedia_search import WikipediaSearchRequest

mcp = FastMCP(
    name = "wiki-mcp-server",
    dependencies=["bs4"]
)


@mcp.tool()
def search_wekipedia(query: WikipediaSearchRequest) -> WikipediaSearchResults:
    """
    Performs advanced search on Wikipedia.
    
    Args:
        query: Wikipedia search request model
    
    Returns:
        WikipediaSearchResults: List of search results
    """
    # Generate search query
    search_query = query.to_search_query()
    if not search_query.strip():
        return WikipediaSearchResults(results=[])
    
    # URL encoding
    encoded_query = quote(search_query)
    language = query.language
    
    # Create advanced search fields JSON
    advanced_fields = {"fields": {}}
    
    # Add only non-empty fields
    if query.plain:
        advanced_fields["fields"]["plain"] = query.plain
    
    if query.phrase:
        advanced_fields["fields"]["phrase"] = query.phrase
    
    if query.not_words:
        advanced_fields["fields"]["not"] = query.not_words
    
    if query.or_words:
        advanced_fields["fields"]["or"] = query.or_words
    
    # Encode advanced search fields JSON
    advanced_search_json = json.dumps(advanced_fields)
    encoded_advanced_search = quote(advanced_search_json)
    
    # Base URL parameters
    params = {
        "search": encoded_query,
        "title": "특수:검색",
        "profile": "advanced",
        "fulltext": "1",
        "ns0": "1"
    }
    
    # Add advanced search fields only if present
    if advanced_fields["fields"]:
        params["advancedSearch-current"] = encoded_advanced_search
    
    # Create URL
    url_params = "&".join([f"{k}={v}" for k, v in params.items()])
    search_url = f"https://{language}.wikipedia.org/w/index.php?{url_params}"
    
    try:
        # Set user agent
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko)'}
        request = Request(search_url, headers=headers)
        
        # Fetch search results page
        html = urlopen(request)
        bs = BeautifulSoup(html, "html.parser")
        
        # Extract search results
        search_results = []
        
        # Extract search result items
        result_items = bs.find_all("li", {"class": "mw-search-result"})
        
        for item in result_items:
            # Extract title
            title_elem = item.find("div", {"class": "mw-search-result-heading"})
            title = title_elem.get_text().strip() if title_elem else "No title"
            
            # Extract content
            detail_elem = item.find("div", {"class": "searchresult"})
            detail = ""
            if detail_elem:
                # Extract content with HTML tags (may contain span tags)
                detail = str(detail_elem)
                # If you need to remove HTML tags, use the code below
                # detail = detail_elem.get_text().strip()
            
            # Add search result item
            search_results.append(
                WikipediaSearchResultItem(
                    title=title,
                    detail=detail
                )
            )
        
        # Return results
        return WikipediaSearchResults(results=search_results)
    
    except Exception as e:
        # Return empty results in case of error
        return WikipediaSearchResults(results=[])









# Detail search

@mcp.tool()
def search_wikipedia_detail(query: str, language: str = "en") -> WikipediaDetailResult:
    """
    Fetches detailed content from a Wikipedia page.
    
    Args:
        query: Wikipedia page title or search term
        language: Wikipedia language code (default: "en", Korean: "ko")
    
    Returns:
        WikipediaDetailResult: Detailed information including title, content, URL
    """
    # Encode query string for URL
    encoded_query = quote(query.replace(' ', '_'))
    
    # Create Wikipedia URL
    url = f"https://{language}.wikipedia.org/wiki/{encoded_query}"
    
    try:
        # Fetch page
        html = urlopen(url)
        bs = BeautifulSoup(html, "html.parser")
        
        # Extract title
        title = bs.h1.get_text() if bs.h1 else query
        
        # Extract content (first paragraphs)
        content = ""
        bodyContent = bs.find("div", {"id": "bodyContent"})
        if bodyContent:
            paragraphs = bodyContent.find_all("p")
            if paragraphs:
                # Combine first 3 paragraphs
                content = "\n\n".join([p.get_text() for p in paragraphs[:3]])
        
        # Extract related links (maximum 5)
        related_links = []
        links = bs.find_all("a", href=re.compile("^(/wiki/)"))
        link_count = 0
        for link in links:
            if 'href' in link.attrs and link_count < 5:
                path = link.attrs['href']
                # Include only internal wiki links
                if re.match("^(/wiki/[^:]+$)", path) and (
                    ("Main_Page" not in path and language == "en") or 
                    ("대문" not in path and language == "ko")
                ):
                    related_links.append({
                        "title": link.get_text(),
                        "url": f"https://{language}.wikipedia.org{path}"
                    })
                    link_count += 1
        
        # Return result
        return WikipediaDetailResult(
            title=title,
            content=content,
            url=url,
            related_links=related_links
        )
    
    except Exception as e:
        # Return basic information in case of error
        return WikipediaDetailResult(
            title=query,
            content=f"An error occurred while fetching the page: {str(e)}",
            url=url
        )


def run_server():
    mcp.run()


if __name__ == "__main__":
    run_server()
