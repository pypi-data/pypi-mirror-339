import argparse
import json
import os
import sys
import logging
from pathlib import Path
from typing import Optional

from chunktopus.utils.openai import (
    semantic_chunk_with_structured_output,
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_pptx
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def setup_parser():
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Chunktopus: A tool for document processing and semantic chunking"
    )
    
    parser.add_argument(
        "file", 
        help="Path to the file to process (PDF, DOCX, PPTX, or plain text)"
    )
    
    parser.add_argument(
        "--api-key", 
        help="OpenAI API key. If not provided, will use OPENAI_API_KEY environment variable"
    )
    
    parser.add_argument(
        "--output", 
        "-o", 
        help="Output file path (defaults to standard output)"
    )
    
    parser.add_argument(
        "--format", 
        choices=["json", "text"], 
        default="json",
        help="Output format (json or text, default: json)"
    )
    
    parser.add_argument(
        "--verbose", 
        "-v", 
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser

def process_file(file_path: str, api_key: Optional[str] = None):
    """Process a file and return chunks"""
    file_path = Path(file_path)
    
    # Check if file exists
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        sys.exit(1)
    
    # Extract text based on file type
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        text = extract_text_from_pdf(str(file_path))
    elif suffix == ".docx":
        text = extract_text_from_docx(str(file_path))
    elif suffix == ".pptx":
        text = extract_text_from_pptx(str(file_path))
    elif suffix in (".txt", ".md", ".csv", ".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        logger.error(f"Unsupported file type: {suffix}")
        sys.exit(1)
    
    # Process the text
    chunks = semantic_chunk_with_structured_output(text, api_key=api_key)
    return chunks

def main():
    """Main entry point for CLI"""
    parser = setup_parser()
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Get API key from args or environment
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    
    try:
        # Process the file
        chunks = process_file(args.file, api_key=api_key)
        
        # Prepare output
        if args.format == "json":
            output = json.dumps(chunks, indent=2)
        else:  # text format
            output = "\n\n".join([f"--- {chunk['metadata']['title']} ---\n{chunk['text']}" for chunk in chunks])
        
        # Write output
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            logger.info(f"Output written to {args.output}")
        else:
            print(output)
            
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 