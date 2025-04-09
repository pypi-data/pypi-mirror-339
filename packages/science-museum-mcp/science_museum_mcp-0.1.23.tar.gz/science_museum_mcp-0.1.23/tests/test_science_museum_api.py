import unittest
import urllib
from unittest.mock import patch

from requests import Response
from starlette.status import HTTP_409_CONFLICT, HTTP_200_OK

from science_museum_mcp import science_museum_api
from science_museum_mcp.constants import ScienceMuseumTools, SEARCH_ALL_PATH, SEARCH_OBJECTS_PATH
from science_museum_mcp.science_museum_api import data_object, search, BASE_URL


class ScienceMuseumApiTests(unittest.TestCase):

    def test_data_object_returns_correct_shape(self):
        records = [1, 2, 3]
        message = "Test message"
        success = True

        result = data_object(records, message, success)

        expected_result = {
            "records": records,
            "message": message,
            "success": success,
            "number_of_records": len(records)
        }

        self.assertEqual(result, expected_result)

    def test_handle_response_returns_correctly_if_status_code_not_ok(self):
        failed_response: Response = Response()
        failed_response.status_code = HTTP_409_CONFLICT # An error code the NHM API can return

        result = science_museum_api.handle_response(failed_response)

        expected_result_records = []
        expected_result_success = False

        self.assertEqual(result["records"], expected_result_records)
        self.assertEqual(result["success"], expected_result_success)

    def test_handle_response_returns_correctly_if_status_code_ok(self):
        successful_response: Response = Response()
        successful_response.status_code = HTTP_200_OK
        mock_api_data = [1, 2, 3]
        successful_response.json = lambda: {"data": mock_api_data}

        result = science_museum_api.handle_response(successful_response)

        expected_result_records = mock_api_data
        expected_result_success = True
        self.assertEqual(result["records"], expected_result_records)
        self.assertEqual(result["success"], expected_result_success)

    def test_get_url_path_match_statement(self):
        expected_all_path = SEARCH_ALL_PATH
        expected_objects_path = SEARCH_OBJECTS_PATH

        search_all_result = science_museum_api.get_url_path(ScienceMuseumTools.SEARCH_ALL)

        self.assertEqual(expected_all_path, search_all_result)

        search_objects_result = science_museum_api.get_url_path(ScienceMuseumTools.SEARCH_OBJECTS)

        self.assertEqual(search_objects_result, expected_objects_path)

    @patch("requests.get")
    @patch("science_museum_mcp.science_museum_api.handle_response")
    def test_search_calls_requests_get_with_correct_params(self, mock_handle_response, mock_requests_get):
        resource_type = ScienceMuseumTools.SEARCH_ALL
        search_term = "my term"
        limit = 10
        offset = 0

        mock_handle_response.return_value = {}
        base_url = f"{BASE_URL}/search"
        search(ScienceMuseumTools.SEARCH_ALL, search_term, limit, offset)

        mock_requests_get.assert_called_with(base_url, params={
            "q": urllib.parse.quote(search_term),
            "page[size]": limit,
            "page[number]": offset
        }, headers={"Accept": "application/json"})


if __name__ == '__main__':
    unittest.main()
