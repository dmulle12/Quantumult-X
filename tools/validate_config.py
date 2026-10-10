#!/usr/bin/env python3
"""Validate the importable profile's structure, remote rules, and safe defaults."""
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

expected_remote = [
    (
        "https://raw.githubusercontent.com/dmulle12/Quantumult-X/main/rulesets/proxy-services.list",
        "Project-Proxy",
        "proxy",
    ),
    (
        "https://raw.githubusercontent.com/dmulle12/Quantumult-X/main/rulesets/direct-cn.list",
        "Project-Direct-CN",
        "direct",
    ),
]
remote = sections.get("filter_remote", [])
if len(remote) != len(expected_remote):
    errors.append(f"[filter_remote] must contain exactly {len(expected_remote)} first-party resources")
else:
    resource_pattern = re.compile(
        r"^(https://raw\.githubusercontent\.com/dmulle12/Quantumult-X/main/rulesets/[^,]+), "
        r"tag=([^,]+), force-policy=(proxy|direct), update-interval=(\d+), enabled=(true|false)$"
    )
    for index, (line, expected) in enumerate(zip(remote, expected_remote), 1):
        match = resource_pattern.fullmatch(line)
        if not match:
            errors.append(f"[filter_remote] line {index}: invalid first-party remote resource")
            continue
        url, tag, policy, interval, enabled = match.groups()
        if (url, tag, policy) != expected:
            errors.append(f"[filter_remote] line {index}: expected {expected[0]} with tag={expected[1]} and force-policy={expected[2]}")
        if int(interval) < 3600:
            errors.append(f"[filter_remote] line {index}: update interval must be at least one hour")
        if enabled != "true":
            errors.append(f"[filter_remote] line {index}: first-party rule resource must be enabled")

if sections.get("rewrite_remote"):
    errors.append("[rewrite_remote] must be empty; no external rewrite feeds are allowed by default")
if sections.get("server_remote"):
    errors.append("[server_remote] must not contain a provider subscription in the template")
local = sections.get("filter_local", [])
if local != ["geoip, lan, direct", "final, proxy"]:
    errors.append("[filter_local] must contain only the LAN override and final proxy fallback, in that order")
if any(line.lower() == "geoip, cn, direct" for line in local):
    errors.append("China GeoIP direct fallback must remain remote so it does not shadow remote host rules")
if re.search(r"(?i)(passphrase\s*=\s*\S|p12\s*=\s*\S|https?://[^\s,]+(?:token|secret|password)=)", text):
    errors.append("possible credential or private certificate value found")

if errors:
    print("Configuration validation FAILED:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print("Configuration validation passed.")
print(f"Sections checked: {len(sections)}; first-party remote filter resources: {len(remote)}; remote rewrite resources: 0")
