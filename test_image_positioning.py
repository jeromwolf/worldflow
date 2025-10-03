"""
Test script for image positioning in PDF generation
"""
import sys
sys.path.insert(0, '/app')

from services.pdf_parser import pdf_parser
from services.pdf_generator import pdf_generator
from pathlib import Path

# Test file path
test_pdf = "/Users/blockmeta/Downloads/다쏘시스템 ORTEMS APS 솔루션 소개서 파워포인트 구성안.pdf"

print(f"📄 Testing PDF: {test_pdf}")

# Read PDF file
with open(test_pdf, 'rb') as f:
    file_content = f.read()

print(f"✅ File size: {len(file_content) / 1024:.2f} KB")

# Parse PDF
print("\n🔍 Parsing PDF...")
try:
    pdf_document = pdf_parser.parse(file_content, "test.pdf")
    print(f"✅ Parsed successfully with {pdf_document.parser_used}")
    print(f"   Total pages: {pdf_document.total_pages}")

    # Check images
    total_images = 0
    for page in pdf_document.pages:
        if page.images:
            print(f"\n📄 Page {page.page_number}:")
            for img in page.images:
                total_images += 1
                print(f"   - Image {img.image_index}: "
                      f"position=({img.position_x:.1f}, {img.position_y:.1f}), "
                      f"size={img.width}x{img.height}")

    print(f"\n✅ Total images found: {total_images}")

    # Convert to Markdown
    print("\n📝 Converting to Markdown...")
    markdown = pdf_parser.to_markdown(pdf_document, include_metadata=False)
    print(f"✅ Markdown length: {len(markdown)} characters")
    print(f"   First 200 chars:\n{markdown[:200]}...")

    # Mock ProjectImage objects for testing
    print("\n🖼️  Creating mock ProjectImage objects...")

    class MockProjectImage:
        def __init__(self, page_num, img_index, img_data):
            self.page_number = page_num
            self.image_index = img_index
            self.storage_path = f"IMAGE_PLACEHOLDER:page_{page_num}_img_{img_index}"
            self.position_x = img_data.position_x
            self.position_y = img_data.position_y
            self.width = img_data.width
            self.height = img_data.height
            self.image_type = img_data.image_type

    mock_images = []
    for page in pdf_document.pages:
        for img in page.images:
            mock_img = MockProjectImage(page.page_number, img.image_index, img)
            mock_images.append(mock_img)

    print(f"✅ Created {len(mock_images)} mock ProjectImage objects")

    # Test HTML generation with positioning
    print("\n🎨 Generating HTML with positioned images...")

    # We need to call the internal method directly to test
    from services.pdf_generator import PDFGeneratorService
    gen = PDFGeneratorService()

    html_content = gen._markdown_to_html(
        markdown_content=markdown,
        title="Test Document",
        language="ko",
        project_images=mock_images
    )

    print(f"✅ HTML generated: {len(html_content)} characters")

    # Check if page containers exist
    import re
    page_containers = re.findall(r'<div class="page-container"', html_content)
    positioned_images = re.findall(r'<img class="positioned"', html_content)

    print(f"   Page containers found: {len(page_containers)}")
    print(f"   Positioned images found: {len(positioned_images)}")

    # Show sample of positioned image HTML
    positioned_sample = re.search(r'<img class="positioned"[^>]+>', html_content)
    if positioned_sample:
        print(f"\n📸 Sample positioned image:")
        print(f"   {positioned_sample.group(0)[:150]}...")

    # Save test HTML
    test_html_path = "/tmp/test_positioned.html"
    with open(test_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"\n💾 Saved test HTML to: {test_html_path}")

    print("\n✅ Test completed successfully!")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
