"""
File Storage Service - AWS S3 integration
"""
import os
import uuid
from typing import Optional
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from loguru import logger
from core.config import settings


class StorageService:
    """AWS S3 file storage service"""

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.S3_BUCKET_NAME

    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str = "application/pdf",
        folder: str = "uploads"
    ) -> str:
        """
        Upload file to S3

        Args:
            file_content: File bytes
            filename: Original filename
            content_type: MIME type
            folder: S3 folder path

        Returns:
            S3 URL of uploaded file
        """
        try:
            # Generate unique filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            file_extension = os.path.splitext(filename)[1]
            s3_key = f"{folder}/{timestamp}_{unique_id}{file_extension}"

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType=content_type,
                Metadata={
                    'original_filename': filename
                }
            )

            # Generate URL
            file_url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"

            logger.info(f"Uploaded file to S3: {s3_key}")
            return file_url

        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {str(e)}")
            raise ValueError(f"File upload failed: {str(e)}")

    def download_file(self, s3_url: str) -> bytes:
        """
        Download file from S3

        Args:
            s3_url: Full S3 URL

        Returns:
            File content as bytes
        """
        try:
            # Extract S3 key from URL
            s3_key = self._extract_s3_key(s3_url)

            # Download from S3
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )

            file_content = response['Body'].read()
            logger.info(f"Downloaded file from S3: {s3_key}")
            return file_content

        except ClientError as e:
            logger.error(f"Failed to download file from S3: {str(e)}")
            raise ValueError(f"File download failed: {str(e)}")

    def delete_file(self, s3_url: str) -> bool:
        """
        Delete file from S3

        Args:
            s3_url: Full S3 URL

        Returns:
            True if successful
        """
        try:
            # Extract S3 key from URL
            s3_key = self._extract_s3_key(s3_url)

            # Delete from S3
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )

            logger.info(f"Deleted file from S3: {s3_key}")
            return True

        except ClientError as e:
            logger.error(f"Failed to delete file from S3: {str(e)}")
            return False

    def get_presigned_url(self, s3_url: str, expiration: int = 3600) -> str:
        """
        Generate presigned URL for temporary access

        Args:
            s3_url: Full S3 URL
            expiration: URL expiration time in seconds (default 1 hour)

        Returns:
            Presigned URL
        """
        try:
            s3_key = self._extract_s3_key(s3_url)

            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )

            return presigned_url

        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {str(e)}")
            raise ValueError(f"Presigned URL generation failed: {str(e)}")

    def _extract_s3_key(self, s3_url: str) -> str:
        """Extract S3 key from full URL"""
        # URL format: https://bucket.s3.region.amazonaws.com/key
        parts = s3_url.split(f"{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/")
        if len(parts) > 1:
            return parts[1]
        else:
            raise ValueError(f"Invalid S3 URL format: {s3_url}")


# Singleton instance
storage_service = StorageService()
