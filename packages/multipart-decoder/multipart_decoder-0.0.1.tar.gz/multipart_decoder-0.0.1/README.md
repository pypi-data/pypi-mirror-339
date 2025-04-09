# multipart_decoder

A lightweight Python package for decoding multipart/form-data content.

## Installation

```bash
pip install multipart-decoder
```


**Basic Usage Example for multipart_decoder**

This example demonstrates how to parse simple form data with text fields.

```python

from multipart_decoder import MultipartDecoder

# Example with raw form data
def basic_form_parsing():
    # In a real application, these would come from an HTTP request
    content_type = "multipart/form-data; boundary=----WebKitFormBoundarydVTl2EAp1scXYsWZ"
    body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5ZFZUbDJFQXAxc2NYWXNXWg0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJ1c2VybmFtZSINCg0KZXhhbXBsZV91c2VyDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnlkVlRsMkVBcDFzY1hZc1daDQpDb250ZW50LURpc3Bvc2l0aW9uOiBmb3JtLWRhdGE7IG5hbWU9ImVtYWlsIg0KDQp1c2VyQGV4YW1wbGUuY29tDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnlkVlRsMkVBcDFzY1hZc1daLS0NCg=="

    # Parse the multipart form data
    form_data = MultipartDecoder(body, content_type)
    
    # Access the form fields
    print(f"Username: {form_data['username']}")
    print(f"Email: {form_data['email']}")
    
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
    "username": "example_user",
    "email": "user@example.com"
}
```


**File Upload Example for multipart_decoder**

This example demonstrates how to handle file uploads in multipart form data.

```python
from multipart_decoder import MultipartDecoder
import os

def process_file_upload():
    """Process an example multipart form with file uploads."""
    content_type = (
            "multipart/form-data; boundary=----WebKitFormBoundary4AQwYOUUCEUw9hsX"
        )
    body = "LS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDEiDQoNCnZhbHVlMQ0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWVsZDIiDQoNCnZhbHVlMg0KLS0tLS0tV2ViS2l0Rm9ybUJvdW5kYXJ5NEFRd1lPVVVDRVV3OWhzWA0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJmaWxlMSI7IGZpbGVuYW1lPSJleGFtcGxlLnR4dCINCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFpbg0KDQpIZWxsbywgd29ybGQhDQotLS0tLS1XZWJLaXRGb3JtQm91bmRhcnk0QVF3WU9VVUNFVXc5aHNYLS0NCg=="

    form_data = MultipartDecoder(body, content_type)
    # Process regular form field
    print(f"Field 1: {form_data['field1']}")
    print(f"Field 2: {form_data['field2']}")

    # Process file uploads
    if 'file1' in form_data:
        filename, content_type, file_data = form_data['file1']
        print(f"  - Filename: {filename}")
        print(f"  - Content type: {content_type}")
        print(f"  - File size: {len(file_data)} bytes")

        # Example: save the file
        save_path = f"saved_{filename}"
        with open(save_path, "wb") as f:
            f.write(file_data)
        print(f"  - File saved to: {save_path}")

        # # After using the file, delete it for this example
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
