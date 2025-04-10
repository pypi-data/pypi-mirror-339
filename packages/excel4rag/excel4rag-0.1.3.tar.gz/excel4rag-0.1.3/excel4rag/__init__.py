"""
Excel4RAG - A Python package for extracting tables and key-value pairs from Excel files.
"""

from .excel_handler import ExcelDocumentHandler, Table, DocumentAnalysis
from .table_formatter import TableFormatter
from typing import List, Optional

__version__ = "0.1.3"
__all__ = ["ExcelDocumentHandler", "Table", "DocumentAnalysis", "TableFormatter", "excel_to_json", "excel_to_jsonl", "excel_to_html", "excel_to_markdown"]

def _setup_handler(filename: str, table_ids: Optional[List[str]] = None) -> ExcelDocumentHandler:
    """Helper function to set up the handler with default settings.
    
    Args:
        filename: Path to the Excel file
        table_ids: Optional list of table IDs to extract
    """
    handler = ExcelDocumentHandler(filename)
    handler.load_document()
    # Set a pattern that matches all tables
    handler.set_table_pattern(r".*")
    return handler

def _filter_tables(tables: List[Table], table_ids: Optional[List[str]] = None) -> List[Table]:
    """Filter tables by their IDs.
    
    Args:
        tables: List of tables to filter
        table_ids: Optional list of table IDs to keep
        
    Returns:
        Filtered list of tables
    """
    if table_ids is None:
        return tables
    return [table for table in tables if table.table_id in table_ids]

def excel_to_json(filename: str, output_path: str = None, table_ids: Optional[List[str]] = None) -> str:
    """Convert Excel file tables to JSON format.
    
    Args:
        filename: Path to the Excel file
        output_path: Optional path to save the JSON file
        table_ids: Optional list of table IDs to extract
        
    Returns:
        JSON string representation of the tables
    """
    handler = _setup_handler(filename)
    tables = handler.extract_tables()
    filtered_tables = _filter_tables(tables, table_ids)
    return TableFormatter.to_json(filtered_tables, output_path)

def excel_to_jsonl(filename: str, output_path: str = None, table_ids: Optional[List[str]] = None) -> str:
    """Convert Excel file tables to JSONL format (one JSON object per line).
    
    Args:
        filename: Path to the Excel file
        output_path: Optional path to save the JSONL file
        table_ids: Optional list of table IDs to extract
        
    Returns:
        JSONL string representation of the tables
    """
    handler = _setup_handler(filename)
    tables = handler.extract_tables()
    filtered_tables = _filter_tables(tables, table_ids)
    return TableFormatter.to_jsonl(filtered_tables, output_path)

def excel_to_html(filename: str, output_path: str = None, table_ids: Optional[List[str]] = None) -> str:
    """Convert Excel file tables to HTML format.
    
    Args:
        filename: Path to the Excel file
        output_path: Optional path to save the HTML file
        table_ids: Optional list of table IDs to extract
        
    Returns:
        HTML string representation of the tables
    """
    handler = _setup_handler(filename)
    tables = handler.extract_tables()
    filtered_tables = _filter_tables(tables, table_ids)
    return TableFormatter.to_html(filtered_tables, output_path)

def excel_to_markdown(filename: str, output_path: str = None, table_ids: Optional[List[str]] = None) -> str:
    """Convert Excel file tables to Markdown format.
    
    Args:
        filename: Path to the Excel file
        output_path: Optional path to save the Markdown file
        table_ids: Optional list of table IDs to extract
        
    Returns:
        Markdown string representation of the tables
    """
    handler = _setup_handler(filename)
    tables = handler.extract_tables()
    filtered_tables = _filter_tables(tables, table_ids)
    return TableFormatter.to_markdown(filtered_tables, output_path) 