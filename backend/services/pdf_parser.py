"""
PDF Parser Service - ODIN-AI verified multi-parser strategy
Uses: pdfplumber (tables) → PyMuPDF (layout) → PyPDF2 (fallback)
"""
import io
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
import pdfplumber
import fitz  # PyMuPDF
import PyPDF2
from loguru import logger


@dataclass
class PDFPage:
    """Single PDF page data"""
    page_number: int
    text: str
    tables: List[List[List[str]]]
    metadata: Dict[str, Any]


@dataclass
class PDFDocument:
    """Complete PDF document data"""
    pages: List[PDFPage]
    total_pages: int
    metadata: Dict[str, Any]
    parser_used: str


class PDFParser:
    """Multi-parser PDF extraction with auto-fallback"""

    def __init__(self):
        self.parsers = ["pdfplumber", "pymupdf", "pypdf2"]

    def parse(self, file_content: bytes, filename: str) -> PDFDocument:
        """
        Parse PDF with automatic fallback strategy

        Args:
            file_content: PDF file bytes
            filename: Original filename for logging

        Returns:
            PDFDocument with extracted content
        """
        for parser_name in self.parsers:
            try:
                logger.info(f"Attempting to parse {filename} with {parser_name}")

                if parser_name == "pdfplumber":
                    result = self._parse_with_pdfplumber(file_content)
                elif parser_name == "pymupdf":
                    result = self._parse_with_pymupdf(file_content)
                else:  # pypdf2
                    result = self._parse_with_pypdf2(file_content)

                logger.success(f"Successfully parsed {filename} with {parser_name}")
                return result

            except Exception as e:
                logger.warning(f"{parser_name} failed for {filename}: {str(e)}")
                continue

        raise ValueError(f"All parsers failed to parse {filename}")

    def _parse_with_pdfplumber(self, file_content: bytes) -> PDFDocument:
        """Parse with pdfplumber (best for tables)"""
        pages_data = []

        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            metadata = pdf.metadata or {}

            for page_num, page in enumerate(pdf.pages, start=1):
                # Extract text
                text = page.extract_text() or ""

                # Extract tables
                tables = []
                extracted_tables = page.extract_tables()
                if extracted_tables:
                    tables = extracted_tables

                # Page metadata
                page_metadata = {
                    "width": page.width,
                    "height": page.height,
                    "rotation": getattr(page, "rotation", 0)
                }

                pages_data.append(PDFPage(
                    page_number=page_num,
                    text=text,
                    tables=tables,
                    metadata=page_metadata
                ))

        return PDFDocument(
            pages=pages_data,
            total_pages=len(pages_data),
            metadata=metadata,
            parser_used="pdfplumber"
        )

    def _parse_with_pymupdf(self, file_content: bytes) -> PDFDocument:
        """Parse with PyMuPDF/fitz (best for layout)"""
        pages_data = []

        doc = fitz.open(stream=file_content, filetype="pdf")
        metadata = doc.metadata

        for page_num in range(len(doc)):
            page = doc[page_num]

            # Extract text with layout preservation
            text = page.get_text("text")

            # Extract tables (basic)
            tables = []
            try:
                tabs = page.find_tables()
                if tabs:
                    for table in tabs:
                        tables.append(table.extract())
            except Exception as e:
                logger.debug(f"Table extraction failed on page {page_num + 1}: {e}")

            # Page metadata
            page_metadata = {
                "width": page.rect.width,
                "height": page.rect.height,
                "rotation": page.rotation
            }

            pages_data.append(PDFPage(
                page_number=page_num + 1,
                text=text,
                tables=tables,
                metadata=page_metadata
            ))

        doc.close()

        return PDFDocument(
            pages=pages_data,
            total_pages=len(pages_data),
            metadata=metadata,
            parser_used="pymupdf"
        )

    def _parse_with_pypdf2(self, file_content: bytes) -> PDFDocument:
        """Parse with PyPDF2 (fallback)"""
        pages_data = []

        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        metadata = pdf_reader.metadata or {}

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]

            # Extract text
            text = page.extract_text()

            # PyPDF2 doesn't extract tables well
            tables = []

            # Page metadata
            page_metadata = {
                "rotation": page.get("/Rotate", 0)
            }

            pages_data.append(PDFPage(
                page_number=page_num + 1,
                text=text,
                tables=tables,
                metadata=page_metadata
            ))

        return PDFDocument(
            pages=pages_data,
            total_pages=len(pages_data),
            metadata=metadata,
            parser_used="pypdf2"
        )

    def to_markdown(self, document: PDFDocument) -> str:
        """
        Convert PDFDocument to Markdown format

        Args:
            document: Parsed PDF document

        Returns:
            Markdown formatted string
        """
        markdown_parts = []

        # Document metadata header
        if document.metadata:
            markdown_parts.append("---")
            for key, value in document.metadata.items():
                if value:
                    markdown_parts.append(f"{key}: {value}")
            markdown_parts.append("---\n")

        # Process each page
        for page in document.pages:
            markdown_parts.append(f"# Page {page.page_number}\n")

            # Add text content
            if page.text:
                markdown_parts.append(page.text.strip())
                markdown_parts.append("")  # Empty line

            # Add tables
            if page.tables:
                for table_idx, table in enumerate(page.tables, start=1):
                    markdown_parts.append(f"\n**Table {table_idx}:**\n")
                    markdown_parts.append(self._table_to_markdown(table))
                    markdown_parts.append("")

            markdown_parts.append("\n---\n")  # Page separator

        return "\n".join(markdown_parts)

    def _table_to_markdown(self, table: List[List[str]]) -> str:
        """Convert table to Markdown table format"""
        if not table:
            return ""

        lines = []

        # Header row
        if table:
            header = table[0]
            lines.append("| " + " | ".join(str(cell or "") for cell in header) + " |")
            lines.append("| " + " | ".join("---" for _ in header) + " |")

            # Data rows
            for row in table[1:]:
                lines.append("| " + " | ".join(str(cell or "") for cell in row) + " |")

        return "\n".join(lines)


# Singleton instance
pdf_parser = PDFParser()
