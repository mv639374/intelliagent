from typing import List, Dict, Any

class Citation:
    def __init__(self, source: str, text_snippet: str, score: float, doc_id: str, chunk_id: str):
        self.source = source
        self.text_snippet = text_snippet
        self.score = score
        self.document_id = doc_id
        self.chunk_id = chunk_id

    def to_dict(self):
        return {
            "source": self.source,
            "text_snippet": self.text_snippet,
            "score": self.score,
            "document_id": self.document_id,
            "chunk_id": self.chunk_id,
        }

def format_citations(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Formats the final list of chunks into a structured citation format.
    
    This function would typically involve a database lookup to get the
    original document filename from the document_id. For this test,
    we'll use a placeholder.
    """
    citations = []
    for chunk in chunks:
        metadata = chunk.get("metadata", {})
        doc_id = metadata.get("document_id", "Unknown")
        page_num = metadata.get("page", 1)

        # In a real app: filename = lookup_filename(doc_id)
        filename = f"Document-{doc_id[:8]}" 
        
        citation = Citation(
            source=f"{filename} (Page {page_num})",
            text_snippet=chunk.get("text", ""),
            score=chunk.get("score", 0.0),
            doc_id=doc_id,
            chunk_id=chunk.get("chunk_id", "Unknown"),
        )
        citations.append(citation.to_dict())
        
    return citations