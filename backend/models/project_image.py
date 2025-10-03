"""
ProjectImage Model - PDF 이미지 정보 저장
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .base import Base


class ProjectImage(Base):
    """프로젝트 내 이미지 정보"""

    __tablename__ = "project_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    # 페이지 정보
    page_number = Column(Integer, nullable=False)  # 페이지 번호 (1-based)
    image_index = Column(Integer, nullable=False)  # 페이지 내 이미지 순서 (0-based)

    # 저장 경로
    storage_path = Column(String(500), nullable=False)  # Storage에 저장된 이미지 경로

    # 위치 정보 (PDF 좌표계)
    position_x = Column(Float)  # X 좌표
    position_y = Column(Float)  # Y 좌표
    width = Column(Float)  # 이미지 너비
    height = Column(Float)  # 이미지 높이

    # OCR 정보 (Priority 3에서 사용)
    has_text = Column(Boolean, default=False)  # 텍스트 포함 여부
    original_text = Column(Text)  # OCR로 추출된 원본 텍스트
    translated_text = Column(Text)  # 번역된 텍스트

    # 메타데이터
    image_type = Column(String(10))  # PNG, JPEG, etc.
    file_size = Column(Integer)  # 파일 크기 (bytes)

    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    project = relationship("Project", back_populates="images")

    def __repr__(self):
        return f"<ProjectImage(project_id={self.project_id}, page={self.page_number}, index={self.image_index})>"
