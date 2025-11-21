# tests/test_atlas_client.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, Mock
from atlas_client import AtlasClient

class TestAtlasClient(unittest.TestCase):
    def setUp(self):
        self.client = AtlasClient(
            url="http://localhost:21000",
            username="admin",
            password="admin"
        )
        self.sample_guid = "1234-abcd-5678-efgh"
        self.sample_entity = {
            "typeName": "test_entity",
            "attributes": {"name": "Test Entity", "qualifiedName": "Test Entity@localhost"}
        }

    @patch("atlas_client.requests.Session.get")
    def test_search_entities(self, mock_get):
        # Mock da resposta da API
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"entities": [{"name": "Test Entity"}]}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_get.return_value = mock_response

        result = self.client.search_entities("Test Entity")
        self.assertIn("entities", result)
        self.assertEqual(result["entities"][0]["name"], "Test Entity")

    @patch("atlas_client.requests.Session.post")
    def test_create_entity(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "guidAssignments": {self.sample_entity["attributes"]["qualifiedName"]: self.sample_guid}
        }
        mock_response.headers = {"Content-Type": "application/json"}
        mock_post.return_value = mock_response

        result = self.client.create_entity({"entities": [self.sample_entity]})
        self.assertIn(self.sample_entity["attributes"]["qualifiedName"], result["guidAssignments"])
        self.assertEqual(result["guidAssignments"][self.sample_entity["attributes"]["qualifiedName"]], self.sample_guid)

    @patch("atlas_client.requests.Session.get")
    def test_get_entity(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"entity": self.sample_entity}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_get.return_value = mock_response

        result = self.client.get_entity(self.sample_guid)
        self.assertIn("entity", result)
        self.assertEqual(result["entity"]["typeName"], "test_entity")

    @patch("atlas_client.requests.Session.get")
    def test_get_lineage(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"nodes": [], "edges": []}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_get.return_value = mock_response

        result = self.client.get_lineage(self.sample_guid)
        self.assertIn("nodes", result)
        self.assertIn("edges", result)
        self.assertEqual(result["nodes"], [])
        self.assertEqual(result["edges"], [])

if __name__ == "__main__":
    unittest.main()
