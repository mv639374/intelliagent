import re
from typing import Dict

from langdetect import LangDetectException, detect


class Preprocessor:
    """
    A class for preprocessing text content before indexing.
    """

    def process(self, text: str) -> Dict:
        """
        Cleans text and detects its language.
        """
        cleaned_text = self._normalize_whitespace(text)

        try:
            language = detect(cleaned_text[:500])  # Use a sample for speed
        except LangDetectException:
            language = "unknown"

        return {"cleaned_text": cleaned_text, "language": language}

    def _normalize_whitespace(self, text: str) -> str:
        """
        Replaces multiple whitespace characters with a single space.
        """
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        return text
