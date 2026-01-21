from typing import Dict, Any
from datetime import datetime
from .html_cleaner import HTMLCleaner


class SchemaMapper:
    """
    Maps raw job JSON into a clean, structured schema.
    """

    REQUIRED_FIELDS = {
        "job_id": ["id", "job_id"],
        "job_title": ["title", "job_title"],
        "company": ["company", "company_name"],
        "location": ["location", "job_location"],
        "description": ["description", "job_description"],
        "posted_date": ["posted_date", "created_at"],
        "expiry_date": ["expiry_date", "valid_until"],
        "salary_min": ["salary_min"],
        "salary_max": ["salary_max"],
        "experience": ["experience", "experience_required"],
    }

    def extract_field(self, source: Dict[str, Any], keys: list[str]):
        for key in keys:
            if key in source and source[key] is not None:
                return source[key]
        return None

    def map(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        mapped = {}

        for target_field, source_keys in self.REQUIRED_FIELDS.items():
            mapped[target_field] = self.extract_field(raw_job, source_keys)

        # Clean description HTML
        mapped["description"] = HTMLCleaner.clean(mapped.get("description"))

        # Normalize dates
        mapped["posted_date"] = self._parse_date(mapped.get("posted_date"))
        mapped["expiry_date"] = self._parse_date(mapped.get("expiry_date"))

        return mapped

    def _parse_date(self, date_value):
        if not date_value:
            return None

        if isinstance(date_value, datetime):
            return date_value.date().isoformat()

        if isinstance(date_value, str):
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d-%m-%Y"):
                try:
                    return datetime.strptime(date_value, fmt).date().isoformat()
                except ValueError:
                    continue

        return None
