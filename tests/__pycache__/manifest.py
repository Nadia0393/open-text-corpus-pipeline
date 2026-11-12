"""Per-run manifest: a JSON record of what went in, what came out, and which code produced it."""

import json
import subprocess
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

REQUIRED_KEYS = {
    "source",
    "input_path",
    "output_path",
    "rows_in",
    "rows_out",
    "pipeline_version",
    "pyspark_version",
    "git_commit",
    "created_at",
}


def get_git_commit() -> str:
    """Return the current commit SHA, or 'unknown' outside a git checkout."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=False
    )
    return result.stdout.strip() or "unknown"


def _package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "unknown"


def build_manifest(
    source: str,
    input_path: str,
    output_path: str,
    rows_in: int,
    rows_out: int,
) -> dict:
    return {
        "source": source,
        "input_path": input_path,
        "output_path": output_path,
        "rows_in": rows_in,
        "rows_out": rows_out,
        "pipeline_version": _package_version("open-text-corpus-pipeline"),
        "pyspark_version": _package_version("pyspark"),
        "git_commit": get_git_commit(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def write_manifest(manifest: dict, path: str | Path) -> Path:
    missing = REQUIRED_KEYS - manifest.keys()
    if missing:
        raise ValueError(f"Manifest missing keys: {sorted(missing)}")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path