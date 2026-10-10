# First-Party Rule Sets

## What is active

The importable profile embeds the two rule sources below in `[filter_local]`. They are authored and maintained in this repository; no external filter resource is loaded.

| Source | Policy | Scope |
|---|---|---|
| [`proxy-services.list`](../rulesets/proxy-services.list) | `proxy` | Selected developer, AI, and global content-service domains |
| [`direct-cn.list`](../rulesets/direct-cn.list) | `direct` | Selected mainland China service domains |

The domains are hand-curated, conservative suffix matches. They are not copied from or synchronized with a public blocklist, and they are **not exhaustive**. The optional [`privacy-reject.optional.list`](../rulesets/privacy-reject.optional.list) is not embedded and has no effect unless you deliberately copy selected entries into `[filter_local]`.

## Match order

The profile evaluates its local rules in this order:

1. Selected proxy-service suffixes (`proxy-services.list`).
2. Selected mainland service suffixes (`direct-cn.list`).
3. `geoip, lan, direct`.
4. `geoip, cn, direct`.
5. `final, proxy` for unmatched traffic.

Quantumult X processes filter rules in order. Keep specific exceptions before broader matches. A `host-suffix` entry matches the listed domain and its subdomains, not merely strings that happen to end with the same characters; for example, `github.com.attacker.invalid` is not a match for `github.com`.

## Optional privacy blocks

The optional reject list includes ad and analytics domains that may also be used by site features, attribution, or embedded content. Blocking them can cause breakage. It is deliberately excluded from the generated default profile. If you choose to use an entry, review it first and add it above `final, proxy` in `[filter_local]`; rebuild and run the checks afterward.

## Change and test

1. Add or remove a three-column Quantumult X rule in the relevant `.list` file, following the existing `host-suffix, domain, policy` form.
2. Keep proxy-service rules ahead of direct-service rules when precedence matters. Avoid broad `host-keyword` matches and speculative top-level domains.
3. Run `python3 tools/build_config.py` to update the generated section of `Quantumult-X.conf`.
4. Run `python3 tools/build_config.py --check`, `python3 tools/validate_config.py`, and `python3 tools/test_rules.py`.
5. Import the profile and confirm the effective policy in Quantumult X's match/activity logs.

The regression cases in [`../tests/rule-cases.tsv`](../tests/rule-cases.tsv) cover known examples, suffix boundaries, and the fallback. They do not substitute for app-level or network testing. Do not add a provider subscription, private credentials, or MITM certificate material to this repository.
