# Part 2 Architecture Note (Excel + PDF -> Output Excel)

## What I built

I implemented a working prototype that:

1. Reads File 1 (Excel) and detects parent/child item rows.
2. Extracts text from File 2 (PDF) and links each child item to its `Instruction:` block.
3. Converts instruction language into deterministic action percentages.
4. Calculates action quantities per child and aggregates final values at parent level only.
5. Generates an output XLSX matching File 3 structure and validates it.

The output format is XLSX (not CSV) to match the expected deliverable and preserve structure/formatting for Google Sheets import.

## Architecture (scaled view)

Pipeline stages:

- Extract: deterministic extraction from Excel + PDF text.
- Parse:
  - Lane A deterministic parser for common phrasing.
  - Lane B structured LLM fallback only when Lane A is uncertain/inconsistent.
- Compute: deterministic math + parent-level aggregation.
- Validate: coverage, split sanity, parent-child reconciliation, schema checks.
- Export: final XLSX + run report.

This separation keeps language interpretation bounded while math and accounting stay fully deterministic.

## Lane logic

Lane A runs first for every item.  
Lane B is triggered only if:

- Lane A confidence is low,
- `remaining` logic is unresolved,
- extracted percentages are inconsistent (for example, split > 100%),
- or no actionable extraction is detected.

Ambiguous behavior is configurable:

- `continue` (default): continue processing and flag issue in report.
- `block`: stop run immediately.

## Reliability and integrity controls

- Continue-on-error mode available for ambiguous/fallback failures.
- Every run outputs a machine-readable report with lane usage and error details.
- Validation checks include:
  - all expected child rows processed,
  - percentages in valid range,
  - no invalid split overflow,
  - parent quantity equals sum of child quantities.

## Client standardization requests

To reduce ambiguity at scale, I would require:

1. Canonical action verb dictionary (`reuse`, `dispose`, `clean`, `package`, `transport`).
2. Explicit percentage wording standard (no vague language).
3. Rule for `remaining` phrasing (must include numeric remainder).
4. Rounding policy (implemented as ROUND_HALF_UP to 2 decimals at output).
5. Conflict and missing-instruction policy.
6. Document versioning/change log for evolving instruction language.

## Why this scales to hundreds of pages

- Deterministic parsing handles the majority of rows cheaply.
- LLM usage is fallback-only and schema-constrained.
- Processing is item/section-addressable, so it can be parallelized and retried without reprocessing entire documents.
- Validation and reporting create an auditable feedback loop to improve parser coverage over time.
