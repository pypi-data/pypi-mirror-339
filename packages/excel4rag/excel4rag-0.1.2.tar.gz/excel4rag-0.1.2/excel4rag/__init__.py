"""
Excel4RAG - A Python package for extracting tables and key-value pairs from Excel files.
"""

from .excel_handler import ExcelDocumentHandler, Table, DocumentAnalysis
from .table_formatter import TableFormatter

__version__ = "0.1.2"
__all__ = ["ExcelDocumentHandler", "Table", "DocumentAnalysis", "TableFormatter", "excel_to_json", "excel_to_jsonl", "excel_to_html", "excel_to_markdown"]

def _setup_handler(filename: str) -> ExcelDocumentHandler:
    """Helper function to set up the handler with default settings."""
    handler = ExcelDocumentHandler(filename)
    handler.load_document()
    # Set a pattern that matches all tables
    handler.set_table_pattern(r".*")
    return handler

def excel_to_json(filename: str, output_path: str = None) -> str:
    """Convert Excel file tables to JSON format.
    
    Args:
        filename: Path to the Excel file
        output_path: Optional path to save the JSON file
        
    Returns:
        JSON string representation of the tables
    """
    handler = _setup_handler(filename)
    tables = handler.extract_tables()
    return TableFormatter.to_json(tables, output_path)

def excel_to_jsonl(filename: str, output_path: str = None) -> str:
    """Convert Excel file tables to JSONL format (one JSON object per line).
    
    Args:
        filename: Path to the Excel file
        output_path: Optional path to save the JSONL file
        
    Returns:
        JSONL string representation of the tables
    """
    handler = _setup_handler(filename)
    tables = handler.extract_tables()
    return TableFormatter.to_jsonl(tables, output_path)

def excel_to_html(filename: str, output_path: str = None) -> str:
    """Convert Excel file tables to HTML format.
    
    Args:
        filename: Path to the Excel file
        output_path: Optional path to save the HTML file
        
    Returns:
        HTML string representation of the tables
    """
    handler = _setup_handler(filename)
    tables = handler.extract_tables()
    return TableFormatter.to_html(tables, output_path)

def excel_to_markdown(filename: str, output_path: str = None) -> str:
    """Convert Excel file tables to Markdown format.
    
    Args:
        filename: Path to the Excel file
        output_path: Optional path to save the Markdown file
        
    Returns:
        Markdown string representation of the tables
    """
    handler = _setup_handler(filename)
    tables = handler.extract_tables()
    return TableFormatter.to_markdown(tables, output_path) 