# App package

# Package initialization
from typing import Dict, List, Any, Optional, Union
import os

from chunktopus.utils.openai import (
    semantic_chunk_with_structured_output,
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_pptx
)

__version__ = "0.1.0"

def chunktopus(
    file_path: str = None, 
    text: str = None,
    credentials: Dict[str, str] = None
) -> List[Dict[str, Any]]:
    """
    Process a document or text and return semantic chunks.
    
    Args:
        file_path: Path to the file to process (local path or URL)
        text: Raw text to process (alternative to file_path)
        credentials: Dictionary containing authentication credentials
                    Example: {"api_key": "your-openai-api-key"}
                    
    Returns:
        List of chunks with metadata
    """
    if not file_path and not text:
        raise ValueError("Either file_path or text must be provided")
    
    if file_path and text:
        raise ValueError("Provide either file_path or text, not both")
    
    # Extract API key from credentials
    api_key = None
    if credentials and "api_key" in credentials:
        api_key = credentials["api_key"]
    
    # Process file if path is provided
    if file_path:
        import pathlib
        
        # Check if it's a URL
        if file_path.startswith(("http://", "https://")):
            import requests
            from tempfile import NamedTemporaryFile
            import os
            
            # Download the file
            response = requests.get(file_path)
            response.raise_for_status()
            
            # Get file extension from URL
            ext = os.path.splitext(file_path)[1].lower()
            
            # Create a temporary file with the correct extension
            with NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name
            
            try:
                # Process the downloaded file
                file_path = temp_path
            finally:
                # Clean up the temporary file later
                pass
        
        # Get file extension
        file_suffix = pathlib.Path(file_path).suffix.lower()
        
        # Extract text based on file type
        if file_suffix == ".pdf":
            text = extract_text_from_pdf(file_path)
        elif file_suffix == ".docx":
            text = extract_text_from_docx(file_path)
        elif file_suffix == ".pptx":
            text = extract_text_from_pptx(file_path)
        elif file_suffix in (".txt", ".md", ".csv", ".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            raise ValueError(f"Unsupported file type: {file_suffix}")
    
    # Process the text
    return semantic_chunk_with_structured_output(text, api_key=api_key)
