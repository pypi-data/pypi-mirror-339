"""
Tests for iiko_pkg.exceptions
"""

import unittest

from iiko_pkg.exceptions import IikoError, AuthenticationError, ApiError, ValidationError, NetworkError


class TestExceptions(unittest.TestCase):
    """Test exceptions"""

    def test_iiko_error(self):
        """Test IikoError exception"""
        error = IikoError("Test error")
        self.assertEqual(str(error), "Test error")

    def test_authentication_error(self):
        """Test AuthenticationError exception"""
        error = AuthenticationError("Test authentication error")
        self.assertEqual(str(error), "Test authentication error")
        self.assertIsInstance(error, IikoError)

    def test_api_error(self):
        """Test ApiError exception"""
        error = ApiError(400, "Test API error")
        self.assertEqual(str(error), "API Error 400: Test API error")
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.error_message, "Test API error")
        self.assertIsNone(error.response)
        self.assertIsInstance(error, IikoError)
        
        # Test with response
        response = "Test response"
        error = ApiError(400, "Test API error", response)
        self.assertEqual(str(error), "API Error 400: Test API error")
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.error_message, "Test API error")
        self.assertEqual(error.response, "Test response")
        self.assertIsInstance(error, IikoError)

    def test_validation_error(self):
        """Test ValidationError exception"""
        error = ValidationError("Test validation error")
        self.assertEqual(str(error), "Test validation error")
        self.assertIsInstance(error, IikoError)

    def test_network_error(self):
        """Test NetworkError exception"""
        error = NetworkError("Test network error")
        self.assertEqual(str(error), "Test network error")
        self.assertIsInstance(error, IikoError)


if __name__ == "__main__":
    unittest.main()
