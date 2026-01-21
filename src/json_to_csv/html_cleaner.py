import re
from html import unescape


class HTMLCleaner:
    """
    Cleans HTML content from text fields such as job descriptions.
    """

    TAG_RE = re.compile(r"<[^>]+>")

    @staticmethod
    def clean(text: str | None) -> str | None:
        if not text or not isinstance(text, str):
            return None

        # Decode HTML entities
        text = unescape(text)

        # Remove HTML tags
        text = HTMLCleaner.TAG_RE.sub(" ", text)

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text).strip()

        return text
