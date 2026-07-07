"""Local file storage for appointment photos."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from app.models.appointment import AppointmentPhoto
from app.models.enums import AppointmentPhotoTag
from app.services.exceptions import ValidationError


class AppointmentPhotoStorageService:
    """Persist appointment photos under the local static uploads directory."""

    def __init__(self, upload_root: str = "app/static/uploads") -> None:
        """Initialize the storage service with an upload root."""
        self.upload_root = Path(upload_root)
        self.upload_root.mkdir(parents=True, exist_ok=True)

    def save_appointment_photo(
        self,
        *,
        appointment_id: int,
        tag: AppointmentPhotoTag,
        filename: str,
        content: bytes,
    ) -> AppointmentPhoto:
        """Persist raw photo bytes and return unsaved photo metadata."""
        if not filename:
            raise ValidationError("Photo filename is required.")

        extension = Path(filename).suffix or ".jpg"
        stored_name = f"appointment_{appointment_id}_{uuid4().hex}{extension}"
        destination = self.upload_root / stored_name
        destination.write_bytes(content)

        return AppointmentPhoto(
            appointment_id=appointment_id,
            tag=tag,
            file_path=f"static/uploads/{stored_name}",
        )
