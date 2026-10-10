#!/usr/bin/env python3
"""Exercise the project's conservative host-suffix rules against fixture cases."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_SETS = ("proxy-services.list", "direct-cn.list")


def load_rules() -> list[tuple[str, str]]:
    rules: list[tuple[str, str]] = []
    for filename in ACTIVE_SETS:
        path = ROOT / "rulesets" / filename
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith(("#", ";")):
                continue
            kind, suffix, policy = (field.strip() for field in line.split(","))
            if kind != "host-suffix":
                raise ValueError(f"unsupported test rule: {line}")
            rules.append((suffix.lower(), policy.lower()))
    return rules


def main() -> int:
    rules = load_rules()
    failures: list[str] = []
    fixture = ROOT / "tests" / "rule-cases.tsv"
    for number, raw in enumerate(fixture.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 2:
            failures.append(f"{fixture.name}:{number}: expected two tab-separated fields")
            continue
        host, expected = fields[0].lower(), fields[1]
        actual = "final:proxy"
        for suffix, policy in rules:
            if host == suffix or host.endswith("." + suffix):
                actual = f"{policy}:{suffix}"
                break
        if actual != expected:
            failures.append(f"{fixture.name}:{number}: {host} expected {expected}, got {actual}")
    if failures:
        print("Rule tests FAILED:")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print(f"Rule tests passed ({sum(1 for line in fixture.read_text(encoding='utf-8').splitlines() if line.strip() and not line.lstrip().startswith('#'))} cases).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"Rule tests FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
