import urllib.parse

import requests
from requests import Response
import logging

from classes.tools import ScienceMuseumTools
from science_museum_mcp.constants import LOGGER_NAME, SEARCH_ALL_PATH, SEARCH_OBJECTS_PATH, \
    SEARCH_PEOPLE_PATH, SEARCH_DOCUMENTS_PATH

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)
BASE_URL = "https://collection.sciencemuseumgroup.org.uk"

# Data contract
def data_object(records: list, msg: str | None, success: bool) -> dict:
    return {
        "records": records,
        "message": msg,
        "success": success,
        "number_of_records": len(records)
    }


def handle_response(response: Response) -> dict:
    if not response.ok:
        logger.error(response.reason)
        return data_object([],
                               f"Request to Science Museum API failed with status code {response.status_code}",
                               False)
    logger.info(response)
    data = response.json()

    records = data["data"]

    if len(records) == 0:
        logger.info("0 Records returned")
        return data_object([], "Received OK from Science Museum API, but received no records.", True)

    logger.info(f"Found {len(records)} records")
    return data_object(records, None, True)

def get_url_path(search_type: ScienceMuseumTools) -> str | None:
    match search_type:
        case ScienceMuseumTools.SEARCH_ALL:
            url_path = SEARCH_ALL_PATH
        case ScienceMuseumTools.SEARCH_OBJECTS:
            url_path = SEARCH_OBJECTS_PATH
        case ScienceMuseumTools.SEARCH_PEOPLE:
            url_path = SEARCH_PEOPLE_PATH
        case ScienceMuseumTools.SEARCH_DOCUMENTS:
            url_path = SEARCH_DOCUMENTS_PATH
        case _:
            url_path = None

    return url_path

def search(search_type: ScienceMuseumTools, search_term: str, limit: int, offset: int) -> dict:
    url_path = get_url_path(search_type)

    url: str = f"{BASE_URL}/{url_path}"
    params = {
        "q": search_term,
        "page[size]": limit,
        "page[number]": offset
    }

    headers = {
        "Accept": "application/json"
    }
    logger.info(f"GET {url} with params {params}")

    response = requests.get(url, params=params, headers=headers)

    return handle_response(response)
