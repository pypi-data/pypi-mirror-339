# Excel4RAG

A Python package for extracting tables and key-value pairs from Excel files, designed for use in RAG (Retrieval-Augmented Generation) applications.

## Features

- Extract tables from Excel documents
- Pattern-based table matching
- Key-value pair extraction
- Convert tables to pandas DataFrames
- Support for multiple tables on a single sheet
- Error handling and validation

## Installation

```bash
pip install excel4rag
```

## Usage

```python
from excel4rag import ExcelDocumentHandler

# Initialize the handler
handler = ExcelDocumentHandler("path/to/your/document.xlsx")

# Load the document
handler.load_document()

# Set a pattern to match tables (e.g., tables containing "Data")
handler.set_table_pattern(r"Data")

# Analyze the document
analysis = handler.analyze_document()

# Access extracted tables
for table in analysis.tables:
    print(f"Table ID: {table.table_id}")
    print(f"Sheet Name: {table.sheet_name}")
    print(f"Start Cell: {table.start_cell}")
    print(f"Pattern Match: {table.pattern_match}")
    print("DataFrame:")
    print(table.dataframe)

# Access key-value pairs
print("Key-Value Pairs:")
for key, value in analysis.key_values.items():
    print(f"{key}: {value}")
```

## Table Detection

The system automatically detects tables by:
1. Finding contiguous blocks of non-empty cells
2. Ensuring tables have at least 2 rows and 2 columns
3. Using the first row as column headers
4. Matching the content against the provided pattern

## Key-Value Pair Patterns

The system recognizes key-value pairs in the following formats:
- `Key: Value`
- `Key=Value`
- `Key - Value`

## Error Handling

The system includes comprehensive error handling for:
- Non-existent files
- Invalid file types
- Missing document loading
- Missing table pattern
- Table processing errors

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/excel4rag.git
cd excel4rag

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Testing

Run the test suite:
```bash
pytest
```

## License

MIT License 