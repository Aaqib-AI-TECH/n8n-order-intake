"""HTTP wrapper around the Experiment 1 print brief extractor.

This exposes the local extractor as a small web service so the n8n workflow's
HTTP Request node can call it. Run this in the same virtual environment that has
Experiment 1 working (the one with llama-cpp-python and the GGUF model).

Every extraction is also appended to data/intake_log.csv, so there is a local
record of captured orders even before Google Sheets is wired up.

Run:
    uvicorn api_server:app --host 0.0.0.0 --port 8000

Host 0.0.0.0 matters: it lets n8n running in Docker reach this service at
http://host.docker.internal:8000.
"""

from __future__ import annotations

import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

# Point this at your Experiment 1 project folder so we can import its extractor.
EXP1_PATH = os.environ.get(
    "EXP1_PATH",
    r"C:\Users\e16008577\Downloads\RP72026\github\print-brief-extractor",
)
sys.path.insert(0, EXP1_PATH)

try:
    from extractor import extract_brief  # noqa: E402  (from Experiment 1)
    from schema import ALL_FIELDS  # noqa: E402
except Exception as exc:  # pragma: no cover
    raise RuntimeError(
        f"Could not import the Experiment 1 extractor from {EXP1_PATH}. "
        "Set EXP1_PATH to your print-brief-extractor folder, e.g.\n"
        '  $env:EXP1_PATH = "C:\\Users\\e16008577\\Downloads\\RP72026\\github\\print-brief-extractor"'
    ) from exc

app = FastAPI(title="Print Brief Extractor API", version="1.0")

LOG_PATH = Path("data/intake_log.csv")
LOG_FIELDS = ["received_at"] + ALL_FIELDS


class Brief(BaseModel):
    text: str


def _log(record: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    new_file = not LOG_PATH.exists()
    with LOG_PATH.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=LOG_FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        writer.writerow(record)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/extract")
def extract(brief: Brief) -> dict:
    fields = extract_brief(brief.text).model_dump(mode="json")
    record = {"received_at": datetime.now(timezone.utc).isoformat(), **fields}
    _log(record)
    return record
