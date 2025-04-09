"""
Unit tests for the multipart_decoder package.
"""

import unittest
from multipart_decoder import MultipartDecoder


class TestMultipartDecoder(unittest.TestCase):
    def test_basic_form_fields(self):
        """Test decoding of basic form fields."""
        content_type = (
            "multipart/form-data; boundary=----WebKitFormBoundaryp0mBfJEEcQtmxFCF"
        )
        body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5cDBtQmZKRUVjUXRteEZDRg0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDEiDQoNCnZhbHVlMQ0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5cDBtQmZKRUVjUXRteEZDRg0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDIiDQoNCnZhbHVlMg0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5cDBtQmZKRUVjUXRteEZDRi0tDQo="

        result = MultipartDecoder(body, content_type)
        self.assertEqual(result["field1"], "value1")
        self.assertEqual(result["field2"], "value2")

    def test_file_upload(self):
        """Test decoding of file uploads."""
        content_type = (
            "multipart/form-data; boundary=----WebKitFormBoundaryI6YbOCiSAMjU6wK2"
        )
        body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5STZZYk9DaVNBTWpVNndLMg0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWxlMSI7IGZpbGVuYW1lPSJleGFtcGxlLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQpIZWxsbywgd29ybGQhDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnlJNlliT0NpU0FNalU2d0syLS0NCg=="

        result = MultipartDecoder(body, content_type)
        self.assertTrue("file1" in result)
        self.assertTrue(isinstance(result["file1"], tuple))

        filename, content_type, data = result["file1"]
        self.assertEqual(filename, "example.txt")
        self.assertEqual(content_type, "text/plain")
        self.assertEqual(data, b"Hello, world!")

    def test_mixed_content(self):
        """Test decoding of mixed content (form fields and file uploads)."""
        content_type = (
            "multipart/form-data; boundary=----WebKitFormBoundary4AQwYOUUCEUw9hsX"
        )
        body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDEiDQoNCnZhbHVlMQ0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDIiDQoNCnZhbHVlMg0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWxlMSI7IGZpbGVuYW1lPSJleGFtcGxlLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQpIZWxsbywgd29ybGQhDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnk0QVF3WU9VVUNFVXc5aHNYLS0NCg=="

        result = MultipartDecoder(body, content_type)
        self.assertEqual(result["field1"], "value1")

        filename, content_type, data = result["file1"]
        self.assertEqual(filename, "example.txt")
        self.assertEqual(content_type, "text/plain")
        self.assertEqual(data, b"Hello, world!")

    def test_invalid_content(self):
        """Test handling of invalid content."""
        content_type = (
            "multipart/form-data; boundary=----WebKitFormBoundaryI6YbOCiSAMjU6wK2"
        )
        body = "LS0tWxsbCg=="

        with self.assertRaises(ValueError):
            MultipartDecoder(body, content_type)

    def test_missing_boundary(self):
        """Test handling of missing boundary parameter."""
        content_type = "multipart/form-data"
        body = "LS0tWxsbCg=="

        with self.assertRaises(ValueError):
            MultipartDecoder(body, content_type)


if __name__ == "__main__":
    unittest.main()
