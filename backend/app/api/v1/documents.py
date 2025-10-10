# import hashlib
# from pathlib import Path

# from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.api.deps import get_current_project, get_current_user
# from app.db.session import get_db
# from app.models.document import Document, DocumentStatus
# from app.models.project import Project
# from app.models.user import User
# from workers.tasks.ingest_tasks import ingest_document_task

# router = APIRouter()

# # Define upload directory
# UPLOAD_DIR = Path("/app/uploads")
# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# @router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
# async def upload_document(
#     file: UploadFile = File(...),
#     project: Project = Depends(get_current_project),
#     current_user: User = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db),
# ):
#     """
#     Accepts a file upload, creates a Document record in the database,
#     saves the file to disk, and enqueues a background task to process it.
#     """
#     try:
#         # Read file contents
#         contents = await file.read()
#         sha256_hash = hashlib.sha256(contents).hexdigest()

#         # Save file to disk using sha256 as filename
#         file_path = UPLOAD_DIR / sha256_hash
#         with open(file_path, "wb") as f:
#             f.write(contents)

#         print(f"Saved file to: {file_path}")

#         # Create a new Document record
#         new_document = Document(
#             project_id=project.id,
#             filename=file.filename,
#             mime_type=file.content_type,
#             size_bytes=len(contents),
#             sha256=sha256_hash,
#             owner_id=current_user.id,
#             status=DocumentStatus.PENDING,
#         )

#         db.add(new_document)
#         await db.commit()
#         await db.refresh(new_document)

#         print(f"Created document record with ID: {new_document.id}")

#         # Enqueue the ingestion task with both ID and hash
#         ingest_document_task.delay(document_id=str(new_document.id), sha256_hash=sha256_hash)

#         print(f"Enqueued ingest task for document: {new_document.id}")

#         return {
#             "doc_id": str(new_document.id),
#             "status": "queued_for_ingestion",
#             "filename": file.filename,
#             "sha256": sha256_hash,
#         }

#     except Exception as e:
#         await db.rollback()
#         print(f"Error uploading document: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to upload document: {str(e)}"
#         )



import hashlib
from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_current_project, get_current_user
from app.db.session import get_db
from app.models.document import Document, DocumentStatus
from app.models.project import Project
from app.models.user import User
from workers.tasks.ingest_tasks import ingest_document_task

router = APIRouter()

UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    file: UploadFile = File(...),
    project: Project = Depends(get_current_project),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    contents = await file.read()
    sha256_hash = hashlib.sha256(contents).hexdigest()

    # --- FIX: Check if document already exists ---
    result = await db.execute(select(Document).where(Document.sha256 == sha256_hash))
    existing_document = result.scalar_one_or_none()

    if existing_document:
        print(f"Document with hash {sha256_hash} already exists. Returning existing document ID.")
        return {
            "doc_id": str(existing_document.id),
            "status": "already_exists",
            "filename": existing_document.filename,
            "sha256": existing_document.sha256,
        }
    # --- END FIX ---

    file_path = UPLOAD_DIR / sha256_hash
    with open(file_path, "wb") as f:
        f.write(contents)
    print(f"Saved new file to: {file_path}")

    new_document = Document(
        project_id=project.id,
        filename=file.filename,
        mime_type=file.content_type,
        size_bytes=len(contents),
        sha256=sha256_hash,
        owner_id=current_user.id,
    )
    db.add(new_document)
    await db.commit()
    await db.refresh(new_document)

    ingest_document_task.delay(document_id=str(new_document.id), sha256_hash=sha256_hash)

    return {
        "doc_id": str(new_document.id),
        "status": "queued_for_ingestion",
        "filename": file.filename,
        "sha256": sha256_hash,
    }