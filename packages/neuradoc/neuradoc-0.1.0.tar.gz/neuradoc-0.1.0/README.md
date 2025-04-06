# NeuraDoc

[![PyPI version](https://img.shields.io/pypi/v/neuradoc.svg)](https://pypi.org/project/neuradoc/)
[![Python Version](https://img.shields.io/pypi/pyversions/neuradoc.svg)](https://pypi.org/project/neuradoc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

NeuraDoc is a Python package for parsing and transforming various document formats into LLM-ready data with element classification capabilities. The library intelligently extracts and classifies content from documents for AI/ML workflows.

## Features

- **Multi-format Support**: Parse at least 10 different document types (PDF, Word, TXT, etc.)
- **Element Extraction**: Extract text, images, tables, and diagrams from documents
- **Classification**: Classify document elements by type
- **Smart Positioning**: Position and organize extracted elements intelligently
- **LLM Integration**: Convert extracted data to LLM-ready formats (tokenized structures)
- **Memory Efficiency**: Optimized for processing large documents

## Supported Document Formats

NeuraDoc supports the following document formats:

- PDF (`.pdf`)
- Microsoft Word (`.docx`, `.doc`)
- Plain Text (`.txt`)
- Microsoft Excel (`.xlsx`, `.xls`)
- HTML (`.html`, `.htm`)
- XML (`.xml`)
- Images (`.jpg`, `.jpeg`, `.png`, `.gif`)
- Microsoft PowerPoint (`.pptx`, `.ppt`)
- CSV (`.csv`)
- JSON (`.json`)
- Markdown (`.md`)

## Installation

### Basic Installation

```bash
pip install neuradoc
```

### Installation with Optional Dependencies

```bash
# Install with OCR support
pip install neuradoc[ocr]

# Install with advanced table extraction
pip install neuradoc[tables]

# Install with NLP capabilities
pip install neuradoc[nlp]

# Install with transformer model support
pip install neuradoc[transformers]

# Install with web interface
pip install neuradoc[web]

# Install with all optional dependencies
pip install neuradoc[ocr,tables,nlp,transformers,web]
```

## Quick Start

### Basic Usage

```python
import neuradoc

# Load and parse a document
doc = neuradoc.load_document("path/to/your/document.pdf")

# Get all text content
text = doc.get_text_content()

# Get tables
tables = doc.get_tables()

# Get images
images = doc.get_images()

# Save extracted content in different formats
doc.save("output.json", format="json")
doc.save("output.md", format="markdown")
doc.save("output.txt", format="text")
```

### Advanced Usage

```python
import neuradoc
from neuradoc.models.element import ElementType
from neuradoc.transformers.llm_transformer import chunk_document

# Load document
doc = neuradoc.load_document("document.docx")

# Filter elements by type
headings = doc.get_elements_by_type(ElementType.HEADING)
code_blocks = doc.get_elements_by_type(ElementType.CODE)

# Transform document into chunks for LLM processing
chunks = chunk_document(doc, max_chunk_size=1000, overlap=100)

# Process chunks with your LLM
for chunk in chunks:
    # Process each chunk with your LLM implementation
    print(f"Chunk: {len(chunk)} characters")
```

## Web Interface

NeuraDoc includes a web interface for document processing:

```bash
# Install web dependencies
pip install neuradoc[web]

# Run the web server
python -m neuradoc.web.app
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
