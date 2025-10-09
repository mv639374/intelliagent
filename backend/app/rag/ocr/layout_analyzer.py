from typing import Any, Dict, List

import pdfplumber


class LayoutAnalyzer:
    """
    Analyzes the layout of a PDF to extract structured elements like tables.
    """

    def extract_tables(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Uses pdfplumber to find and extract tables from each page.

        Args:
        ----
            file_path: The local path to the PDF file.

        Returns:
        -------
            A list of dictionaries, each representing a table found.

        """
        all_tables = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    for table in tables:
                        all_tables.append(
                            {
                                "page_number": i + 1,
                                "table_data": table,  # List of lists representing rows/cells
                            }
                        )
        except Exception as e:
            print(f"Error extracting tables with pdfplumber: {e}")
        return all_tables
