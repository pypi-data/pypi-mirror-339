"""
Tests for iiko_pkg.client
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from iiko_pkg.client import IikoClient
from iiko_pkg.models.auth import TokenResponse
from iiko_pkg.exceptions import NetworkError


class TestIikoClient(unittest.TestCase):
    """Test IikoClient class"""

    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key"
        self.client = IikoClient(api_key=self.api_key)

    @patch("requests.Session.post")
    def test_get_token(self, mock_post):
        """Test get_token method"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "token": "test_token",
            "expire_seconds": 3600
        }
        mock_post.return_value = mock_response

        # Call method
        token = self.client._get_token()

        # Assertions
        self.assertEqual(token, "test_token")
        self.assertIsNotNone(self.client.token)
        self.assertEqual(self.client.token.token, "test_token")
        self.assertEqual(self.client.token.expire_seconds, 3600)
        self.assertIsNotNone(self.client.token.created_at)

        # Check if token is cached
        token2 = self.client._get_token()
        self.assertEqual(token2, "test_token")
        mock_post.assert_called_once()  # Should only be called once

    @patch("requests.Session.post")
    def test_get_token_expired(self, mock_post):
        """Test get_token method with expired token"""
        # Set expired token
        self.client.token = TokenResponse(
            token="expired_token",
            expire_seconds=3600,
            created_at=datetime.now() - timedelta(hours=2)  # 2 hours ago
        )

        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "token": "new_token",
            "expire_seconds": 3600
        }
        mock_post.return_value = mock_response

        # Call method
        token = self.client._get_token()

        # Assertions
        self.assertEqual(token, "new_token")
        self.assertIsNotNone(self.client.token)
        self.assertEqual(self.client.token.token, "new_token")
        mock_post.assert_called_once()  # Should be called to get new token

    @patch("requests.Session.post")
    def test_get_token_error(self, mock_post):
        """Test get_token method with error"""
        # Mock error response
        mock_post.side_effect = Exception("Connection error")

        # Call method and check exception
        with self.assertRaises(NetworkError):
            self.client._get_token()

    @patch("iiko_pkg.client.IikoClient._get_token")
    @patch("requests.Session.request")
    def test_make_request(self, mock_request, mock_get_token):
        """Test _make_request method"""
        # Mock token
        mock_get_token.return_value = "test_token"

        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_request.return_value = mock_response

        # Call method
        result = self.client._make_request("POST", "/test", {"param": "value"})

        # Assertions
        self.assertEqual(result, {"key": "value"})
        mock_get_token.assert_called_once()
        mock_request.assert_called_once_with(
            method="POST",
            url="https://api-ru.iiko.services/test",
            headers={"Authorization": "Bearer test_token"},
            json={"param": "value"}
        )

    @patch("iiko_pkg.client.IikoClient._get_token")
    @patch("requests.Session.request")
    def test_make_request_error(self, mock_request, mock_get_token):
        """Test _make_request method with error"""
        # Mock token
        mock_get_token.return_value = "test_token"

        # Mock error response
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API error")
        mock_request.return_value = mock_response

        # Call method and check exception
        with self.assertRaises(Exception):
            self.client._make_request("POST", "/test", {"param": "value"})

    @patch("iiko_pkg.client.IikoClient._make_request")
    def test_get_organizations(self, mock_make_request):
        """Test get_organizations method"""
        # Mock response
        mock_make_request.return_value = {
            "organizations": [
                {
                    "id": "org1",
                    "name": "Organization 1",
                    "country": "Country",
                    "restaurantAddress": "Address",
                    "latitude": 1.0,
                    "longitude": 2.0
                }
            ]
        }

        # Call method
        result = self.client.get_organizations()

        # Assertions
        self.assertEqual(len(result.organizations), 1)
        self.assertEqual(result.organizations[0].id, "org1")
        self.assertEqual(result.organizations[0].name, "Organization 1")
        mock_make_request.assert_called_once_with(
            "POST",
            "/api/1/organizations",
            {
                "returnAdditionalInfo": False,
                "includeDisabled": False
            }
        )

    @patch("iiko_pkg.client.IikoClient._make_request")
    def test_get_menu(self, mock_make_request):
        """Test get_menu method"""
        # Mock response
        mock_make_request.return_value = {
            "menus": [
                {
                    "id": "menu1",
                    "name": "Menu 1",
                    "description": "Description",
                    "categories": [],
                    "products": [],
                    "groups": [],
                    "version": "1.0",
                    "organization_id": "org1"
                }
            ]
        }

        # Call method
        result = self.client.get_menu("org1")

        # Assertions
        self.assertEqual(len(result.menus), 1)
        self.assertEqual(result.menus[0].id, "menu1")
        self.assertEqual(result.menus[0].name, "Menu 1")
        mock_make_request.assert_called_once_with(
            "POST",
            "/api/1/nomenclature",
            {
                "organizationIds": ["org1"],
                "includeDeleted": False,
                "includeHidden": False
            }
        )


if __name__ == "__main__":
    unittest.main()
