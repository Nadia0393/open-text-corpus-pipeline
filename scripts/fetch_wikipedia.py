"""Download a sample of English Wikipedia articles to JSONL."""

import json
from pathlib import Path

from datasets import load_dataset

OUTPUT = Path("data/raw/wikipedia_sample.jsonl")
SAMPLE_SIZE = 10_000


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    # Streaming avoids downloading the full multi-GB dump.
    ds = load_dataset("wikimedia/wikipedia", "20231101.en", split="train", streaming=True)

    written = 0
    with OUTPUT.open("w", encoding="utf-8") as f:
        for article in ds:
            record = {
                "source_id": article["id"],
                "url": article["url"],
                "title": article["title"],
                "text": article["text"],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1
            if written >= SAMPLE_SIZE:
                break

    print(f"Wrote {written} articles to {OUTPUT}")


if __name__ == "__main__":
    main()
