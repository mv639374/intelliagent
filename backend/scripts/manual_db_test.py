import asyncio
import uuid
import hashlib

from sqlalchemy.future import select

# This script assumes it is run from the `backend/` directory.
# All imports are relative to the `backend/` root.
from app.db.session import AsyncSessionLocal
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.document import Document, DocumentStatus

async def run_db_test():
    """
    Connects to the database and performs a series of write operations
    to validate the schema and models.
    """
    print("--- Starting Manual Database Test ---")

    # The AsyncSessionLocal factory returns an async session when called
    async with AsyncSessionLocal() as session:
        async with session.begin(): # Start a transaction
            print("✅ Session created successfully.")

            # 1. Create a User
            test_user = User(
                username="testuser",
                email="test@example.com",
                hashed_password="fakehashedpassword",
                role=UserRole.ADMIN
            )
            session.add(test_user)
            await session.flush() # Flush to get the user's generated ID
            print(f"✅ User '{test_user.username}' created with ID: {test_user.id}")

            # 2. Create a Project associated with the User
            test_project = Project(
                name="Test Project",
                description="A project for manual testing.",
                owner_id=test_user.id
            )
            session.add(test_project)
            await session.flush() # Flush to get the project's generated ID
            print(f"✅ Project '{test_project.name}' created with ID: {test_project.id}")

            # 3. Create a Document associated with the User and Project
            # Generate a fake SHA256 hash for the document
            file_content = b"this is a test document"
            sha256_hash = hashlib.sha256(file_content).hexdigest()

            test_document = Document(
                project_id=test_project.id,
                filename="test_document.txt",
                mime_type="text/plain",
                size_bytes=len(file_content),
                sha256=sha256_hash,
                status=DocumentStatus.PENDING,
                owner_id=test_user.id
            )
            session.add(test_document)
            await session.flush()
            print(f"✅ Document '{test_document.filename}' created with ID: {test_document.id}")

            # The 'async with session.begin():' block will automatically commit here.
            print("\n✅ Transaction committing...")

    print("--- Manual Database Test Completed Successfully ---")


if __name__ == "__main__":
    # Ensure Docker services (especially postgres) are running before executing
    print("Ensure your Docker services are running (`make run-dev`).")
    asyncio.run(run_db_test())