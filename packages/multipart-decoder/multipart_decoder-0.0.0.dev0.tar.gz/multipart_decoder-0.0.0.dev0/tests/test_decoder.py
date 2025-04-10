"""
Unit tests for the multipart_decoder package.
"""

import unittest
from multipart_decoder import MultipartFormParser


class TestMultipartFormParser(unittest.TestCase):
    def test_basic_form_fields(self):
        """Test decoding of basic form fields."""
        content_type = (
            "multipart/form-data; boundary=----WebKitFormBoundaryp0mBfJEEcQtmxFCF"
        )
        body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5cDBtQmZKRUVjUXRteEZDRg0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDEiDQoNCnZhbHVlMQ0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5cDBtQmZKRUVjUXRteEZDRg0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDIiDQoNCnZhbHVlMg0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5cDBtQmZKRUVjUXRteEZDRi0tDQo="

        result = MultipartFormParser(body, content_type)
        self.assertEqual(result["fields"]["field1"], "value1")
        self.assertEqual(result["fields"]["field2"], "value2")

    def test_file_upload(self):
        """Test decoding of file uploads."""
        content_type = (
            "multipart/form-data; boundary=----WebKitFormBoundaryI6YbOCiSAMjU6wK2"
        )
        body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5STZZYk9DaVNBTWpVNndLMg0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWxlMSI7IGZpbGVuYW1lPSJleGFtcGxlLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQpIZWxsbywgd29ybGQhDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnlJNlliT0NpU0FNalU2d0syLS0NCg=="

        result = MultipartFormParser(body, content_type)
        self.assertIn("file1", result["files"])

        file_info = result["files"]["file1"]
        self.assertEqual(file_info["filename"], "example.txt")
        self.assertEqual(file_info["content_type"], "text/plain")
        self.assertEqual(file_info["content"], b"Hello, world!")
        self.assertEqual(file_info["size"], len(b"Hello, world!"))

    def test_mixed_content(self):
        """Test decoding of mixed content (form fields and file uploads)."""
        content_type = (
            "multipart/form-data; boundary=----WebKitFormBoundary4AQwYOUUCEUw9hsX"
        )
        body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDEiDQoNCnZhbHVlMQ0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDIiDQoNCnZhbHVlMg0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWxlMSI7IGZpbGVuYW1lPSJleGFtcGxlLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQpIZWxsbywgd29ybGQhDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnk0QVF3WU9VVUNFVXc5aHNYLS0NCg=="

        result = MultipartFormParser(body, content_type)
        self.assertEqual(result["fields"]["field1"], "value1")
        self.assertEqual(result["fields"]["field2"], "value2")

        file_info = result["files"]["file1"]
        self.assertEqual(file_info["filename"], "example.txt")
        self.assertEqual(file_info["content_type"], "text/plain")
        self.assertEqual(file_info["content"], b"Hello, world!")
        self.assertEqual(file_info["size"], len(b"Hello, world!"))

    def test_empty_body(self):
        """Test validation of empty request body."""
        content_type = "multipart/form-data; boundary=something"
        body = ""
        
        with self.assertRaises(ValueError) as context:
            MultipartFormParser(body, content_type)
        self.assertIn("Request body cannot be empty", str(context.exception))

    def test_malformed_multipart_data(self):
        """Test handling of malformed multipart data."""
        content_type = "multipart/form-data; boundary=boundary"
        # Base64 encoded partial/malformed multipart data
        body = "LS0tYm91bmRhcnkNCkNvbnRlbnQtRGlzcG9zaXRpb246IGZvcm0tZGF0YTsNCg=="
        
        with self.assertRaises(Exception) as context:
            MultipartFormParser(body, content_type)
        self.assertIn("Failed to", str(context.exception))


if __name__ == "__main__":
    unittest.main()
