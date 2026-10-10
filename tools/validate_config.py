#!/usr/bin/env python3
"""Validate the importable profile's structure, first-party rules, and safe defaults."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "Quantumult-X.conf"
text = CONFIG.read_text(encoding="utf-8")
errors: list[str] = []
sections: dict[str, list[str]] = {}
current = None
for number, raw in enumerate(text.splitlines(), 1):
    line = raw.strip()
    if not line or line.startswith((";", "#", "//")):
        continue
    match = re.fullmatch(r"\[([^]]+)\]", line)
    if match:
        current = match.group(1).lower()
        if current in sections:
            errors.append(f"line {number}: duplicate section [{current}]")
        sections.setdefault(current, [])
        continue
    if current is None:
        errors.append(f"line {number}: content before first section")
    else:
        sections[current].append(line)

required = {"general", "dns", "policy", "server_remote", "filter_remote", "rewrite_remote", "filter_local", "rewrite_local", "mitm"}
missing = sorted(required - sections.keys())
if missing:
    errors.append("missing sections: " + ", ".join(f"[{name}]" for name in missing))

if sections.get("filter_remote"):
    errors.append("[filter_remote] must be empty; use first-party rulesets embedded in the profile")
if sections.get("rewrite_remote"):
    errors.append("[rewrite_remote] must be empty; no external rewrite feeds are allowed by default")
if sections.get("server_remote"):
    errors.append("[server_remote] must not contain a provider subscription in the template")
if not any(line.lower() == "final, proxy" for line in sections.get("filter_local", [])):
    errors.append("[filter_local] must include final, proxy")
if not any(line.lower() == "geoip, lan, direct" for line in sections.get("filter_local", [])):
    errors.append("[filter_local] must include geoip, lan, direct")
if not any(line.lower() == "geoip, cn, direct" for line in sections.get("filter_local", [])):
    errors.append("[filter_local] must include geoip, cn, direct")
if re.search(r"(?i)(passphrase\s*=\s*\S|p12\s*=\s*\S|https?://[^\s,]+(?:token|secret|password)=)", text):
    errors.append("possible credential or private certificate value found")
if "github.com/dmulle12/rules" in text:
    errors.append("third-party dmulle12/rules dependency remains in the main profile")

if errors:
    print("Configuration validation FAILED:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print("Configuration validation passed.")
print(f"Sections checked: {len(sections)}; remote filter resources: 0; remote rewrite resources: 0")
