import json
import logging
import traceback

from mcp import stdio_server

from classes.tools import SearchTool, ScienceMuseumTools
from science_museum_mcp import science_museum_api
from mcp.server import Server
from mcp.types import Tool, TextContent

from science_museum_mcp.constants import DEFAULT_LIMIT, DEFAULT_OFFSET, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)


def search(search_type: ScienceMuseumTools, search_term: str, limit: int=DEFAULT_LIMIT, offset=DEFAULT_OFFSET) -> str:
    logger.info(f"Starting {search_type} for {search_term} with limit {limit} and offset {offset}")
    science_museum_api_result = science_museum_api.search(search_type, search_term, limit, offset)

    logger.info(science_museum_api_result["number_of_records"])

    return json.dumps(science_museum_api_result)

async def serve():
    server = Server("science-museum-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=ScienceMuseumTools.SEARCH_ALL,
                description="Tool to search all categories of the Science Museum API",
                inputSchema=SearchTool.model_json_schema(),
            ),
            Tool(
                name=ScienceMuseumTools.SEARCH_OBJECTS,
                description="Tool to search objects of the Science Museum API",
                inputSchema=SearchTool.model_json_schema(),
            ),
            Tool(
                name=ScienceMuseumTools.SEARCH_PEOPLE,
                description="Tool to search people in the Science Museum API",
                inputSchema=SearchTool.model_json_schema(),
            ),
            Tool(
                name=ScienceMuseumTools.SEARCH_DOCUMENTS,
                description="Tool to search documents in the Science Museum API",
                inputSchema=SearchTool.model_json_schema(),
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:

        try:
            match name:
                case ScienceMuseumTools.SEARCH_ALL:
                    search_type = ScienceMuseumTools.SEARCH_ALL
                case ScienceMuseumTools.SEARCH_OBJECTS:
                    search_type = ScienceMuseumTools.SEARCH_OBJECTS
                case ScienceMuseumTools.SEARCH_PEOPLE:
                    search_type = ScienceMuseumTools.SEARCH_PEOPLE
                case ScienceMuseumTools.SEARCH_DOCUMENTS:
                    search_type = ScienceMuseumTools.SEARCH_DOCUMENTS
                case _:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}, please specify a tool from the provided tools list"
                    )]

            search_term = arguments["search_term"]
            limit = arguments["limit"] if "limit" in arguments else DEFAULT_LIMIT
            offset = arguments["offset"] if "offset" in arguments else DEFAULT_OFFSET
            result = search(search_type, search_term, limit=limit, offset=offset)
            return [TextContent(
                type="text",
                text=result
            )]

        except Exception as e:
            logger.error(traceback.print_exc())
            return [TextContent(
                type="text",
                text=f"Tool encountered an error {e}. Please report this to the github page."
            )]


    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)