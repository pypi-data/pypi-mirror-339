from typing import List, Optional
from pydantic import BaseModel, Field

class WikipediaDetailResult(BaseModel):
    """
    Wikipedia detailed page information
    
    - title: Wikipedia page title
    - content: Page content
    - url: Wikipedia page URL
    - related_links: List of related page links
    """
    
    title: str = Field(description="Wikipedia page title")
    content: str = Field(description="Wikipedia page content")
    url: str = Field(description="Wikipedia page URL")
    related_links: List[dict] = Field(default_factory=list, description="List of related page links")