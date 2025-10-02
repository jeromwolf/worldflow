"""
Project API Routes - File upload and project management
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import UUID

from core.database import get_db
from core.dependencies import get_current_active_user
from core.config import settings
from models.user import User
from models.project import Project, ProjectStatus
from schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate, ProjectList
from services.pdf_parser import pdf_parser
from services.storage import storage_service
from loguru import logger

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.post("/upload", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(
    file: UploadFile = File(...),
    source_language: str = Form(default="ko"),
    target_language: str = Form(default="en"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload PDF file and create new project

    Steps:
    1. Validate file (PDF, size limit)
    2. Upload to S3
    3. Parse PDF to extract text and tables
    4. Convert to Markdown
    5. Create project record
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    # Read file content
    file_content = await file.read()
    file_size_mb = len(file_content) / (1024 * 1024)

    # Validate file size
    if file_size_mb > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds {settings.MAX_FILE_SIZE_MB}MB limit"
        )

    try:
        # Upload to S3
        logger.info(f"Uploading file {file.filename} to S3")
        file_url = storage_service.upload_file(
            file_content=file_content,
            filename=file.filename,
            content_type="application/pdf",
            folder=f"users/{current_user.id}/originals"
        )

        # Parse PDF
        logger.info(f"Parsing PDF {file.filename}")
        pdf_document = pdf_parser.parse(file_content, file.filename)

        # Validate page count
        if pdf_document.total_pages > settings.MAX_PAGES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"PDF exceeds maximum page limit of {settings.MAX_PAGES} pages"
            )

        # Convert to Markdown
        logger.info(f"Converting {file.filename} to Markdown")
        markdown_content = pdf_parser.to_markdown(pdf_document)

        # Create project record
        new_project = Project(
            user_id=current_user.id,
            original_filename=file.filename,
            original_file_url=file_url,
            source_language=source_language,
            target_language=target_language,
            page_count=pdf_document.total_pages,
            status=ProjectStatus.PARSING,
            progress_percent=0,
            markdown_original=markdown_content
        )

        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)

        logger.success(f"Project created: {new_project.id} for user {current_user.id}")
        return new_project

    except ValueError as e:
        logger.error(f"PDF processing failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to process PDF: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.get("/", response_model=ProjectList)
async def list_projects(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's projects with pagination"""
    offset = (page - 1) * page_size

    # Get total count
    count_result = await db.execute(
        select(func.count(Project.id))
        .where(Project.user_id == current_user.id)
        .where(Project.deleted_at.is_(None))
    )
    total = count_result.scalar_one()

    # Get projects
    result = await db.execute(
        select(Project)
        .where(Project.user_id == current_user.id)
        .where(Project.deleted_at.is_(None))
        .order_by(Project.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    projects = result.scalars().all()

    return ProjectList(
        projects=projects,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get project details"""
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id)
        .where(Project.user_id == current_user.id)
        .where(Project.deleted_at.is_(None))
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update project (mainly for editing translated markdown)"""
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id)
        .where(Project.user_id == current_user.id)
        .where(Project.deleted_at.is_(None))
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Update fields
    if project_update.markdown_translated is not None:
        project.markdown_translated = project_update.markdown_translated

    if project_update.status is not None:
        project.status = ProjectStatus(project_update.status)

    await db.commit()
    await db.refresh(project)

    logger.info(f"Project updated: {project_id}")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Soft delete project"""
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id)
        .where(Project.user_id == current_user.id)
        .where(Project.deleted_at.is_(None))
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Soft delete
    from datetime import datetime
    project.deleted_at = datetime.utcnow()

    await db.commit()

    logger.info(f"Project soft deleted: {project_id}")
    return None
