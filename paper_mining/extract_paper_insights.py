from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

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

WAVELENGTH_PATTERN = re.compile(
    r"(?P<ex_start>\d{3})\s*[-to]+\s*(?P<ex_end>\d{3})\s*nm.*?(?P<em_start>\d{3})\s*[-to]+\s*(?P<em_end>\d{3})\s*nm",
    re.IGNORECASE | re.DOTALL,
)


def read_text(input_path: Path) -> str:
    if input_path.suffix.lower() == ".pdf":
        if PdfReader is None:
            raise RuntimeError("PyPDF2 is required to parse PDF files.")
        reader = PdfReader(str(input_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return input_path.read_text(encoding="utf-8", errors="ignore")


def extract_insights(text: str) -> dict:
    lowered = text.lower()

    algorithms = sorted({pattern for pattern in ALGORITHM_PATTERNS if pattern.lower() in lowered})
    standards = sorted({pattern for pattern in STANDARD_PATTERNS if pattern.lower() in lowered})

    windows = []
    for match in WAVELENGTH_PATTERN.finditer(text):
        windows.append(
            {
                "excitation_range_nm": f"{match.group('ex_start')}-{match.group('ex_end')}",
                "emission_range_nm": f"{match.group('em_start')}-{match.group('em_end')}",
                "context_snippet": text[max(0, match.start() - 80): match.end() + 80].replace("\n", " "),
            }
        )

    return {
        "algorithms": algorithms,
        "standards": standards,
        "spectral_windows": windows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract EEM paper insights from text or PDF files.")
    parser.add_argument("--input", required=True, help="Path to a paper in .txt, .md, or .pdf format")
    parser.add_argument("--output", required=True, help="JSON output path")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    text = read_text(input_path)
    insights = extract_insights(text)
    output_path.write_text(json.dumps(insights, indent=2), encoding="utf-8")
    print(f"Wrote insights to {output_path}")


if __name__ == "__main__":
    main()
