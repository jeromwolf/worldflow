"""
PDF Generator Service - Markdown to PDF conversion
Uses WeasyPrint for HTML/CSS to PDF rendering
"""
from typing import Optional
import markdown
import base64
import re
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from io import BytesIO
from loguru import logger


class PDFGeneratorService:
    """Convert Markdown to PDF with styling"""

    def __init__(self):
        self.font_config = FontConfiguration()

    def markdown_to_pdf(
        self,
        markdown_content: str,
        title: Optional[str] = None,
        language: str = "en",
        storage_service = None,
        project_images: list = None
    ) -> bytes:
        """
        Convert Markdown to PDF

        Args:
            markdown_content: Markdown text
            title: Document title
            language: Language code for font selection
            storage_service: Storage service instance for loading images
            project_images: List of ProjectImage objects with position info

        Returns:
            PDF file bytes
        """
        try:
            # Convert Markdown to HTML
            html_content = self._markdown_to_html(markdown_content, title, language, project_images)

            # Replace image paths with Base64 data URIs
            if storage_service:
                html_content = self._embed_images_as_base64(html_content, storage_service)

            # Generate PDF
            pdf_bytes = self._html_to_pdf(html_content)

            logger.success(f"Generated PDF ({len(pdf_bytes)} bytes)")
            return pdf_bytes

        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            raise ValueError(f"PDF generation failed: {str(e)}")

    def _markdown_to_html(
        self,
        markdown_content: str,
        title: Optional[str],
        language: str,
        project_images: list = None
    ) -> str:
        """Convert Markdown to HTML with CSS styling"""

        # Split content by pages (# Page N markers)
        pages_content = self._split_by_pages(markdown_content, project_images)

        # Convert each page to HTML with positioned images
        body_html = ""
        for page_data in pages_content:
            page_html = self._convert_page_to_html(page_data)
            body_html += page_html

        # Build complete HTML document
        html_template = f"""
<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title or 'Translated Document'}</title>
    <style>
        @page {{
            size: letter;  /* US Letter (8.5" x 11") */
            margin: 2.5cm 2cm;
            @top-center {{
                content: "{title or ''}";
                font-size: 10pt;
                color: #666;
            }}
            @bottom-center {{
                content: counter(page);
                font-size: 10pt;
                color: #666;
            }}
        }}

        body {{
            font-family: "Noto Sans", "Malgun Gothic", Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }}

        h1 {{
            font-size: 24pt;
            font-weight: bold;
            margin-top: 20pt;
            margin-bottom: 12pt;
            color: #222;
            page-break-after: avoid;
        }}

        h2 {{
            font-size: 18pt;
            font-weight: bold;
            margin-top: 16pt;
            margin-bottom: 10pt;
            color: #333;
            page-break-after: avoid;
        }}

        h3 {{
            font-size: 14pt;
            font-weight: bold;
            margin-top: 12pt;
            margin-bottom: 8pt;
            color: #444;
            page-break-after: avoid;
        }}

        h4, h5, h6 {{
            font-size: 12pt;
            font-weight: bold;
            margin-top: 10pt;
            margin-bottom: 6pt;
            color: #555;
            page-break-after: avoid;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 10pt;
            text-align: justify;
        }}

        ul, ol {{
            margin-top: 6pt;
            margin-bottom: 10pt;
            padding-left: 20pt;
        }}

        li {{
            margin-bottom: 4pt;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10pt;
            margin-bottom: 10pt;
            page-break-inside: avoid;
        }}

        th {{
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            padding: 8pt;
            text-align: left;
            font-weight: bold;
        }}

        td {{
            border: 1px solid #ddd;
            padding: 8pt;
        }}

        code {{
            background-color: #f5f5f5;
            padding: 2pt 4pt;
            border-radius: 3px;
            font-family: "Courier New", monospace;
            font-size: 9pt;
        }}

        pre {{
            background-color: #f5f5f5;
            padding: 10pt;
            border-radius: 5px;
            overflow-x: auto;
            page-break-inside: avoid;
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
        }}

        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 12pt;
            margin-left: 0;
            color: #666;
            font-style: italic;
        }}

        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 20pt 0;
        }}

        a {{
            color: #0066cc;
            text-decoration: none;
        }}

        img {{
            max-width: 100%;
            height: auto;
            page-break-inside: avoid;
        }}

        .page-container {{
            page-break-after: always;
        }}

        .page-content {{
            /* Page content wrapper */
        }}

        .page-break {{
            page-break-before: always;
        }}
    </style>
</head>
<body>
    {body_html}
</body>
</html>
"""

        return html_template

    def _embed_images_as_base64(self, html_content: str, storage_service) -> str:
        """
        Replace image file paths with Base64 data URIs

        Args:
            html_content: HTML with img tags containing file paths
            storage_service: Storage service to load image files

        Returns:
            HTML with embedded Base64 images
        """
        # Pattern to match img src attributes
        # Matches: <img ... src="path/to/image.png" ...>
        img_pattern = r'<img\s+([^>]*\s+)?src=["\']([^"\']+)["\']([^>]*)>'

        def replace_image(match):
            """Replace single image path with Base64 data URI"""
            before_src = match.group(1) or ''
            image_path = match.group(2)
            after_src = match.group(3) or ''

            # Skip if already a data URI or external URL
            if image_path.startswith('data:') or image_path.startswith('http'):
                return match.group(0)

            try:
                # Load image from storage
                image_bytes = storage_service.download_file(image_path)

                # Determine MIME type from file extension
                if image_path.lower().endswith('.png'):
                    mime_type = 'image/png'
                elif image_path.lower().endswith(('.jpg', '.jpeg')):
                    mime_type = 'image/jpeg'
                elif image_path.lower().endswith('.gif'):
                    mime_type = 'image/gif'
                elif image_path.lower().endswith('.webp'):
                    mime_type = 'image/webp'
                else:
                    mime_type = 'image/png'  # Default

                # Encode to Base64
                base64_data = base64.b64encode(image_bytes).decode('utf-8')

                # Create data URI
                data_uri = f"data:{mime_type};base64,{base64_data}"

                # Rebuild img tag with data URI
                return f'<img {before_src}src="{data_uri}"{after_src}>'

            except Exception as e:
                logger.warning(f"Failed to embed image {image_path}: {e}")
                # Keep original path if embedding fails
                return match.group(0)

        # Replace all images
        result = re.sub(img_pattern, replace_image, html_content)

        return result

    def _split_by_pages(self, markdown_content: str, project_images: list = None) -> list:
        """
        Split markdown content by pages

        Args:
            markdown_content: Full markdown text
            project_images: List of ProjectImage objects

        Returns:
            List of dicts with page_number, content, and images
        """
        import re

        # Split by page markers (# Page N)
        page_pattern = r'# Page (\d+)'
        parts = re.split(page_pattern, markdown_content)

        pages_data = []

        # parts[0] is content before first page (usually empty or metadata)
        # parts[1] = page_number, parts[2] = content, parts[3] = page_number, parts[4] = content, ...
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                page_num = int(parts[i])
                page_content = parts[i + 1]

                # Find images for this page
                page_images = []
                if project_images:
                    page_images = [img for img in project_images if img.page_number == page_num]

                pages_data.append({
                    'page_number': page_num,
                    'content': page_content,
                    'images': page_images
                })

        return pages_data

    def _convert_page_to_html(self, page_data: dict) -> str:
        """
        Convert a single page to HTML with positioned images

        Args:
            page_data: Dict with page_number, content, images

        Returns:
            HTML string for the page
        """
        import markdown

        page_num = page_data['page_number']
        content = page_data['content']
        images = page_data['images']

        # Convert markdown to HTML
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc', 'nl2br'])
        content_html = md.convert(content)

        # Apply image positioning
        if images:
            content_html = self._apply_image_positions_for_page(content_html, images)

        # Wrap in page container
        page_html = f'''
<div class="page-container" data-page="{page_num}">
    <div class="page-content">
        {content_html}
    </div>
</div>
'''
        return page_html

    def _apply_image_positions_for_page(self, html_content: str, page_images: list) -> str:
        """
        Apply sizing to images (keep in normal flow, just resize)

        Args:
            html_content: HTML content for one page
            page_images: List of ProjectImage objects for this page only

        Returns:
            HTML with sized images
        """
        # Create a mapping of storage_path -> ProjectImage
        image_map = {img.storage_path: img for img in page_images}

        # Pattern to match img tags
        img_pattern = r'<img\s+([^>]*\s+)?src=["\']([^"\']+)["\']([^>]*)>'

        def replace_with_size(match):
            """Resize image to match original PDF rendering"""
            before_src = match.group(1) or ''
            image_path = match.group(2)
            after_src = match.group(3) or ''

            # Find matching ProjectImage
            project_image = image_map.get(image_path)

            if project_image and project_image.width:
                # Use rendered size from PDF
                # Keep image in normal flow, just resize it
                style = f'style="width: {project_image.width}pt; height: {project_image.height}pt; display: block; margin: 10pt auto;"'
                return f'<img {before_src}src="{image_path}"{after_src} {style}>'
            else:
                # No size info - return original
                return match.group(0)

        # Replace all images
        result = re.sub(img_pattern, replace_with_size, html_content)

        return result

    def _html_to_pdf(self, html_content: str) -> bytes:
        """Convert HTML to PDF using WeasyPrint"""

        # Create BytesIO buffer
        pdf_buffer = BytesIO()

        # Generate PDF
        HTML(string=html_content).write_pdf(
            pdf_buffer,
            font_config=self.font_config
        )

        # Get bytes
        pdf_bytes = pdf_buffer.getvalue()
        pdf_buffer.close()

        return pdf_bytes


# Singleton instance
pdf_generator = PDFGeneratorService()
