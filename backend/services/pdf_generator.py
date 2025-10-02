"""
PDF Generator Service - Markdown to PDF conversion
Uses WeasyPrint for HTML/CSS to PDF rendering
"""
from typing import Optional
import markdown
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
        language: str = "en"
    ) -> bytes:
        """
        Convert Markdown to PDF

        Args:
            markdown_content: Markdown text
            title: Document title
            language: Language code for font selection

        Returns:
            PDF file bytes
        """
        try:
            # Convert Markdown to HTML
            html_content = self._markdown_to_html(markdown_content, title, language)

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
        language: str
    ) -> str:
        """Convert Markdown to HTML with CSS styling"""

        # Convert Markdown to HTML
        md = markdown.Markdown(extensions=[
            'extra',       # Tables, fenced code blocks, etc.
            'codehilite',  # Code syntax highlighting
            'toc',         # Table of contents
            'nl2br'        # New line to <br>
        ])

        body_html = md.convert(markdown_content)

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
            size: A4;
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
