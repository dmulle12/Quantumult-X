# Quantumult-X

A reviewable Quantumult X profile with **project-authored, first-party remote routing rules**, a deterministic configuration builder, an optional privacy blocklist, and safe rewrite examples. The active routing rules are served from this public repository rather than copied into the profile or fetched from a third-party rules provider.

> **Security defaults:** Back up your current profile before importing. No proxy subscription, credentials, MITM private key, or certificate is included. The profile loads two first-party remote filter resources. The optional ad/analytics reject set is not active by default.

## Repository layout

- [`Quantumult-X.conf`](./Quantumult-X.conf): Importable profile; references the project-owned remote rule sets in `[filter_remote]`.
- [`rulesets/proxy-services.list`](./rulesets/proxy-services.list): Curated proxy routes for selected developer, AI, and global content services.
- [`rulesets/direct-cn.list`](./rulesets/direct-cn.list): Curated direct routes for selected mainland China services, followed by a China GeoIP fallback.
- [`rulesets/privacy-reject.optional.list`](./rulesets/privacy-reject.optional.list): Optional ad/analytics blocks; intentionally not active in the default profile.
- [`docs/RULES.md`](./docs/RULES.md): Rule scope, precedence, maintenance, and limitations.
- [`docs/REWRITES.md`](./docs/REWRITES.md): Rewrite/MitM safety notes and the limits of the supplied examples.
- [`snippets/rewrite-examples.snippet`](./snippets/rewrite-examples.snippet): Inactive syntax examples using the reserved `example.invalid` domain only.
- [`tools/build_config.py`](./tools/build_config.py): Validates source lists and generates the profile's remote-resource entries.
- [`tools/validate_config.py`](./tools/validate_config.py) and [`tools/test_rules.py`](./tools/test_rules.py): Structural/safety checks and routing regression tests.

## Quick start

1. Back up your current profile in Quantumult X and import `Quantumult-X.conf`.
2. Make sure Quantumult X can access `raw.githubusercontent.com` so it can download and periodically update the rules. If that host is unavailable on your network, the remote rules may not refresh.
3. Add a subscription from a proxy provider **you trust** in the app. No subscription URL or proxy nodes are supplied here.
4. The profile uses built-in `proxy`, `direct`, and `reject` policies. Its default is selected-domain routing, local-network traffic direct, selected mainland China services and China GeoIP direct, and unmatched traffic through `proxy`.
5. Keep MITM off unless you have reviewed a specific rewrite and understand the certificate's scope.

## Editing and verifying rules

Edit `rulesets/proxy-services.list` or `rulesets/direct-cn.list`, then run:

```bash
python3 tools/build_config.py
python3 tools/build_config.py --check
python3 tools/validate_config.py
python3 tools/test_rules.py
```

The builder generates the `[filter_remote]` resource block; do not edit it by hand. The proxy set is loaded before the direct-China set. The direct set ends with `geoip, cn, direct`, while `[filter_local]` retains only the LAN override and `final, proxy` fallback so local entries do not shadow the remote host rules.

## Scope and limitations

This is an intentionally small, human-reviewable editorial set—not a complete geographic firewall list, GFWList replacement, universal ad blocker, or exhaustive catalog of each service's CDN/API domains. The suffix rules may need adjustment for a particular carrier, app version, or location. A pass in local tests does not prove that every app works; inspect Quantumult X's match/activity logs and disable or change a rule if it causes a problem.

The supported filter-resource syntax follows the official [Quantumult X sample configuration](https://github.com/crossutility/Quantumult-X/blob/master/sample.conf). The active lists are maintained in this repository; they are not synchronized with third-party rules projects.
