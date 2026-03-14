#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from part2_pipeline import deterministic_parse, decide_lane_b_reason


def run() -> int:
    cases = [
        {
            "name": "deterministic_reuse_dispose_split",
            "instruction": "50% must be reused locally. The remaining 50% must be disposed of.",
            "expect_lane_b": False,
        },
        {
            "name": "deterministic_reuse_clean",
            "instruction": "All materials (100%) must be reused locally and fully (100%) cleaned.",
            "expect_lane_b": False,
        },
        {
            "name": "ambiguous_no_action_words",
            "instruction": "Handle released materials according to policy.",
            "expect_lane_b": True,
        },
        {
            "name": "remaining_clause_without_percentage",
            "instruction": "50% must be reused. The remaining must be disposed of.",
            "expect_lane_b": True,
        },
        {
            "name": "over_100_conflict",
            "instruction": "80% must be reused and 40% disposed of.",
            "expect_lane_b": True,
        },
    ]

    failures = []
    for i, case in enumerate(cases, start=1):
        parsed = deterministic_parse(str(900000 + i), case["instruction"])
        reason = decide_lane_b_reason(parsed)
        got_lane_b = reason is not None
        if got_lane_b != case["expect_lane_b"]:
            failures.append(
                {
                    "name": case["name"],
                    "expected_lane_b": case["expect_lane_b"],
                    "got_lane_b": got_lane_b,
                    "reason": reason,
                    "notes": parsed.notes,
                }
            )

    if failures:
        print("SYNTHETIC TESTS FAILED")
        for f in failures:
            print(f)
        return 1

    print("SYNTHETIC TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
