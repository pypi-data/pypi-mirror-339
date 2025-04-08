from typing import List, Optional
from pydantic import BaseModel, Field

class WikipediaSearchRequest(BaseModel):
    """
    Request model for Wikipedia advanced search
    
    - plain: List of words to include (these words)
    - phrase: Exact phrase match (exact match with this phrase)
    - not_words: List of words to exclude (exclude these words)
    - or_words: List of alternative words (one of these words)
    - search_query: General search query
    - language: Language code for search (default: en)
    """
    
    plain: Optional[List[str]] = Field(default=None, description="Include these words")
    phrase: Optional[str] = Field(default=None, description="Exact match with this phrase")
    not_words: Optional[List[str]] = Field(default=None, description="Exclude these words")
    or_words: Optional[List[str]] = Field(default=None, description="Include one of these words")
    search_query: Optional[str] = Field(default=None, description="General search query")
    language: str = Field(default="en", description="Language code for search")
    
    def to_search_query(self) -> str:
        """
        Converts search request to Wikipedia search query string
        """
        query_parts = []
        
        # Add general search query
        if self.search_query:
            query_parts.append(self.search_query)
        
        # These words (plain)
        if self.plain:
            query_parts.extend(self.plain)
        
        # Exact phrase match (phrase)
        if self.phrase:
            query_parts.append(f'"{self.phrase}"')
        
        # Words to exclude (not_words)
        if self.not_words:
            query_parts.extend([f'-{word}' for word in self.not_words])
        
        # Alternative words (or_words)
        if self.or_words and len(self.or_words) > 1:
            or_query = " OR ".join(self.or_words)
            query_parts.append(f'({or_query})')
        elif self.or_words and len(self.or_words) == 1:
            query_parts.append(self.or_words[0])
        
        return " ".join(query_parts) 