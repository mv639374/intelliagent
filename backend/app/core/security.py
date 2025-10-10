from app.rag.ingest.pii_redactor import PIIRedactor
from typing import List, Dict, Any

# Singleton instance of the redactor
pii_redactor = PIIRedactor()

def mask_pii_in_results(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Applies PII redaction to the 'text' field of each chunk in a list.
    
    In a real application, this would be conditionally applied based on
    the user's role or a project-level policy.
    """
    for chunk in chunks:
        if "text" in chunk:
            chunk["text"] = pii_redactor.redact(chunk["text"])
    return chunks