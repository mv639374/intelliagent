import hashlib
from pathlib import Path
from typing import Any, Dict, List

from fastapi import UploadFile

from .base_connector import BaseConnector

# Define a storage path. In a real app, this would be configurable.
UPLOAD_DIR = Path("/data/uploads")


class FileConnector(BaseConnector):
    """
    Connector for handling local file uploads.
    """

    async def fetch(self, source: UploadFile) -> List[Dict[str, Any]]:
        """
        Reads an uploaded file, saves it to a persistent storage location,
        and returns its content and metadata.

        Args:
        ----
            source: The UploadFile object from FastAPI.

        Returns:
        -------
            A list containing a single dictionary with the file's
            content and computed metadata.

        """
        # Ensure the upload directory exists
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        contents = await source.read()
        sha256_hash = hashlib.sha256(contents).hexdigest()

        # Save the file to a content-addressable path
        file_path = UPLOAD_DIR / sha256_hash
        with open(file_path, "wb") as f:
            f.write(contents)

        return [
            {
                "content": contents,
                "metadata": {
                    "filename": source.filename,
                    "mime_type": source.content_type,
                    "size_bytes": len(contents),
                    "sha256": sha256_hash,
                    "storage_path": str(file_path),
                },
            }
        ]
