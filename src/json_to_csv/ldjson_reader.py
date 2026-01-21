import json
from typing import Generator, Dict, Any
from pathlib import Path


class LDJSONReader:
    """
    Reads LDJSON / JSONL files safely and efficiently.

    Each line must be a valid JSON object.
    Invalid lines are skipped but logged.
    """

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(f"LDJSON file not found: {self.file_path}")

        if self.file_path.suffix not in {".ldjson", ".jsonl", ".json"}:
            raise ValueError(
                "Invalid file type. Expected .ldjson, .jsonl, or .json"
            )

    def read(self) -> Generator[Dict[str, Any], None, None]:
        """
        Generator that yields one JSON object per line.

        Yields:
            dict: Parsed JSON object
        """
        with self.file_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    yield json.loads(line)
                except json.JSONDecodeError as e:
                    print(
                        f"[LDJSONReader] Skipping invalid JSON "
                        f"(line {line_number}): {e}"
                    )

    def read_all(self) -> list[Dict[str, Any]]:
        """
        Reads the entire file into memory.

        Use only for small-to-medium datasets.
        """
        return list(self.read())
