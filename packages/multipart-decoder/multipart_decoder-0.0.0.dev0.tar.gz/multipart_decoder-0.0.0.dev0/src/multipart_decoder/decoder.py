"""
Decoder module for parsing multipart/form-data content.
"""

import re
import logging
from base64 import b64decode
from binascii import Error as BinasciiError
from requests_toolbelt.multipart import decoder


def MultipartFormParser(body, content_type):
    """
    Decode a multipart/form-data request body.
    :param body: The body of the request, typically a byte string.
    :param content_type: The content type of the request, typically 'multipart/form-data; boundary=...'.
    :return: A dictionary containing the extracted fields and files.
    :raises ValueError: If input parameters are invalid
    :raises Exception: For various parsing errors
    """
    extracted_data = {"fields": {}, "files": {}}
    
    # Validate input parameters
    if not body:
        raise ValueError("Request body cannot be empty")
    if not content_type or 'boundary=' not in content_type:
        raise ValueError("Invalid content type: must be multipart/form-data with boundary")
    
    try:
        # Decode the base64 encoded body
        try:
            data = b64decode(body)
        except BinasciiError as e:
            raise ValueError(f"Invalid base64 encoded body: {str(e)}")
            
        # Parse multipart data
        try:
            multipart_data = decoder.MultipartDecoder(data, content_type)
        except Exception as e:
            raise ValueError(f"Failed to decode multipart form data: {str(e)}")
        
        # Process parts
        for part in multipart_data.parts:
            try:
                # Get content disposition header
                if b"Content-Disposition" not in part.headers:
                    logging.warning("Skipping part without Content-Disposition header")
                    continue
                    
                content_disposition = part.headers[b"Content-Disposition"].decode()
                
                # Extract the field name
                name_match = re.search(r'name="([^"]+)"', content_disposition)
                if not name_match:
                    logging.warning("Skipping part without field name")
                    continue
                    
                field_name = name_match.group(1)
                
                # Check if it's a file
                filename_match = re.search(r'filename="([^"]+)"', content_disposition)
                
                if filename_match:
                    # Handle file upload
                    filename = filename_match.group(1)
                    content_type = part.headers.get(
                        b"Content-Type", b"application/octet-stream"
                    ).decode()
                    file_data = part.content
                    
                    # Store file information
                    extracted_data["files"][field_name] = {
                        "filename": filename,
                        "content_type": content_type,
                        "content": file_data,
                        "size": len(file_data),
                    }
                else:
                    # Handle regular form fields
                    try:
                        field_value = part.text.strip()
                    except UnicodeDecodeError:
                        logging.warning(f"Could not decode text for field {field_name}, storing as binary")
                        field_value = part.content
                    extracted_data["fields"][field_name] = field_value
                    
            except Exception as e:
                logging.error(f"Error processing part: {str(e)}")
                # Continue processing other parts instead of failing completely
    
    except Exception as e:
        # Re-raise with more context
        raise Exception(f"Failed to parse multipart form data: {str(e)}") from e
        
    return extracted_data
