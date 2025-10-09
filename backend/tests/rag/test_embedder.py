from app.rag.embedder import Embedder


def test_embedder_shape():
    embedder = Embedder()
    embeddings = embedder.embed_texts(["hello", "world"])
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384  # all-MiniLM-L6-v2 dimension
