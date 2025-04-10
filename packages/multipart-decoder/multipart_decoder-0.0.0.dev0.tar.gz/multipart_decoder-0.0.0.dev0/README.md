# multipart_decoder

A lightweight Python package for parsing multipart/form-data content.

## Installation

```bash
pip install multipart-decoder
```


**Basic Usage Example for multipart_decoder**

This example demonstrates how to parse simple form data with text fields.

```python

from multipart_decoder import MultipartFormParser

# Example with raw form data
def basic_form_parsing():
    # In a real application, these would come from an HTTP request
    content_type = "multipart/form-data; boundary=----WebKitFormBoundarydVTl2EAp1scXYsWZ"
    body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5ZFZUbDJFQXAxc2NYWXNXWg0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJ1c2VybmFtZSINCg0KZXhhbXBsZV91c2VyDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnlkVlRsMkVBcDFzY1hZc1daDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImVtYWlsIg0KDQp1c2VyQGV4YW1wbGUuY29tDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnlkVlRsMkVBcDFzY1hZc1daLS0NCg=="

    # Parse the multipart form data
    form_data = MultipartFormParser(body, content_type)

    # Access the form fields
    print(f"Username: {form_data['fields']['username']}")
    print(f"Email: {form_data['fields']['email']}")

    # Show the entire parsed data structure
    print("\nComplete form data dictionary:")
    print(form_data)

if __name__ == "__main__":
    basic_form_parsing()

```
## Expected Output

### Basic Form Parsing:
- **Username**: `example_user`
- **Email**: `user@example.com`

#### Complete Form Data Dictionary:
```json
{
    "fields": {
        "username": "example_user",
        "email": "user@example.com"
    },
    "files": {}
}

```


**File Upload Example for multipart_decoder**

This example demonstrates how to handle file uploads in multipart form data.

```python
from multipart_decoder import MultipartFormParser
import os

def process_file_upload():
    content_type = "multipart/form-data; boundary=----WebKitFormBoundary4AQwYOUUCEUw9hsX"
    body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDEiDQoNCnZhbHVlMQ0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDIiDQoNCnZhbHVlMg0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWxlMSI7IGZpbGVuYW1lPSJleGFtcGxlLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQpIZWxsbywgd29ybGQhDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnk0QVF3WU9VVUNFVXc5aHNYLS0NCg=="

    form_data = MultipartFormParser(body, content_type)

    # Access fields
    print(f"Field 1: {form_data['fields']['field1']}")
    print(f"Field 2: {form_data['fields']['field2']}")

    # Access files
    if 'file1' in form_data['files']:
        file_info = form_data['files']['file1']
        print(f"  - Filename: {file_info['filename']}")
        print(f"  - Content type: {file_info['content_type']}")
        print(f"  - File size: {file_info['size']} bytes")

        # Example: save the file
        save_path = f"saved_{file_info['filename']}"
        with open(save_path, "wb") as f:
            f.write(file_info['content'])
        print(f"  - File saved to: {save_path}")

        # Cleanup (for demonstration)
        os.remove(save_path)

if __name__ == "__main__":
    process_file_upload()

```
# Expected Output:

### Test Fields:
- **Field 1**: `value1`
- **Field 2**: `value2`

### File Field:
- **Filename**: `example.txt`
- **Content Type**: `text/plain`
- **File Size**: `13 bytes`
- **File Saved To**: `saved_example.txt`
