"""
Excel4RAG - A Python package for extracting tables and key-value pairs from Excel files.
"""

from .excel_handler import ExcelDocumentHandler, Table, DocumentAnalysis
from .table_formatter import TableFormatter

__version__ = "0.1.0"
__all__ = ["ExcelDocumentHandler", "Table", "DocumentAnalysis", "TableFormatter"] 