from typing import Any, Dict, List

from langchain_text_splitters import RecursiveCharacterTextSplitter


class Chunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
            separators=["\n\n", "\n", " ", ""],
        )

    def chunk_text(self, text: str, page_number: int) -> List[Dict[str, Any]]:
        """
        Chunks a single string of text.
        """
        chunks = self.text_splitter.split_text(text)
        return [{"text": chunk, "metadata": {"page": page_number, "source": "text"}} for chunk in chunks]

    def chunk_pages_and_tables(self, page_texts: List[Dict], tables: List[Dict]) -> List[Dict[str, Any]]:
        """
        Chunks text from pages and adds tables as distinct chunks.
        """
        all_chunks = []
        # Chunk text from each page
        for page in page_texts:
            page_num = page["page_number"]
            page_content = page["text"]
            all_chunks.extend(self.chunk_text(page_content, page_num))

        # Add each extracted table as a separate chunk
        for table in tables:
            table_str = "\n".join(["\t".join(map(str, row)) for row in table["table_data"]])
            all_chunks.append(
                {"text": f"Table:\n{table_str}", "metadata": {"page": table["page_number"], "source": "table"}}
            )
        return all_chunks


# Initialize a singleton instance
chunker = Chunker()
