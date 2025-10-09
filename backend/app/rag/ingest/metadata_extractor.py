import io
from typing import Any, Dict

import docx
import pdfplumber


class MetadataExtractor:
    """
    Extracts metadata from various file types.
    """

    def extract(self, content: bytes, mime_type: str) -> Dict[str, Any]:
        if "pdf" in mime_type:
            return self._extract_pdf_metadata(content)
        elif "openxmlformats-officedocument.wordprocessingml" in mime_type:
            return self._extract_docx_metadata(content)
        return {}

    def _extract_pdf_metadata(self, content: bytes) -> Dict[str, Any]:
        metadata = {}
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                doc_metadata = pdf.metadata
                metadata["title"] = doc_metadata.get("Title")
                metadata["author"] = doc_metadata.get("Author")
                metadata["page_count"] = len(pdf.pages)
        except Exception as e:
            print(f"Error extracting PDF metadata: {e}")
        return metadata

    def _extract_docx_metadata(self, content: bytes) -> Dict[str, Any]:
        metadata = {}
        try:
            doc = docx.Document(io.BytesIO(content))
            core_props = doc.core_properties
            metadata["title"] = core_props.title
            metadata["author"] = core_props.author
            metadata["created"] = core_props.created
            metadata["modified"] = core_props.modified
        except Exception as e:
            print(f"Error extracting DOCX metadata: {e}")
        return metadata
