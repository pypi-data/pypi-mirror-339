from enum import Enum

LOGGER_NAME = "ScienceMuseumMCPServer"
SEARCH_ALL_PATH = "search"
SEARCH_OBJECTS_PATH = "search/objects"

class ScienceMuseumTools(str, Enum):
    SEARCH_ALL = "search_all"
    SEARCH_OBJECTS = "search_objects"

DEFAULT_LIMIT = 100
DEFAULT_OFFSET = 0
