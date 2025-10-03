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
class PDFImage:
    """Single PDF image data"""
    image_index: int  # 페이지 내 이미지 순서
    image_bytes: bytes  # 이미지 바이너리 데이터
    image_type: str  # PNG, JPEG 등
    width: int
    height: int
    position_x: float
    position_y: float
    bbox: tuple  # (x0, y0, x1, y1)


@dataclass
class PDFPage:
    """Single PDF page data"""
    page_number: int
    text: str
    tables: List[List[List[str]]]
    images: List[PDFImage]  # 이미지 리스트 추가
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
        # PyMuPDF를 먼저 시도 (이미지 추출 지원)
        self.parsers = ["pymupdf", "pdfplumber", "pypdf2"]

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
                    images=[],  # pdfplumber는 이미지 추출 미지원
                    metadata=page_metadata
                ))

        return PDFDocument(
            pages=pages_data,
            total_pages=len(pages_data),
            metadata=metadata,
            parser_used="pdfplumber"
        )

    def _parse_with_pymupdf(self, file_content: bytes) -> PDFDocument:
        """Parse with PyMuPDF/fitz (best for layout and images)"""
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

            # Extract images with position info
            images = []

            # Method 1: Try to get image positions from page dict
            page_dict = page.get_text("dict")
            image_positions = {}  # Map xref -> bbox

            for block in page_dict.get("blocks", []):
                if block.get("type") == 1:  # Image block
                    xref = block.get("number")
                    bbox = block.get("bbox")  # (x0, y0, x1, y1)
                    if xref and bbox:
                        image_positions[xref] = bbox

            # Method 2: Parse page content stream for image transformation matrices
            # This handles Form XObjects and images rendered via Do operator
            try:
                # Get all image instances with their transformation matrices
                for item in page.get_image_info():
                    xref = item.get("xref")
                    bbox = item.get("bbox")  # Already has the bbox!
                    if xref and bbox:
                        image_positions[xref] = bbox
                        logger.debug(f"Got image position from get_image_info: xref={xref}, bbox={bbox}")
            except Exception as e:
                logger.debug(f"get_image_info failed: {e}")

            # Now extract image data
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]  # Image reference number

                    # First check if image is actually rendered on this page
                    # get_image_rects returns empty list if image is not rendered
                    img_rects = page.get_image_rects(xref)
                    if not img_rects:
                        # Image is referenced but not rendered on this page - skip it
                        logger.debug(f"Skipping image xref={xref} (not rendered on page {page_num + 1})")
                        continue

                    # Extract image data
                    img_info = doc.extract_image(xref)
                    image_bytes = img_info["image"]
                    image_ext = img_info["ext"]  # png, jpeg 등

                    # Get image position from page_dict first
                    if xref in image_positions:
                        bbox = image_positions[xref]
                        position_x = bbox[0]  # x0
                        position_y = bbox[1]  # y0
                        img_width = bbox[2] - bbox[0]  # x1 - x0
                        img_height = bbox[3] - bbox[1]  # y1 - y0
                        logger.debug(f"Found position for image {img_index} xref={xref}: ({position_x:.1f}, {position_y:.1f})")
                    else:
                        # Use get_image_rects (we already checked it's not empty)
                        rect = img_rects[0]
                        position_x = rect.x0
                        position_y = rect.y0
                        img_width = rect.width
                        img_height = rect.height
                        logger.debug(f"Got position from get_image_rects for {img_index}")

                    bbox = (position_x, position_y, position_x + img_width, position_y + img_height)

                    # Use rendered size (bbox size), not intrinsic image size
                    # This ensures the image displays at the correct size in the PDF
                    images.append(PDFImage(
                        image_index=img_index,
                        image_bytes=image_bytes,
                        image_type=image_ext.upper(),
                        width=int(img_width),  # Rendered width from bbox
                        height=int(img_height),  # Rendered height from bbox
                        position_x=position_x,
                        position_y=position_y,
                        bbox=bbox
                    ))

                    logger.debug(
                        f"Extracted image {img_index} from page {page_num + 1}: "
                        f"{img_info['width']}x{img_info['height']} {image_ext} "
                        f"at ({position_x:.1f}, {position_y:.1f})"
                    )

                except Exception as e:
                    logger.warning(f"Failed to extract image {img_index} from page {page_num + 1}: {e}")
                    continue

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
                images=images,
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
                images=[],  # PyPDF2는 이미지 추출 미지원
                metadata=page_metadata
            ))

        return PDFDocument(
            pages=pages_data,
            total_pages=len(pages_data),
            metadata=metadata,
            parser_used="pypdf2"
        )

    def to_markdown(self, document: PDFDocument, include_metadata: bool = False, include_images: bool = True) -> str:
        """
        Convert PDFDocument to Markdown format

        Args:
            document: Parsed PDF document
            include_metadata: Whether to include metadata in output (default: False for translation)
            include_images: Whether to include image placeholders (default: True)

        Returns:
            Markdown formatted string
        """
        markdown_parts = []

        # Document metadata header (optional, excluded by default for cleaner translation)
        if include_metadata and document.metadata:
            markdown_parts.append("---")
            for key, value in document.metadata.items():
                if value:
                    markdown_parts.append(f"{key}: {value}")
            markdown_parts.append("---\n")

        # Process each page
        for page in document.pages:
            markdown_parts.append(f"# Page {page.page_number}\n")

            # Add images first (if any)
            if include_images and page.images:
                for img in page.images:
                    # Use placeholder that will be replaced with actual storage path later
                    # Format: ![Image](IMAGE_PLACEHOLDER:page_X_img_Y)
                    placeholder = f"IMAGE_PLACEHOLDER:page_{page.page_number}_img_{img.image_index}"
                    img_metadata = f"{img.width}x{img.height} {img.image_type}"
                    markdown_parts.append(f"![Image {img.image_index + 1} ({img_metadata})]({placeholder})\n")

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

    @staticmethod
    def replace_image_placeholders(markdown: str, image_mapping: Dict[str, str]) -> str:
        """
        Replace image placeholders with actual storage paths

        Args:
            markdown: Markdown content with placeholders
            image_mapping: Dict mapping placeholder keys to storage URLs
                          e.g., {"page_1_img_0": "https://storage.../image.png"}

        Returns:
            Markdown with placeholders replaced
        """
        result = markdown
        for placeholder_key, storage_path in image_mapping.items():
            placeholder = f"IMAGE_PLACEHOLDER:{placeholder_key}"
            result = result.replace(placeholder, storage_path)
        return result


# Singleton instance
pdf_parser = PDFParser()
