from typing import List, Dict, Any, Optional
import json
import pandas as pd
from pathlib import Path
from .excel_handler import Table

class TableFormatter:
    """A class to format tables into various output formats."""
    
    @staticmethod
    def _table_to_dict(table: Table) -> Dict[str, Any]:
        """Convert a table to a dictionary format."""
        return {
            "table_id": table.table_id,
            "sheet_name": table.sheet_name,
            "start_cell": table.start_cell,
            "pattern_match": table.pattern_match,
            "data": table.dataframe.to_dict(orient='records')
        }
    
    @staticmethod
    def to_json(tables: List[Table], output_path: Optional[str] = None) -> str:
        """Convert tables to JSON format.
        
        Args:
            tables: List of Table objects to convert
            output_path: Optional path to save the JSON file
            
        Returns:
            JSON string representation of the tables
        """
        result = [TableFormatter._table_to_dict(table) for table in tables]
        json_str = json.dumps(result, indent=2)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str
    
    @staticmethod
    def to_jsonl(tables: List[Table], output_path: Optional[str] = None) -> str:
        """Convert tables to JSONL format (one JSON object per line).
        
        Args:
            tables: List of Table objects to convert
            output_path: Optional path to save the JSONL file
            
        Returns:
            JSONL string representation of the tables
        """
        result = [TableFormatter._table_to_dict(table) for table in tables]
        jsonl_str = '\n'.join(json.dumps(item) for item in result)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(jsonl_str)
        
        return jsonl_str
    
    @staticmethod
    def to_html(tables: List[Table], output_path: Optional[str] = None) -> str:
        """Convert tables to HTML format.
        
        Args:
            tables: List of Table objects to convert
            output_path: Optional path to save the HTML file
            
        Returns:
            HTML string representation of the tables
        """
        html_parts = ['<html><head><style>table {border-collapse: collapse; width: 100%;} th, td {border: 1px solid black; padding: 8px; text-align: left;}</style></head><body>']
        
        for table in tables:
            html_parts.append(f'<h2>Table: {table.table_id}</h2>')
            html_parts.append(f'<p>Sheet: {table.sheet_name}, Start Cell: {table.start_cell}</p>')
            html_parts.append(table.dataframe.to_html())
            html_parts.append('<hr>')
        
        html_parts.append('</body></html>')
        html_str = '\n'.join(html_parts)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_str)
        
        return html_str
    
    @staticmethod
    def to_markdown(tables: List[Table], output_path: Optional[str] = None) -> str:
        """Convert tables to Markdown format.
        
        Args:
            tables: List of Table objects to convert
            output_path: Optional path to save the Markdown file
            
        Returns:
            Markdown string representation of the tables
        """
        md_parts = []
        
        for table in tables:
            md_parts.append(f'## Table: {table.table_id}')
            md_parts.append(f'**Sheet:** {table.sheet_name}, **Start Cell:** {table.start_cell}')
            md_parts.append('')
            md_parts.append(table.dataframe.to_markdown())
            md_parts.append('')
        
        md_str = '\n'.join(md_parts)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_str)
        
        return md_str 