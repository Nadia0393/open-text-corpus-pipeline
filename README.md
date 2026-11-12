# open-text-corpus-pipeline

A PySpark pipeline that turns raw public web text into a deduplicated, quality-filtered, versioned dataset, with a manifest for every run. The goal is a reproducible training-data curation workflow in the style of work done for language model pretraining and evaluation.

**Current status:** Bronze layer only. Raw JSONL is ingested, given stable identifiers and content hashes, written as partitioned Parquet, and recorded in a manifest. Normalization, quality filters, deduplication, and the Iceberg output are not yet implemented.

## Data

The pipeline uses the English Wikipedia snapshot `20231101.en` from the Hugging Face dataset `wikimedia/wikipedia`. Wikipedia content is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). If you redistribute derived data, you must keep that license and give attribution.

Raw and derived data are not stored in this repository. The `data/` directory is git-ignored. To fetch a sample of 10,000 articles:

```bash
uv run python scripts/fetch_wikipedia.py
```

This writes `data/raw/wikipedia_sample.jsonl`.

## Running the Bronze layer

Requirements: Python 3.11, Java 17 (Spark needs a JVM), and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --all-extras --dev
uv run python scripts/fetch_wikipedia.py
uv run python -m open_text_corpus_pipeline.ingest.run_bronze
```

The last command writes:

- `data/bronze/wikipedia/`: Parquet partitioned by `ingest_date`
- `data/manifests/bronze-<date>.json`: the run manifest

Run the tests with:

```bash
uv run ruff check .
uv run pytest -q
```

## Design decisions

**Stable `doc_id`.** Each document ID is built from the source name and the Wikipedia page ID (`wikipedia-20231101-en:<page_id>`). Rerunning on the same input produces the same IDs, so downstream joins and deduplication stay consistent. A random UUID would change on every run.

**Content hash.** `content_hash` is the SHA-256 of the article text. Identical text gives identical hashes, which makes exact-duplicate detection a simple grouping step. Any change to the text changes the hash.

**`ingested_at` is excluded from the hash.** It changes on every run, so including it would make identical content look different each time. Only the metadata changes between runs. The content does not.

**Manifest per run.** Parquet has no transaction log, so each run writes a JSON manifest recording the source, input and output paths, row counts in and out, the package and PySpark versions, the git commit, and a UTC timestamp. The manifest is what makes a run traceable and reproducible. The write step refuses to save a manifest with missing keys.

## Tests

Tests cover:

- content hash determinism, and sensitivity to a one-character change
- `doc_id` stability across runs
- no null or duplicate `doc_id` values in Bronze output
- manifest completeness

Spark starts once per test session through a shared fixture in `tests/conftest.py`.

## Limitations

- **Manifest does not record a dirty working tree.** If code has uncommitted changes when a run happens, the manifest records the last commit, not the code that actually ran.
- **No checksum on the input file.** The manifest records the input path but not its content hash, so it can't detect that the input changed between runs.
- **Only tested on a 10,000-article sample.** Performance and behavior at full scale are unmeasured.
- **Dependency versions are only partly recorded.** The manifest captures the package and PySpark versions, but not the Java version or the full lockfile state.

## Roadmap

1. Silver layer: text normalization, language tagging, and quality filters with per-filter counts
2. Exact deduplication on `content_hash`
3. Near-duplicate removal with MinHash and LSH
4. Iceberg output with snapshot-based time travel
5. Quality gates that fail the run on threshold breaches
6. Evaluation contamination check against a held-out set

## License

Code is licensed under the MIT License. See [LICENSE](LICENSE). The Wikipedia data is licensed separately under CC BY-SA 4.0, as noted above.