# Part 2: Architecture and Reasoning

## System architecture and scalability

Pipeline:

1. Extract
- Read File 1 rows (parent and child items).
- Extract PDF text from File 2.
- Build item-bounded text blocks using child item start markers.

2. Parse
- Lane A: deterministic parser for known instruction patterns.
- Lane B: LLM structured fallback only for ambiguous or inconsistent cases.

3. Compute
- Convert parsed percentages into numeric action amounts per child row.
- Aggregate child totals into parent rows only.

4. Validate
- Coverage: all expected child items processed.
- Split checks: percentages in range and no invalid overflows.
- Reconciliation: parent quantity equals sum of child quantities.
- Unit checks: parent and child unit consistency.

5. Export
- Write output XLSX in File 3 format.
- Write run report JSON with lane usage, errors, and validation issues.

Scale approach:
- Keep deterministic parsing as primary path.
- Use fallback model only when needed.
- Process by item/section so jobs can be parallelized and retried safely.

## Client interaction

To reduce ambiguity, ask client to define:

1. Allowed action vocabulary (reuse/dispose/clean/package/transport).
2. Required instruction pattern with explicit percentages.
3. Rule for `remaining` phrasing.
4. Rounding standard and output decimal policy.
5. Conflict policy when instruction text is inconsistent.
6. Versioning rule for changing specification wording.

## Validation and QA

Programmatic controls:

1. Compare generated output to expected schema and parent-level aggregation rules.
2. Validate child-to-parent conservation checks.
3. Record unresolved/ambiguous items in report with reason codes.
4. Maintain regression tests for known edge cases.

Operational policy:

- `continue` mode: keep processing and flag unresolved items.
- `block` mode: stop run on unresolved ambiguous cases.

## What this prototype demonstrates

1. End-to-end generation from File 1 + File 2 to File 3-format XLSX.
2. Deterministic-first design with controlled LLM fallback.
3. Machine-readable run diagnostics for audit and iteration.
