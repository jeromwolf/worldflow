"""
Translation API Routes - AI translation operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import Optional

from core.database import get_db
from core.dependencies import get_current_active_user
from models.user import User
from models.project import Project, ProjectStatus
from services.translator import translator_service
from loguru import logger

router = APIRouter(prefix="/api/translation", tags=["Translation"])


@router.post("/projects/{project_id}/translate", status_code=status.HTTP_202_ACCEPTED)
async def translate_project(
    project_id: UUID,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Start translation for a project (async background task)

    Returns immediately with 202 Accepted
    Translation runs in background
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

    # Check if markdown is ready
    if not project.markdown_original:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF not yet parsed. Please wait for parsing to complete."
        )

    # Check if already translating
    if project.status == ProjectStatus.TRANSLATING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Translation already in progress"
        )

    # Update status
    project.status = ProjectStatus.TRANSLATING
    project.progress_percent = 0
    await db.commit()

    # Add background task
    background_tasks.add_task(
        translate_project_task,
        project_id=project_id,
        db=db
    )

    logger.info(f"Translation started for project {project_id}")

    return {
        "message": "Translation started",
        "project_id": str(project_id),
        "status": "translating"
    }


async def translate_project_task(project_id: UUID, db: AsyncSession):
    """
    Background task to translate project

    This should ideally run in Celery, but for simplicity using BackgroundTasks
    """
    try:
        # Get project
        result = await db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()

        if not project:
            logger.error(f"Project {project_id} not found for translation")
            return

        logger.info(f"Starting translation for project {project_id}")

        # Translate markdown
        translated_markdown = translator_service.translate_markdown(
            markdown=project.markdown_original,
            source_lang=project.source_language,
            target_lang=project.target_language,
            chunk_size=2000
        )

        # Update project
        project.markdown_translated = translated_markdown
        project.status = ProjectStatus.COMPLETED
        project.progress_percent = 100

        await db.commit()

        logger.success(f"Translation completed for project {project_id}")

    except Exception as e:
        logger.error(f"Translation failed for project {project_id}: {str(e)}")

        # Update project status to failed
        try:
            result = await db.execute(
                select(Project).where(Project.id == project_id)
            )
            project = result.scalar_one_or_none()

            if project:
                project.status = ProjectStatus.FAILED
                project.progress_percent = 0
                await db.commit()

        except Exception as db_error:
            logger.error(f"Failed to update project status: {str(db_error)}")


@router.get("/projects/{project_id}/status")
async def get_translation_status(
    project_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get translation progress status"""
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

    return {
        "project_id": str(project.id),
        "status": project.status,
        "progress_percent": project.progress_percent,
        "has_translated_content": bool(project.markdown_translated)
    }


@router.post("/text/translate")
async def translate_text(
    text: str,
    source_lang: str = "ko",
    target_lang: str = "en",
    current_user: User = Depends(get_current_active_user)
):
    """
    Translate arbitrary text (for testing or quick translation)

    This is a synchronous endpoint for small text
    """
    if len(text) > 5000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text too long. Maximum 5000 characters for quick translation."
        )

    try:
        translated = translator_service.translate_text(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang
        )

        return {
            "original": text,
            "translated": translated,
            "source_lang": source_lang,
            "target_lang": target_lang
        }

    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )
