from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SearchQuery(BaseModel):
    query: str
    size: int = Field(default=10, ge=1, le=100)

class AdvancedSearchQuery(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    keywords: Optional[List[str]] = None
    content: Optional[str] = None
    size: int = Field(default=10, ge=1, le=100)

class SearchResult(BaseModel):
    title: str
    abstract: str
    content: str
    keywords: Optional[List[str]] = None
    score: Optional[float] = None