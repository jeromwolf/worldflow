"""
PDF API Routes - PDF generation and download
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from datetime import datetime
from urllib.parse import quote

from core.database import get_db
from core.dependencies import get_current_active_user
from models.user import User
from models.project import Project, ProjectStatus
from services.pdf_generator import pdf_generator
from services.storage import storage_service
from loguru import logger

router = APIRouter(prefix="/api/pdf", tags=["PDF"])


@router.post("/projects/{project_id}/generate")
async def generate_pdf(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate PDF from translated Markdown

    Steps:
    1. Get project with translated markdown
    2. Convert Markdown to PDF
    3. Upload PDF to storage
    4. Update project with PDF URL
    """
    # Get project with images (eager load for position info)
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.images))
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

    # Check if translation is complete
    if not project.markdown_translated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation not yet completed. Please wait or start translation."
        )

    try:
        logger.info(f"Generating PDF for project {project_id}")

        # Load project images with position info
        # Note: project.images is already loaded via relationship
        # with order_by="ProjectImage.page_number, ProjectImage.image_index"

        # Generate PDF from translated Markdown (with embedded images and positions)
        pdf_bytes = pdf_generator.markdown_to_pdf(
            markdown_content=project.markdown_translated,
            title=project.original_filename.replace('.pdf', '_translated.pdf'),
            language=project.target_language,
            storage_service=storage_service,
            project_images=project.images  # Pass image position info
        )

        # Upload PDF to storage
        pdf_filename = project.original_filename.replace('.pdf', '_translated.pdf')
        pdf_path = storage_service.upload_file(
            file_content=pdf_bytes,
            filename=pdf_filename,
            content_type="application/pdf",
            folder=f"users/{current_user.id}/translated"
        )

        # Update project
        project.pdf_translated_url = pdf_path
        await db.commit()
        await db.refresh(project)

        logger.success(f"PDF generated for project {project_id}: {pdf_path}")

        return {
            "message": "PDF generated successfully",
            "project_id": str(project_id),
            "pdf_url": pdf_path,
            "download_url": f"/api/pdf/projects/{project_id}/download"
        }

    except Exception as e:
        logger.error(f"PDF generation failed for project {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF generation failed: {str(e)}"
        )


@router.get("/projects/{project_id}/download")
async def download_pdf(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Download translated PDF

    Returns PDF file with appropriate headers
    """
    # Get project
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

    # Check if PDF exists
    if not project.pdf_translated_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Translated PDF not yet generated. Please generate it first."
        )

    try:
        # Download PDF from storage
        pdf_bytes = storage_service.download_file(project.pdf_translated_url)

        # Generate filename
        filename = project.original_filename.replace('.pdf', '_translated.pdf')

        # Encode filename for HTTP header (RFC 2231)
        # Support both ASCII and UTF-8 filenames for browser compatibility
        encoded_filename = quote(filename.encode('utf-8'))

        # Return PDF with download headers
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )

    except Exception as e:
        logger.error(f"PDF download failed for project {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF download failed: {str(e)}"
        )


@router.get("/projects/{project_id}/preview")
async def preview_pdf(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Preview translated PDF in browser (inline, not download)
    """
    # Get project
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

    # Check if PDF exists
    if not project.pdf_translated_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Translated PDF not yet generated"
        )

    try:
        # Download PDF from storage
        pdf_bytes = storage_service.download_file(project.pdf_translated_url)

        # Return PDF for inline preview
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "inline"
            }
        )

    except Exception as e:
        logger.error(f"PDF preview failed for project {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF preview failed: {str(e)}"
        )
