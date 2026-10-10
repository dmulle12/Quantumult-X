#!/usr/bin/env python3
"""Basic structural/safety checks for the repository's Quantumult X profile."""
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

active_filters = sections.get("filter_remote", [])
if len(active_filters) < 4:
    errors.append("expected at least four active remote filter resources")
for line in active_filters:
    if not line.startswith("https://"):
        errors.append(f"active remote filter is not HTTPS: {line}")
    if "example." in line or "YOUR_" in line:
        errors.append(f"placeholder found in active remote filter: {line}")

active_rewrites = sections.get("rewrite_remote", [])
for line in active_rewrites:
    if not line.startswith("https://"):
        errors.append(f"active rewrite entry must be an HTTPS resource URL: {line}")
    if "enabled=false" not in line:
        errors.append(f"rewrite resource must remain disabled by default: {line}")

if not any(line.lower() == "final, proxy" for line in sections.get("filter_local", [])):
    errors.append("[filter_local] must include final, proxy")
if sections.get("server_remote"):
    errors.append("[server_remote] must not contain a real provider URL in the template")
if re.search(r"(?i)(passphrase\s*=\s*\S|p12\s*=\s*\S|https?://[^\s,]+(?:token|secret|password)=)", text):
    errors.append("possible credential or private certificate value found")

if errors:
    print("Configuration validation FAILED:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print("Configuration validation passed.")
print(f"Sections checked: {len(sections)}; active remote filters: {len(active_filters)}; disabled rewrite resources: {len(active_rewrites)}")
