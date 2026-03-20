from __future__ import annotations

import argparse
import csv
import json
import re
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

try:
    from PyPDF2 import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None


ALGORITHM_PATTERNS = [
    "PARAFAC",
    "KMethod",
    "K-PARAFAC",
    "PFFLR",
    "PLD",
    "MR-PLD",
    "SOM",
    "inner filter effect",
    "Raman normalization",
]

STANDARD_PATTERNS = [
    "glucosamine",
    "muramic acid",
    "humic acid",
    "BSA",
    "protein",
    "bacteria",
]

EX_EM_PATTERNS = [
    re.compile(
        r"(?:excitation|lambdaexcitation|[Ll][\u03bb]?excitation)?\s*[:=/\[]*\s*"
        r"(?P<ex_start>\d{3})\s*(?:-|to|,)\s*(?P<ex_end>\d{3})\s*[\]/)]*\s*nm?"
        r".{0,80}?"
        r"(?:emission|lambdaemission|[Ll][\u03bb]?emission)?\s*[:=/\[]*\s*"
        r"(?P<em_start>\d{3})\s*(?:-|to|,)\s*(?P<em_end>\d{3})\s*[\]/)]*\s*nm?",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"\[\s*(?P<ex_start>\d{3})\s*,\s*(?P<ex_end>\d{3})\s*\]\s*/\s*"
        r"\[\s*(?P<em_start>\d{3})\s*,\s*(?P<em_end>\d{3})\s*\]\s*nm",
        re.IGNORECASE,
    ),
    re.compile(
        r"excitation\s+range\s*[:=]\s*(?P<ex_start>\d{3})\s*(?:-|to)\s*(?P<ex_end>\d{3})\s*nm"
        r".{0,120}?"
        r"emission\s+range\s*[:=]\s*(?P<em_start>\d{3})\s*(?:-|to)\s*(?P<em_end>\d{3})\s*nm",
        re.IGNORECASE | re.DOTALL,
    ),
]

DOI_PATTERN = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Z0-9]+)\b", re.IGNORECASE)
URL_PATTERN = re.compile(r"https?://[^\s<>\"]+", re.IGNORECASE)
YEAR_PATTERN = re.compile(r"\b(?:19|20)\d{2}\b")
AUTHOR_YEAR_PATTERN = re.compile(r"\b([A-Z][A-Za-z-]+(?:\s+et\s+al\.)?,?\s+\((?:19|20)\d{2}\))")
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_whitespace(text: str) -> str:
    return WHITESPACE_PATTERN.sub(" ", text).strip()


def strip_html(html: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = HTML_TAG_PATTERN.sub(" ", text)
    return normalize_whitespace(unescape(text))


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def looks_like_doi(value: str) -> bool:
    stripped = value.strip()
    return stripped.lower().startswith("doi:") or bool(DOI_PATTERN.fullmatch(stripped))


def doi_to_url(value: str) -> str:
    cleaned = value.strip()
    if cleaned.lower().startswith("doi:"):
        cleaned = cleaned.split(":", 1)[1].strip()
    return f"https://doi.org/{cleaned}"


def fetch_url_text(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "necromass-eems-paper-miner/1.0",
            "Accept": "text/html,application/pdf,text/plain,*/*",
        },
    )
    with urlopen(request, timeout=30) as response:
        content_type = response.headers.get_content_type()
        payload = response.read()

    if content_type == "application/pdf":
        if PdfReader is None:
            raise RuntimeError("PyPDF2 is required to parse PDF URLs.")
        from io import BytesIO

        reader = PdfReader(BytesIO(payload))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    try:
        decoded = payload.decode("utf-8")
    except UnicodeDecodeError:
        decoded = payload.decode("latin-1", errors="ignore")

    if "html" in content_type or "<html" in decoded.lower():
        return strip_html(decoded)
    return decoded


def read_text(input_path: Path) -> str:
    if input_path.suffix.lower() == ".pdf":
        if PdfReader is None:
            raise RuntimeError("PyPDF2 is required to parse PDF files.")
        reader = PdfReader(str(input_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return input_path.read_text(encoding="utf-8", errors="ignore")


def load_source_lists(list_paths: list[str]) -> list[str]:
    expanded = []
    for value in list_paths:
        path = Path(value)
        if not path.exists():
            raise FileNotFoundError(f"List file not found: {value}")
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            nested = line.strip()
            if nested and not nested.startswith("#"):
                expanded.append(nested)
    return expanded


def load_sources(input_values: list[str]) -> list[dict]:
    sources = []

    for raw_value in input_values:
        value = raw_value.strip()
        if not value:
            continue

        path = Path(value)
        if path.exists():
            sources.append(
                {
                    "source_id": path.stem,
                    "source_kind": "local_file",
                    "source_reference": str(path),
                    "text": read_text(path),
                }
            )
            continue

        if looks_like_doi(value):
            url = doi_to_url(value)
            sources.append(
                {
                    "source_id": value.replace("/", "_"),
                    "source_kind": "doi",
                    "source_reference": value,
                    "text": fetch_url_text(url),
                    "resolved_url": url,
                }
            )
            continue

        if is_url(value):
            sources.append(
                {
                    "source_id": urlparse(value).netloc.replace(".", "_"),
                    "source_kind": "url",
                    "source_reference": value,
                    "text": fetch_url_text(value),
                }
            )
            continue

        raise FileNotFoundError(f"Input not found or unsupported source: {value}")

    return sources


def extract_windows(text: str) -> list[dict]:
    windows = []
    seen = set()
    for pattern in EX_EM_PATTERNS:
        for match in pattern.finditer(text):
            key = (
                match.group("ex_start"),
                match.group("ex_end"),
                match.group("em_start"),
                match.group("em_end"),
                match.start(),
            )
            if key in seen:
                continue
            seen.add(key)
            windows.append(
                {
                    "excitation_range_nm": f"{match.group('ex_start')}-{match.group('ex_end')}",
                    "emission_range_nm": f"{match.group('em_start')}-{match.group('em_end')}",
                    "context_snippet": normalize_whitespace(
                        text[max(0, match.start() - 100): match.end() + 100]
                    ),
                }
            )
    return windows


def extract_citation_hints(text: str) -> list[str]:
    hints = set()
    for doi in DOI_PATTERN.findall(text):
        hints.add(doi)
    for url in URL_PATTERN.findall(text):
        hints.add(url.rstrip(".,);"))
    for author_year in AUTHOR_YEAR_PATTERN.findall(text):
        hints.add(author_year)
    return sorted(hints)


def extract_insights(text: str) -> dict:
    lowered = text.lower()

    algorithms = sorted({pattern for pattern in ALGORITHM_PATTERNS if pattern.lower() in lowered})
    standards = sorted({pattern for pattern in STANDARD_PATTERNS if pattern.lower() in lowered})
    windows = extract_windows(text)
    citation_hints = extract_citation_hints(text)
    years = sorted(set(YEAR_PATTERN.findall(text)))

    return {
        "algorithms": algorithms,
        "standards": standards,
        "spectral_windows": windows,
        "citation_hints": citation_hints,
        "years_mentioned": years,
    }


def summarize_source(source: dict) -> dict:
    insights = extract_insights(source["text"])
    return {
        "source_id": source["source_id"],
        "source_kind": source["source_kind"],
        "source_reference": source["source_reference"],
        "resolved_url": source.get("resolved_url"),
        "algorithms": insights["algorithms"],
        "standards": insights["standards"],
        "spectral_windows": insights["spectral_windows"],
        "citation_hints": insights["citation_hints"],
        "years_mentioned": insights["years_mentioned"],
    }


def flatten_rows(source_summary: dict) -> list[dict]:
    base_row = {
        "source_id": source_summary["source_id"],
        "source_kind": source_summary["source_kind"],
        "source_reference": source_summary["source_reference"],
        "resolved_url": source_summary.get("resolved_url") or "",
        "algorithms": "; ".join(source_summary["algorithms"]),
        "standards": "; ".join(source_summary["standards"]),
        "citation_hints": "; ".join(source_summary["citation_hints"]),
        "years_mentioned": "; ".join(source_summary["years_mentioned"]),
    }

    if not source_summary["spectral_windows"]:
        return [
            {
                **base_row,
                "excitation_range_nm": "",
                "emission_range_nm": "",
                "context_snippet": "",
            }
        ]

    rows = []
    for window in source_summary["spectral_windows"]:
        rows.append(
            {
                **base_row,
                "excitation_range_nm": window["excitation_range_nm"],
                "emission_range_nm": window["emission_range_nm"],
                "context_snippet": window["context_snippet"],
            }
        )
    return rows


def write_csv(rows: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source_id",
        "source_kind",
        "source_reference",
        "resolved_url",
        "algorithms",
        "standards",
        "excitation_range_nm",
        "emission_range_nm",
        "context_snippet",
        "citation_hints",
        "years_mentioned",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract EEM paper insights from local files, DOI lists, or URLs.")
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        help="Local file, DOI, or URL. Repeatable.",
    )
    parser.add_argument(
        "--input-list",
        action="append",
        default=[],
        help="Text or CSV file containing one local path, DOI, or URL per line. Repeatable.",
    )
    parser.add_argument("--output", required=True, help="JSON output path")
    parser.add_argument("--table-output", help="CSV summary output path")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    table_output_path = Path(args.table_output) if args.table_output else output_path.with_suffix(".csv")

    try:
        input_values = list(args.input) + load_source_lists(args.input_list)
    except FileNotFoundError as exc:
        raise SystemExit(str(exc)) from exc

    if not input_values:
        raise SystemExit("Provide at least one --input or --input-list value.")

    try:
        sources = load_sources(input_values)
    except (FileNotFoundError, HTTPError, URLError, RuntimeError) as exc:
        raise SystemExit(str(exc)) from exc

    summaries = [summarize_source(source) for source in sources]
    combined = {
        "source_count": len(summaries),
        "sources": summaries,
        "unique_algorithms": sorted({item for summary in summaries for item in summary["algorithms"]}),
        "unique_standards": sorted({item for summary in summaries for item in summary["standards"]}),
        "unique_citation_hints": sorted({item for summary in summaries for item in summary["citation_hints"]}),
    }
    rows = [row for summary in summaries for row in flatten_rows(summary)]

    output_path.write_text(json.dumps(combined, indent=2), encoding="utf-8")
    write_csv(rows, table_output_path)
    print(f"Wrote JSON summary to {output_path}")
    print(f"Wrote CSV summary to {table_output_path}")


if __name__ == "__main__":
    main()
