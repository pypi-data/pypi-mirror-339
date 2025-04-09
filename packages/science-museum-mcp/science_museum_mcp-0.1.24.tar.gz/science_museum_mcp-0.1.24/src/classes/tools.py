from typing import Optional

from pydantic import BaseModel

from science_museum_mcp.constants import DEFAULT_LIMIT, DEFAULT_OFFSET


class SearchAll(BaseModel):
    search_term: str
    limit: Optional[int] = DEFAULT_LIMIT # Default to this value to ensure this field is not required in the JSON model schema
    offset: Optional[int] = DEFAULT_OFFSET

class SearchObjects(BaseModel):
    search_term: str
    limit: Optional[int] = DEFAULT_LIMIT
    offset: Optional[int] = DEFAULT_OFFSET

class SearchPeople(BaseModel):
    search_term: str
    limit: Optional[int] = DEFAULT_LIMIT
    offset: Optional[int] = DEFAULT_OFFSET
