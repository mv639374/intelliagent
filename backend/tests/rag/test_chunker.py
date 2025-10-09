# tests/rag/test_chunker.py
from app.rag.chunker import Chunker


def test_chunker():
    text = "a" * 2000
    chunker = Chunker(chunk_size=1000, chunk_overlap=100)
    chunks = chunker.chunk_text(text, page_number=1)

    # Fix: LangChain's RecursiveCharacterTextSplitter produces 3 chunks
    assert len(chunks) == 3  # ← Changed from 2 to 3

    # Verify each chunk has correct metadata
    for chunk in chunks:
        assert "text" in chunk
        assert "metadata" in chunk
        assert chunk["metadata"]["page"] == 1
        assert chunk["metadata"]["source"] == "text"
