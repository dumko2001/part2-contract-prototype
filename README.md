# Part 2 Prototype

This folder now includes an end-to-end **Part 2** prototype:

- `part2_pipeline.py`: Excel + PDF -> generated output Excel
- `artifacts/part2_run_report.json`: parse and reliability report
- `artifacts/FILE_3_GENERATED.xlsx`: generated file in File 3 shape
- `synthetic_tests.py`: synthetic edge-case tests for lane switching

## Required input files

These files are included in this folder by default:

- `[FILE 1]_ subset of registration status.xlsx`
- `FILE 2 subset.pdf`
- `FILE 3 OUTPUT.xlsx` (used by validator)

You can still pass custom locations via CLI flags.

## Quick start

```bash
cd "/Users/sidharth/Downloads/Map for case study/part2_prototype"
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python part2_pipeline.py
.venv/bin/python validate_generated_output.py
.venv/bin/python synthetic_tests.py
```

## Run with custom file paths

```bash
.venv/bin/python part2_pipeline.py \
  --file1 "/absolute/path/to/file1.xlsx" \
  --file2 "/absolute/path/to/file2.pdf" \
  --output "/absolute/path/to/output.xlsx" \
  --report "/absolute/path/to/run_report.json"
```

## Environment setup (Groq)

```bash
cp .env.example .env
# edit .env and set GROQ_API_KEY
```

Optional Groq fallback (Lane B):

1. Copy `.env.example` to `.env`
2. Set `GROQ_API_KEY`
3. Run again

Force fallback test (integration test of Lane B):

```bash
GROQ_API_KEY=... .venv/bin/python part2_pipeline.py --force-lane-b --groq-model openai/gpt-oss-20b
```

## Notes

- Lane A is deterministic parser and should solve this sample directly.
- Lane B uses Groq structured output only for ambiguous lines.
- Missing instructions do not stop processing; they are reported in JSON.
- `lane_a=14, lane_b=0` means:
  - all 14 child instructions were solved by deterministic parser,
  - no LLM fallback was needed for this sample.
- Lane B is used when:
  - deterministic confidence is low,
  - or "remaining ..." logic is unresolved,
  - or split is inconsistent (for example over 100%),
  - or no action could be extracted.
- Reliability upgrades implemented:
  - instruction extraction uses item-bounded blocks (item start to next item), not blank-line-only stops,
  - instruction trace in report includes `page`, `item_code`, and `block_hash`,
  - action-signal check (`%` or known action verbs) is recorded per item.
- Ambiguous handling policy:
  - `--ambiguous-policy continue` (default): continue run, flag item in report `errors`.
  - `--ambiguous-policy block`: stop run immediately on unresolved/failed fallback item.
- Output file is XLSX (not CSV) because your expected file is XLSX and Google Sheets imports XLSX directly.
- Formatting:
  - header row is bold,
  - parent item rows are bold,
  - child rows are normal.
