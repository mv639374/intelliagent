import hashlib
from io import BytesIO

import pytest
from fastapi import UploadFile

from app.rag.ingest.file_connector import FileConnector


@pytest.mark.asyncio
async def test_file_connector_fetch():
    """
    Tests that the FileConnector correctly computes the sha256 hash
    and returns the expected metadata.
    """
    # 1. Prepare a mock file
    file_content = b"This is a test file for the connector."
    file_name = "test_connector.txt"
    file_obj = BytesIO(file_content)
    mock_upload_file = UploadFile(filename=file_name, file=file_obj)

    # 2. Instantiate the connector and fetch
    connector = FileConnector()
    results = await connector.fetch(mock_upload_file)

    # 3. Assertions
    assert len(results) == 1
    doc = results[0]

    # Check metadata
    assert doc["metadata"]["filename"] == file_name
    assert doc["metadata"]["size_bytes"] == len(file_content)

    # Check sha256 hash
    expected_hash = hashlib.sha256(file_content).hexdigest()
    assert doc["metadata"]["sha256"] == expected_hash

    # Check content
    assert doc["content"] == file_content
