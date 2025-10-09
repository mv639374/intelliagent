import re

import spacy

# Load the spaCy model once when the module is loaded
nlp = spacy.load("en_core_web_sm")


class PIIRedactor:
    """
    Detects and redacts PII from text using regex and spaCy NER.
    """

    def __init__(self):
        # Regex for common PII patterns
        self.regex_patterns = {
            "[EMAIL]": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
            "[PHONE]": re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
            "[SSN]": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        }

    def redact(self, text: str) -> str:
        """
        Applies both regex and NER-based redaction.
        """
        # 1. Regex-based redaction
        for placeholder, pattern in self.regex_patterns.items():
            text = pattern.sub(placeholder, text)

        # 2. NER-based redaction using spaCy
        doc = nlp(text)
        redacted_text = list(text)

        for ent in doc.ents:
            if ent.label_ in ["PERSON", "GPE", "ORG"]:  # GPE = Geopolitical Entity
                start = ent.start_char
                end = ent.end_char
                placeholder = f"[{ent.label_}]"
                redacted_text[start:end] = list(placeholder)

        return "".join(redacted_text)
