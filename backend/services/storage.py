"""
File Storage Service - Local filesystem with Railway volume support
Uses local storage for development and Railway persistent volume for production
"""
import os
import uuid
from typing import Optional
from datetime import datetime
from pathlib import Path
from loguru import logger


class StorageService:
    """
    Filesystem storage service
    - Development: ./storage/
    - Railway: /data/ (persistent volume)
    """

    def __init__(self):
        # Railway sets RAILWAY_ENVIRONMENT variable
        is_railway = os.getenv("RAILWAY_ENVIRONMENT") is not None

        if is_railway:
            # Railway persistent volume mounted at /data
            self.base_path = Path("/data")
            logger.info("Using Railway persistent storage at /data")
        else:
            # Local development
            self.base_path = Path("./storage")
            logger.info("Using local storage at ./storage")

        self.base_path.mkdir(parents=True, exist_ok=True)

    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str = "application/pdf",
        folder: str = "uploads"
    ) -> str:
        """
        Upload file to local storage

        Args:
            file_content: File bytes
            filename: Original filename
            content_type: MIME type
            folder: Folder path

        Returns:
            Local file path
        """
        try:
            # Generate unique filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            file_extension = os.path.splitext(filename)[1]
            relative_path = f"{folder}/{timestamp}_{unique_id}{file_extension}"

            # Create folder if not exists
            file_path = self.base_path / relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(file_path, 'wb') as f:
                f.write(file_content)

            logger.info(f"Uploaded file to local storage: {relative_path}")
            return str(relative_path)

        except Exception as e:
            logger.error(f"Failed to upload file: {str(e)}")
            raise ValueError(f"File upload failed: {str(e)}")

    def download_file(self, file_path: str) -> bytes:
        """
        Download file from local storage

        Args:
            file_path: Relative file path

        Returns:
            File content as bytes
        """
        try:
            full_path = self.base_path / file_path

            if not full_path.exists():
                raise ValueError(f"File not found: {file_path}")

            with open(full_path, 'rb') as f:
                file_content = f.read()

            logger.info(f"Downloaded file from local storage: {file_path}")
            return file_content

        except Exception as e:
            logger.error(f"Failed to download file: {str(e)}")
            raise ValueError(f"File download failed: {str(e)}")

    def delete_file(self, file_path: str) -> bool:
        """
        Delete file from local storage

        Args:
            file_path: Relative file path

        Returns:
            True if successful
        """
        try:
            full_path = self.base_path / file_path

            if full_path.exists():
                full_path.unlink()
                logger.info(f"Deleted file from local storage: {file_path}")
                return True
            else:
                logger.warning(f"File not found for deletion: {file_path}")
                return False

        except Exception as e:
            logger.error(f"Failed to delete file: {str(e)}")
            return False

    def get_file_url(self, file_path: str) -> str:
        """
        Get file URL (for local development, returns file path)

        Args:
            file_path: Relative file path

        Returns:
            File path (can be used to download via API)
        """
        return f"/api/files/{file_path}"


# Singleton instance
storage_service = StorageService()
