#!/usr/bin/env python3
"""Exercise first-party LAN CIDR and host-suffix rules against fixture cases."""
from __future__ import annotations

import ipaddress
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_SETS = (
    ("lan.list", "direct"),
    ("back-cn-media.list", "backcn"),
    ("proxy-services.list", "proxy"),
    ("direct-cn.list", "direct"),
)


def load_rules() -> tuple[list[tuple[str, str]], list[ipaddress.IPv4Network | ipaddress.IPv6Network], bool]:
    rules: list[tuple[str, str]] = []
    lan_networks: list[ipaddress.IPv4Network | ipaddress.IPv6Network] = []
    saw_geoip_cn = False
    for filename, required_policy in ACTIVE_SETS:
        path = ROOT / "rulesets" / filename
        active = [
            (number, raw.strip())
            for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
            if raw.strip() and not raw.strip().startswith(("#", ";"))
        ]
        for position, (number, line) in enumerate(active):
            fields = [field.strip().lower() for field in line.split(",")]
            if len(fields) != 3:
                raise ValueError(f"{filename}:{number}: expected three rule fields")
            kind, value, policy = fields
            if policy != required_policy:
                raise ValueError(f"{filename}:{number}: expected policy {required_policy}")
            if kind in {"ip-cidr", "ip6-cidr"}:
                if filename != "lan.list":
                    raise ValueError(f"{filename}:{number}: CIDR rules are only supported in lan.list")
                try:
                    network = ipaddress.ip_network(value, strict=True)
                except ValueError as exc:
                    raise ValueError(f"{filename}:{number}: invalid CIDR {value!r}") from exc
                expected_version = 4 if kind == "ip-cidr" else 6
                if network.version != expected_version:
                    raise ValueError(f"{filename}:{number}: {kind} has the wrong IP version")
                lan_networks.append(network)
                continue
            if kind == "geoip":
                if filename != "direct-cn.list" or value != "cn" or position != len(active) - 1:
                    raise ValueError(f"{filename}:{number}: geoip, cn, direct must be the final remote rule")
                saw_geoip_cn = True
                continue
            if kind != "host-suffix":
                raise ValueError(f"{filename}:{number}: unsupported test rule: {line}")
            rules.append((value, policy))
    if not lan_networks:
        raise ValueError("lan.list must contain active CIDR rules")
    if not saw_geoip_cn:
        raise ValueError("direct-cn.list must end with geoip, cn, direct")
    return rules, lan_networks, saw_geoip_cn


def main() -> int:
    rules, lan_networks, has_geoip_cn = load_rules()
    failures: list[str] = []
    fixture = ROOT / "tests" / "rule-cases.tsv"
    for number, raw in enumerate(fixture.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split(chr(9))
        if len(fields) != 3:
            failures.append(f"{fixture.name}:{number}: expected host, network, and expected-result fields")
            continue
        host, network, expected = fields[0].lower(), fields[1].lower(), fields[2]
        if network == "lan":
            try:
                address = ipaddress.ip_address(host)
            except ValueError:
                failures.append(f"{fixture.name}:{number}: LAN cases must use a literal IP address")
                continue
            actual = "direct:lan" if any(address in cidr for cidr in lan_networks) else "final:proxy"
        elif network in {"cn", "other"}:
            actual = None
            for suffix, policy in rules:
                if host == suffix or host.endswith("." + suffix):
                    actual = f"{policy}:{suffix}"
                    break
            if actual is None:
                if network == "cn" and has_geoip_cn:
                    actual = "direct:geoip-cn"
                else:
                    actual = "final:proxy"
        else:
            failures.append(f"{fixture.name}:{number}: network must be 'cn', 'other', or 'lan'")
            continue
        if actual != expected:
            failures.append(f"{fixture.name}:{number}: {host} expected {expected}, got {actual}")
    if failures:
        print("Rule tests FAILED:")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    cases = sum(1 for line in fixture.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#"))
    print(f"Rule tests passed ({cases} host/network cases; LAN CIDR, service precedence, and GeoIP fallback order checked).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"Rule tests FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
