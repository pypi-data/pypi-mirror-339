from enum import Enum
from typing import Optional

from pydantic import BaseModel

from science_museum_mcp.constants import DEFAULT_LIMIT, DEFAULT_OFFSET

class ScienceMuseumTools(str, Enum):
    SEARCH_ALL = "search_all"
    SEARCH_OBJECTS = "search_objects"
    SEARCH_PEOPLE = "search_people"
    SEARCH_DOCUMENTS = "search_documents"

class SearchTool(BaseModel):
    search_term: str
    limit: Optional[int] = DEFAULT_LIMIT
    offset: Optional[int] = DEFAULT_OFFSET
