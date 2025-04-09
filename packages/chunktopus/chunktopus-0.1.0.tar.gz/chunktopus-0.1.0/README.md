# Chunktopus

A powerful document processing and chunking API by Unsiloed AI, featuring multithreaded OCR and intelligent document chunking using OpenAI's Vision models.

## Installation

```bash
pip install chunktopus
```

## Features

- Process PDF, DOCX, and PPTX documents
- Multiple chunking strategies:
  - Fixed size chunks
  - Semantic chunks (using OpenAI)
  - Page-based chunks
  - Paragraph-based chunks
  - Heading-based chunks
- Fast parallel processing
- RESTful API with FastAPI

## Configuration

### OpenAI API Key

**Important:** This package requires your own OpenAI API key. You must provide your API key in one of the following ways:

1. Set it as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key"
```

2. Create a .env file in your project directory:
```
OPENAI_API_KEY=your-api-key
```

3. Set it programmatically:
```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"
```

## Usage

### Using as a Python Package

```python
from chunktopus import chunktopus

# Process a document with your own OpenAI API key
result = chunktopus(
    file_path="path/to/document.pdf",
    credentials={"api_key": "your-openai-api-key"}
)

# Or process a document from a URL
result = chunktopus(
    file_path="https://example.com/document.pdf",
    credentials={"api_key": "your-openai-api-key"}
)

# Or process raw text
result = chunktopus(
    text="Your text content to chunk semantically...",
    credentials={"api_key": "your-openai-api-key"}
)

# Print the results
for i, chunk in enumerate(result):
    print(f"Chunk {i+1}: {chunk['text'][:100]}...")
```

### Using from Command Line

After installation, you can use the `chunktopus` command:

```bash
# Process a file with your OpenAI API key
chunktopus path/to/document.pdf --api-key "your-openai-api-key"

# Output to a file
chunktopus path/to/document.pdf --api-key "your-openai-api-key" --output results.json

# Format as text instead of JSON
chunktopus path/to/document.pdf --api-key "your-openai-api-key" --format text
```

### Running as a REST API

```python
from chunktopus.server import run_server

# Start the server on port 8000
run_server(port=8000)
```

### Using the document processing functions directly

```python
from chunktopus.services import process_document_chunking
from chunktopus.utils.chunking import ChunkingStrategy

# Set your OpenAI API key
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"

# Process a document with semantic chunking
result = process_document_chunking(
    file_path="path/to/document.pdf",
    file_type="pdf",
    strategy=ChunkingStrategy.SEMANTIC,
)

# Print the results
print(f"Number of chunks: {result['total_chunks']}")
for i, chunk in enumerate(result['chunks']):
    print(f"Chunk {i+1}: {chunk['text'][:100]}...")
```

## API Endpoints

### `/chunking`

POST endpoint that processes a document and returns chunks.

**Parameters:**
- `document_file`: The document file (PDF, DOCX, PPTX)
- `strategy`: Chunking strategy (semantic, fixed, page, paragraph, heading)
- `chunk_size`: Size of chunks for fixed strategy (default: 1000)
- `overlap`: Overlap size for fixed strategy (default: 100)

## License

MIT License 