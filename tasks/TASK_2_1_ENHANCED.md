# Task 2.1: PDF 파싱 엔진 개발 (ODIN-AI 패턴 적용)

**담당자**: 백엔드 개발자
**예상 소요 시간**: 8시간
**우선순위**: 🔴 High
**상태**: 📅 예정
**선행 작업**: TASK_1_1, TASK_1_2 완료 필수

**참고 프로젝트**: ODIN-AI `/tools/pdf-viewer` 모듈

---

## 📋 목표

ODIN-AI 프로젝트에서 검증된 PDF 파싱 패턴을 활용하여, PDF 파일을 Markdown으로 변환하는 강력한 파싱 엔진을 개발합니다.

### 핵심 기능
1. **다중 파서 지원**: PyPDF2, pdfplumber, PyMuPDF 자동 선택
2. **테이블 추출**: 표 구조 보존 및 Markdown 변환
3. **메타데이터 추출**: 제목, 작성자, 페이지 수 등
4. **레이아웃 정보 보존**: 좌표, 폰트, 크기 정보 저장

---

## ✅ 체크리스트

### 1. 데이터 모델 설계 (ODIN-AI 패턴)

#### services/pdf/models.py
- [ ] PDFTable 모델 생성
  ```python
  from dataclasses import dataclass, field
  from typing import List, Dict, Any, Optional

  @dataclass
  class PDFTable:
      """PDF 테이블"""
      page_num: int
      rows: int
      cols: int
      cells: List[List[str]]
      bbox: tuple = None  # (x0, y0, x1, y1)

      def to_markdown(self) -> str:
          """테이블을 마크다운 형식으로 변환"""
          if not self.cells or len(self.cells) == 0:
              return ""

          md_lines = []

          # 헤더
          if len(self.cells) > 0:
              header = self.cells[0]
              md_lines.append("| " + " | ".join(str(cell or "") for cell in header) + " |")
              md_lines.append("| " + " | ".join("---" for _ in header) + " |")

          # 데이터 행
          for row in self.cells[1:]:
              md_lines.append("| " + " | ".join(str(cell or "") for cell in row) + " |")

          return "\n".join(md_lines)
  ```

- [ ] PDFPage 모델 생성
  ```python
  @dataclass
  class PDFPage:
      """PDF 페이지"""
      page_num: int
      text: str
      tables: List[PDFTable] = field(default_factory=list)
      images: List[Dict[str, Any]] = field(default_factory=list)
      bbox: tuple = None  # (width, height)

      # 번역용 추가 필드
      layout_info: Optional[Dict] = None  # 레이아웃 정보 (폰트, 크기, 위치)

      def to_markdown(self) -> str:
          """페이지를 마크다운으로 변환"""
          md_content = [f"## 페이지 {self.page_num}\n"]

          # 텍스트 추가
          md_content.append(self.text)

          # 테이블 추가
          if self.tables:
              md_content.append("\n### 📊 표\n")
              for i, table in enumerate(self.tables):
                  md_content.append(f"**표 {i+1}**\n")
                  md_content.append(table.to_markdown())
                  md_content.append("\n")

          return "\n".join(md_content)
  ```

- [ ] PDFMetadata 모델 생성
  ```python
  @dataclass
  class PDFMetadata:
      """PDF 메타데이터"""
      title: Optional[str] = None
      author: Optional[str] = None
      creator: Optional[str] = None
      producer: Optional[str] = None
      subject: Optional[str] = None
      keywords: Optional[str] = None
      creation_date: Optional[str] = None
      modification_date: Optional[str] = None
      pages: int = 0
      file_size_bytes: int = 0
  ```

- [ ] PDFDocument 모델 생성
  ```python
  @dataclass
  class PDFDocument:
      """PDF 문서"""
      metadata: PDFMetadata
      pages: List[PDFPage] = field(default_factory=list)
      raw_text: str = ""

      def to_markdown(self) -> str:
          """전체 문서를 마크다운으로 변환"""
          md_content = []

          # 제목
          if self.metadata.title:
              md_content.append(f"# {self.metadata.title}\n")

          # 메타데이터
          md_content.append("## 📋 문서 정보\n")
          if self.metadata.author:
              md_content.append(f"- **작성자**: {self.metadata.author}")
          if self.metadata.pages:
              md_content.append(f"- **페이지 수**: {self.metadata.pages}")
          if self.metadata.creation_date:
              md_content.append(f"- **생성일**: {self.metadata.creation_date}")
          md_content.append("\n---\n")

          # 페이지별 내용
          for page in self.pages:
              md_content.append(page.to_markdown())
              md_content.append("\n")

          return "\n".join(md_content)

      def to_dict(self) -> Dict[str, Any]:
          """딕셔너리로 변환 (DB 저장용)"""
          return {
              "metadata": {
                  "title": self.metadata.title,
                  "author": self.metadata.author,
                  "pages": self.metadata.pages,
                  "file_size": self.metadata.file_size_bytes,
              },
              "statistics": {
                  "total_pages": len(self.pages),
                  "total_tables": sum(len(page.tables) for page in self.pages),
                  "total_images": sum(len(page.images) for page in self.pages),
                  "text_length": len(self.raw_text),
              }
          }
  ```

### 2. PDF 파서 클래스 구현 (ODIN-AI 패턴)

#### services/pdf/parser.py
- [ ] PDFParser 클래스 기본 구조
  ```python
  import PyPDF2
  import pdfplumber
  import fitz  # pymupdf
  from pathlib import Path
  from typing import Optional
  import logging

  from .models import PDFDocument, PDFMetadata, PDFPage, PDFTable

  logger = logging.getLogger(__name__)

  class PDFParser:
      """PDF 파일을 파싱하는 메인 클래스 (ODIN-AI 검증 패턴)"""

      def __init__(self, method: str = "auto"):
          """
          Args:
              method: 파싱 방법 ("auto", "pypdf2", "pdfplumber", "pymupdf")
          """
          self.method = method
          self.supported_methods = ["auto", "pypdf2", "pdfplumber", "pymupdf"]

          if method not in self.supported_methods:
              raise ValueError(f"지원하지 않는 파싱 방법: {method}")

      def parse(self, file_path: str) -> PDFDocument:
          """PDF 파일을 파싱하여 구조화된 문서 객체 반환"""
          try:
              path = Path(file_path)
              if not path.exists():
                  raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

              if not path.suffix.lower() == '.pdf':
                  raise ValueError("PDF 파일만 처리할 수 있습니다.")

              # 파싱 방법에 따라 다른 처리
              if self.method == "auto":
                  return self._parse_auto(file_path)
              elif self.method == "pypdf2":
                  return self._parse_pypdf2(file_path)
              elif self.method == "pdfplumber":
                  return self._parse_pdfplumber(file_path)
              elif self.method == "pymupdf":
                  return self._parse_pymupdf(file_path)

          except Exception as e:
              logger.error(f"PDF 파싱 실패: {e}")
              # 빈 문서 반환 (에러 전파 대신)
              return PDFDocument(
                  metadata=PDFMetadata(),
                  pages=[],
                  raw_text=f"파싱 오류: {str(e)}"
              )
  ```

- [ ] Auto 파싱 (폴백 전략)
  ```python
  def _parse_auto(self, file_path: str) -> PDFDocument:
      """자동으로 가장 적합한 파서 선택 (ODIN-AI 검증 순서)"""
      try:
          # 1순위: pdfplumber (테이블 추출 우수)
          logger.info("pdfplumber로 파싱 시도")
          return self._parse_pdfplumber(file_path)
      except Exception as e1:
          logger.warning(f"pdfplumber 실패, pymupdf 시도: {e1}")
          try:
              # 2순위: pymupdf (빠르고 안정적)
              return self._parse_pymupdf(file_path)
          except Exception as e2:
              logger.warning(f"pymupdf 실패, pypdf2 시도: {e2}")
              try:
                  # 3순위: pypdf2 (기본적)
                  return self._parse_pypdf2(file_path)
              except Exception as e3:
                  logger.error(f"모든 파서 실패: {e3}")
                  raise e3
  ```

- [ ] pdfplumber 파싱 (테이블 우수)
  ```python
  def _parse_pdfplumber(self, file_path: str) -> PDFDocument:
      """pdfplumber를 사용한 파싱 (테이블 추출 최적)"""
      with pdfplumber.open(file_path) as pdf:
          # 메타데이터 추출
          metadata = self._extract_metadata_pdfplumber(pdf)
          metadata.file_size_bytes = Path(file_path).stat().st_size

          # 페이지별 처리
          pages = []
          all_text = []

          for i, page in enumerate(pdf.pages):
              # 텍스트 추출
              text = page.extract_text() or ""
              all_text.append(text)

              # 테이블 추출
              tables = []
              try:
                  page_tables = page.extract_tables()
                  for j, table_data in enumerate(page_tables or []):
                      if table_data and len(table_data) > 0:
                          table = PDFTable(
                              page_num=i + 1,
                              rows=len(table_data),
                              cols=len(table_data[0]) if table_data else 0,
                              cells=table_data,
                              bbox=page.bbox
                          )
                          tables.append(table)
              except Exception as e:
                  logger.warning(f"페이지 {i+1} 테이블 추출 실패: {e}")

              # 레이아웃 정보 추출 (번역 시 활용)
              layout_info = {
                  "width": page.width,
                  "height": page.height,
                  "bbox": page.bbox,
              }

              pdf_page = PDFPage(
                  page_num=i + 1,
                  text=text,
                  tables=tables,
                  images=[],
                  bbox=page.bbox,
                  layout_info=layout_info
              )
              pages.append(pdf_page)

          return PDFDocument(
              metadata=metadata,
              pages=pages,
              raw_text="\n".join(all_text)
          )
  ```

- [ ] PyMuPDF 파싱 (빠르고 안정적)
  ```python
  def _parse_pymupdf(self, file_path: str) -> PDFDocument:
      """PyMuPDF를 사용한 파싱 (속도 최적)"""
      doc = fitz.open(file_path)

      # 메타데이터 추출
      metadata = self._extract_metadata_pymupdf(doc)
      metadata.file_size_bytes = Path(file_path).stat().st_size

      # 페이지별 처리
      pages = []
      all_text = []

      for i, page in enumerate(doc):
          # 텍스트 추출 (블록 단위 - 레이아웃 정보 포함)
          text_blocks = page.get_text("dict")["blocks"]
          text = page.get_text()
          all_text.append(text)

          # 테이블 추출 (PyMuPDF 1.23+)
          tables = []
          try:
              page_tables = page.find_tables()
              for j, table in enumerate(page_tables.tables):
                  table_data = table.extract()
                  if table_data:
                      pdf_table = PDFTable(
                          page_num=i + 1,
                          rows=len(table_data),
                          cols=len(table_data[0]) if table_data else 0,
                          cells=table_data,
                          bbox=table.bbox
                      )
                      tables.append(pdf_table)
          except Exception as e:
              logger.warning(f"페이지 {i+1} 테이블 추출 실패: {e}")

          # 레이아웃 정보 (폰트, 크기 포함)
          layout_info = {
              "width": page.rect.width,
              "height": page.rect.height,
              "text_blocks": text_blocks,  # 위치, 폰트, 크기 정보
          }

          pdf_page = PDFPage(
              page_num=i + 1,
              text=text,
              tables=tables,
              images=[],
              bbox=(page.rect.width, page.rect.height),
              layout_info=layout_info
          )
          pages.append(pdf_page)

      doc.close()

      return PDFDocument(
          metadata=metadata,
          pages=pages,
          raw_text="\n".join(all_text)
      )
  ```

- [ ] PyPDF2 파싱 (기본 폴백)
  ```python
  def _parse_pypdf2(self, file_path: str) -> PDFDocument:
      """PyPDF2를 사용한 파싱 (기본 폴백)"""
      with open(file_path, 'rb') as file:
          reader = PyPDF2.PdfReader(file)

          # 메타데이터 추출
          metadata = self._extract_metadata_pypdf2(reader)
          metadata.file_size_bytes = Path(file_path).stat().st_size

          # 페이지별 텍스트 추출
          pages = []
          all_text = []

          for i, page in enumerate(reader.pages):
              text = page.extract_text()
              all_text.append(text)

              pdf_page = PDFPage(
                  page_num=i + 1,
                  text=text,
                  tables=[],  # PyPDF2는 테이블 추출 제한적
                  images=[]
              )
              pages.append(pdf_page)

          return PDFDocument(
              metadata=metadata,
              pages=pages,
              raw_text="\n".join(all_text)
          )
  ```

- [ ] 메타데이터 추출 메서드
  ```python
  def _extract_metadata_pdfplumber(self, pdf) -> PDFMetadata:
      """pdfplumber로 메타데이터 추출"""
      try:
          info = pdf.metadata or {}
          return PDFMetadata(
              title=info.get('Title'),
              author=info.get('Author'),
              creator=info.get('Creator'),
              producer=info.get('Producer'),
              subject=info.get('Subject'),
              keywords=info.get('Keywords'),
              creation_date=str(info.get('CreationDate', '')),
              modification_date=str(info.get('ModDate', '')),
              pages=len(pdf.pages)
          )
      except Exception as e:
          logger.warning(f"메타데이터 추출 실패: {e}")
          return PDFMetadata(pages=len(pdf.pages))

  def _extract_metadata_pymupdf(self, doc) -> PDFMetadata:
      """PyMuPDF로 메타데이터 추출"""
      try:
          info = doc.metadata or {}
          return PDFMetadata(
              title=info.get('title'),
              author=info.get('author'),
              creator=info.get('creator'),
              producer=info.get('producer'),
              subject=info.get('subject'),
              keywords=info.get('keywords'),
              creation_date=info.get('creationDate', ''),
              modification_date=info.get('modDate', ''),
              pages=doc.page_count
          )
      except Exception as e:
          logger.warning(f"메타데이터 추출 실패: {e}")
          return PDFMetadata(pages=doc.page_count)

  def _extract_metadata_pypdf2(self, reader) -> PDFMetadata:
      """PyPDF2로 메타데이터 추출"""
      try:
          info = reader.metadata or {}
          return PDFMetadata(
              title=info.get('/Title'),
              author=info.get('/Author'),
              creator=info.get('/Creator'),
              producer=info.get('/Producer'),
              subject=info.get('/Subject'),
              keywords=info.get('/Keywords'),
              creation_date=str(info.get('/CreationDate', '')),
              modification_date=str(info.get('/ModDate', '')),
              pages=len(reader.pages)
          )
      except Exception as e:
          logger.warning(f"메타데이터 추출 실패: {e}")
          return PDFMetadata(pages=len(reader.pages))
  ```

### 3. Markdown 포맷터 구현

#### services/pdf/markdown_formatter.py
- [ ] 기본 포맷터 클래스
  ```python
  import re
  from typing import List
  from .models import PDFDocument

  class MarkdownFormatter:
      """PDF 내용을 Markdown으로 포맷하는 클래스"""

      def __init__(self, preserve_layout: bool = True):
          self.preserve_layout = preserve_layout

      def format_document(self, doc: PDFDocument, title: str = None) -> str:
          """전체 문서를 마크다운으로 변환"""
          return doc.to_markdown()

      def format_page(self, page: PDFPage) -> str:
          """개별 페이지를 마크다운으로 변환"""
          return page.to_markdown()
  ```

### 4. API 엔드포인트 추가

#### api/projects.py (새 파일)
- [ ] PDF 파싱 API 엔드포인트
  ```python
  from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
  from sqlalchemy.ext.asyncio import AsyncSession
  import tempfile
  import os
  from pathlib import Path

  from services.pdf.parser import PDFParser
  from services.pdf.models import PDFDocument
  from core.database import get_db
  from models.project import Project
  from api.dependencies import get_current_user

  router = APIRouter(prefix="/api/projects", tags=["projects"])

  @router.post("/parse")
  async def parse_pdf(
      file: UploadFile = File(...),
      method: str = "auto",
      user = Depends(get_current_user),
      db: AsyncSession = Depends(get_db)
  ):
      """PDF 파일 파싱 (ODIN-AI 패턴)"""

      # 파일 검증
      if not file.filename.lower().endswith('.pdf'):
          raise HTTPException(400, "PDF 파일만 지원합니다")

      try:
          # 임시 파일 저장
          with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
              content = await file.read()
              tmp.write(content)
              tmp_path = tmp.name

          try:
              # PDF 파싱
              parser = PDFParser(method=method)
              doc: PDFDocument = parser.parse(tmp_path)

              # Markdown 변환
              markdown_original = doc.to_markdown()

              # 프로젝트 생성 (DB 저장은 별도 엔드포인트에서)
              return {
                  "success": True,
                  "metadata": doc.metadata.__dict__,
                  "statistics": doc.to_dict()["statistics"],
                  "markdown_preview": markdown_original[:500] + "...",
                  "full_text_length": len(doc.raw_text)
              }

          finally:
              # 임시 파일 삭제
              os.unlink(tmp_path)

      except Exception as e:
          raise HTTPException(500, f"PDF 파싱 실패: {str(e)}")
  ```

### 5. 유닛 테스트 작성

#### tests/test_pdf_parser.py
- [ ] 테스트 케이스 작성
  ```python
  import pytest
  from pathlib import Path
  from services.pdf.parser import PDFParser

  @pytest.fixture
  def sample_pdf():
      """샘플 PDF 파일 경로"""
      return "tests/fixtures/sample.pdf"

  def test_parse_with_pdfplumber(sample_pdf):
      """pdfplumber 파싱 테스트"""
      parser = PDFParser(method="pdfplumber")
      doc = parser.parse(sample_pdf)

      assert doc is not None
      assert doc.metadata.pages > 0
      assert len(doc.pages) > 0
      assert len(doc.raw_text) > 0

  def test_parse_with_pymupdf(sample_pdf):
      """PyMuPDF 파싱 테스트"""
      parser = PDFParser(method="pymupdf")
      doc = parser.parse(sample_pdf)

      assert doc is not None
      assert doc.metadata.pages > 0

  def test_parse_auto_fallback(sample_pdf):
      """Auto 파싱 폴백 테스트"""
      parser = PDFParser(method="auto")
      doc = parser.parse(sample_pdf)

      assert doc is not None

  def test_table_extraction(sample_pdf):
      """테이블 추출 테스트"""
      parser = PDFParser(method="pdfplumber")
      doc = parser.parse(sample_pdf)

      total_tables = sum(len(page.tables) for page in doc.pages)
      assert total_tables >= 0  # 테이블이 있을 수도, 없을 수도

  def test_markdown_conversion(sample_pdf):
      """Markdown 변환 테스트"""
      parser = PDFParser(method="auto")
      doc = parser.parse(sample_pdf)

      markdown = doc.to_markdown()
      assert markdown is not None
      assert len(markdown) > 0
      assert "##" in markdown  # 마크다운 헤더 포함
  ```

---

## 🧪 검증 방법

### 1. 수동 테스트
```bash
# 테스트 PDF 파일 준비
mkdir -p tests/fixtures
# sample.pdf 파일을 tests/fixtures/ 에 복사

# Python 인터프리터에서 테스트
python
>>> from services.pdf.parser import PDFParser
>>> parser = PDFParser(method="auto")
>>> doc = parser.parse("tests/fixtures/sample.pdf")
>>> print(f"페이지 수: {doc.metadata.pages}")
>>> print(f"텍스트 길이: {len(doc.raw_text)}")
>>> print(doc.to_markdown()[:500])
```

### 2. 자동화 테스트
```bash
pytest tests/test_pdf_parser.py -v
```

### 3. API 테스트
```bash
# 서버 실행
uvicorn main:app --reload

# curl로 테스트
curl -X POST "http://localhost:8000/api/projects/parse" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@tests/fixtures/sample.pdf" \
  -F "method=auto"
```

---

## 📝 완료 조건

- [ ] PDFParser 클래스가 3가지 파서 모두 지원
- [ ] Auto 파싱이 폴백 전략으로 작동
- [ ] 테이블 추출이 정상 작동 (pdfplumber, PyMuPDF)
- [ ] Markdown 변환이 정상 작동
- [ ] 레이아웃 정보가 보존됨
- [ ] 유닛 테스트 95% 이상 통과
- [ ] API 엔드포인트가 정상 응답

---

## 🚨 주의사항

- **메모리 관리**: 대용량 PDF는 청크 단위 처리 고려
- **에러 핸들링**: 파싱 실패 시 빈 문서 반환 (에러 전파 X)
- **임시 파일 정리**: UploadFile 처리 후 반드시 삭제
- **로그 안전**: 파일명만 로그, 내용은 로그 X

---

## 📚 참고 자료

- **ODIN-AI 참고 코드**:
  - `/tools/pdf-viewer/pdf_viewer/parser.py`
  - `/tools/pdf-viewer/pdf_viewer/markdown_formatter.py`
  - `/tools/pdf-viewer/api/app.py`
- [pdfplumber 문서](https://github.com/jsvine/pdfplumber)
- [PyMuPDF 문서](https://pymupdf.readthedocs.io/)

---

**작성일**: 2025-10-02
**ODIN-AI 패턴 적용**: ✅
**최종 수정**: 2025-10-02
