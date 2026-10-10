# First-Party Remote Rule Sets

## What is active

The importable profile references two rule sources from this public repository in `[filter_remote]`. They are authored and maintained here; no third-party filter feed is loaded.

| Source | Forced policy | Scope |
|---|---|---|
| [`proxy-services.list`](../rulesets/proxy-services.list) | `proxy` | Selected developer, AI, and global content-service domains |
| [`direct-cn.list`](../rulesets/direct-cn.list) | `direct` | Selected mainland China service domains, then the China GeoIP fallback |

Quantumult X's `force-policy` parameter makes the resource use the configured policy. The optional [`privacy-reject.optional.list`](../rulesets/privacy-reject.optional.list) is not loaded and has no effect unless you deliberately configure it.

## Match order and priority

The active profile is arranged as follows:

1. `[filter_local]`: `geoip, lan, direct` for local-network traffic.
2. `[filter_remote]`: selected proxy-service suffixes.
3. `[filter_remote]`: selected mainland-China service suffixes.
4. The final rule in the direct-China resource: `geoip, cn, direct`.
5. `final, proxy` for unmatched traffic.

Quantumult X checks local filters before remote filters, with `final` as the fallback after those rules. For this reason, the China GeoIP rule is kept in the last remote resource instead of `[filter_local]`; otherwise, it could match before and shadow the explicit remote host rules. The project resources are listed proxy first, direct second, and the GeoIP fallback last.

A `host-suffix` entry matches the listed domain and its subdomains, not merely strings that happen to end with the same characters; for example, `github.com.attacker.invalid` is not a match for `github.com`.

## Optional privacy blocks

The optional reject list includes ad and analytics domains that may also be used by site features, attribution, or embedded content. Blocking them can cause breakage. It is deliberately excluded from the profile. If you choose to use an entry, review it first and configure it as a separate remote resource or add selected entries to `[filter_local]`; rebuild and run the checks afterward.

## Change and test

1. Add or remove a three-column Quantumult X rule in the relevant `.list` file, following the existing `host-suffix, domain, policy` form. Keep `geoip, cn, direct` as the final active rule in `direct-cn.list`.
2. Keep proxy-service rules in the first remote set and direct-service rules in the second. Avoid broad `host-keyword` matches and speculative top-level domains.
3. Run `python3 tools/build_config.py` to update the generated remote-resource block in `Quantumult-X.conf`.
4. Run `python3 tools/build_config.py --check`, `python3 tools/validate_config.py`, and `python3 tools/test_rules.py`.
5. Ensure the repository changes are published before importing the profile, then update the remote resources in Quantumult X and confirm effective policies in its match/activity logs.

The remote lists are served from `raw.githubusercontent.com`; Quantumult X needs network access to that host to download or update them. The regression cases in [`../tests/rule-cases.tsv`](../tests/rule-cases.tsv) cover known host examples, suffix boundaries, fallback behavior, and validate that the China GeoIP rule remains last. They do not substitute for app-level or network testing. Do not add a provider subscription, private credentials, or MITM certificate material to this repository.

For resource syntax and parameters, see the official [Quantumult X sample configuration](https://github.com/crossutility/Quantumult-X/blob/master/sample.conf).
