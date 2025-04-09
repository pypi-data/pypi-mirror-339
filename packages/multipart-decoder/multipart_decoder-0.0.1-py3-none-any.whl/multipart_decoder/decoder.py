"""
Decoder module for parsing multipart/form-data content.
"""

import re
import base64
import email.parser
from io import BytesIO
from email.policy import default


def MultipartDecoder(content_bytes, content_type):
    """
    Decode multipart form-data from bytes content.
    
    Args:
        content_bytes (bytes): The raw multipart form-data content
        content_type (str): The Content-Type header value (must include boundary)
    
    Returns:
        dict: A dictionary where keys are field names and values are either:
             - strings for regular form fields
             - tuples of (filename, content_type, data) for file uploads
             
    Raises:
        ValueError: If the content is not multipart or lacks required headers
    """
    if not content_type or 'boundary=' not in content_type:
        raise ValueError("Content-Type header must include a boundary parameter")

    try:
        content_bytes = base64.b64decode(content_bytes)
    except (base64.binascii.Error, TypeError) as e:
        raise ValueError("Failed to decode base64 content") from e
    # Prepare the content with proper headers for the email parser
    content = BytesIO()
    content.write(b'Content-Type: ' + content_type.encode('utf-8') + b'\r\n\r\n')
    content.write(content_bytes)
    content.seek(0)

    # Parse the multipart content
    parser = email.parser.BytesParser(policy=default)
    message = parser.parse(content)

    if not message.is_multipart():
        raise ValueError("Content is not multipart")

    form_data = {}

    # Process each part of the multipart message
    for part in message.get_payload():
        # Get the Content-Disposition header to extract field name and filename
        content_disposition = part.get("Content-Disposition", "")
        # Use regex to extract field name from content disposition
        name_match = re.search(r'name="([^"]*)"', content_disposition)

        if name_match:
            field_name = name_match.group(1)
            filename_match = re.search(r'filename="([^"]*)"', content_disposition)

            if filename_match:
                # This is a file upload
                filename = filename_match.group(1)
                part_content_type = part.get_content_type()
                data = part.get_payload(decode=True)  # Binary file content
                form_data[field_name] = (filename, part_content_type, data)
            else:
                # This is a regular form field
                form_data[field_name] = part.get_payload(decode=True).decode(part.get_content_charset('utf-8'))

    return form_data
