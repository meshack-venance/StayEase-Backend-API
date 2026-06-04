from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import StayEaseException


ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


async def save_image_upload(file: UploadFile, folder: str, filename_prefix: str) -> str:
    _validate_image_metadata(file)

    content = await file.read()
    _validate_image_size(content)

    extension = Path(file.filename or "").suffix.lower()
    filename = f"{filename_prefix}-{uuid4().hex}{extension}"
    target_dir = Path(settings.upload_dir) / folder
    target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / filename
    # UploadFile is read into memory because our configured limit is small.
    target_path.write_bytes(content)

    return f"/{settings.upload_dir}/{folder}/{filename}"


def _validate_image_metadata(file: UploadFile) -> None:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise StayEaseException(
            "Unsupported image extension. Use jpg, jpeg, png, or webp.",
            status_code=400,
        )

    if file.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise StayEaseException(
            "Unsupported image content type. Use jpg, png, or webp.",
            status_code=400,
        )


def _validate_image_size(content: bytes) -> None:
    max_size_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_size_bytes:
        raise StayEaseException(
            f"Image size must be {settings.max_upload_size_mb}MB or less.",
            status_code=400,
        )
