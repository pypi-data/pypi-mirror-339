from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

class WikipediaSearchResultItem(BaseModel):
    """
    Wikipedia search result item
    
    - title: Search result title
    - detail: Detailed content
    """
    
    title: str = Field(description="Search result title")
    detail: str = Field(description="Search result detailed content")

class WikipediaSearchResults(BaseModel):
    """
    Wikipedia search results list
    - results: List of search results
    """
    results: List[WikipediaSearchResultItem] = Field(default_factory=list, description="List of search results") 