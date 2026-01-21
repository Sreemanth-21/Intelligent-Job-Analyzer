import pandas as pd
from pathlib import Path

from .ldjson_reader import LDJSONReader
from .schema_mapper import SchemaMapper


def run_part1(
    input_ldjson: str,
    output_csv: str,
    output_parquet: str | None = None,
):
    reader = LDJSONReader(input_ldjson)
    mapper = SchemaMapper()

    records = []

    for raw_job in reader.read():
        mapped_job = mapper.map(raw_job)
        records.append(mapped_job)

    if not records:
        raise ValueError("No valid job records found.")

    df = pd.DataFrame(records)

    # Ensure output directory exists
    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_csv, index=False)

    if output_parquet:
        df.to_parquet(output_parquet, index=False)

    print("✅ PART 1 completed successfully")
    print(f"📄 Rows: {len(df)}")
    print(f"📄 Columns: {len(df.columns)}")
    print(f"💾 CSV saved to: {output_csv}")

    if output_parquet:
        print(f"💾 Parquet saved to: {output_parquet}")


if __name__ == "__main__":
    run_part1(
        input_ldjson="data/raw/jobs.ldjson",
        output_csv="data/interim/jobs_clean_raw.csv",
        output_parquet="data/interim/jobs_clean_raw.parquet",
    )
    