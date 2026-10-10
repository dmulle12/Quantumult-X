# Quantumult-X

A reviewable Quantumult X profile with **project-authored, first-party routing rules**, a deterministic build step, an optional privacy blocklist, and safe rewrite examples. The profile does not download routing rules or app rewrites from third-party feeds.

> **Security defaults:** Back up your current profile before importing. No proxy subscription, credentials, MITM private key, or certificate is included. Remote rule and rewrite sections are empty. The optional ad/analytics reject set is not active by default.

## Repository layout

- [`Quantumult-X.conf`](./Quantumult-X.conf): Importable profile; active project rules are embedded in `[filter_local]`.
- [`rulesets/proxy-services.list`](./rulesets/proxy-services.list): Curated first-party proxy routes for selected developer, AI, and global content services.
- [`rulesets/direct-cn.list`](./rulesets/direct-cn.list): Curated first-party direct routes for selected mainland China services.
- [`rulesets/privacy-reject.optional.list`](./rulesets/privacy-reject.optional.list): Optional ad/analytics blocks; intentionally not included in the default profile.
- [`docs/RULES.md`](./docs/RULES.md): Rule scope, precedence, maintenance, and limitations.
- [`docs/REWRITES.md`](./docs/REWRITES.md): Rewrite/MitM safety notes and the limits of the supplied examples.
- [`snippets/rewrite-examples.snippet`](./snippets/rewrite-examples.snippet): Inactive syntax examples using the reserved `example.invalid` domain only.
- [`tools/build_config.py`](./tools/build_config.py): Embeds active rule sources into the importable profile.
- [`tools/validate_config.py`](./tools/validate_config.py) and [`tools/test_rules.py`](./tools/test_rules.py): Structural/safety checks and routing regression tests.

## Quick start

1. Back up your current profile in Quantumult X and import `Quantumult-X.conf`.
2. Add a subscription from a proxy provider **you trust** in the app. No subscription URL or proxy nodes are supplied here.
3. The profile uses built-in `proxy`, `direct`, and `reject` policies. Its default is selected-domain routing, mainland China IPs direct, LAN direct, and all unmatched traffic through `proxy`.
4. If your region or needs differ, edit the first-party files in `rulesets/`, rebuild the profile, and verify matching in Quantumult X before relying on it.
5. Keep MITM off unless you have reviewed a specific rewrite and understand the certificate's scope.

## Editing and verifying rules

Edit `rulesets/proxy-services.list` or `rulesets/direct-cn.list`, then run:

```bash
python3 tools/build_config.py
python3 tools/build_config.py --check
python3 tools/validate_config.py
python3 tools/test_rules.py
```

The config's generated block must not be edited by hand. The builder and CI ensure it stays synchronized with the first-party sources.

## Scope and limitations

This is an intentionally small, human-reviewable editorial set—not a complete geographic firewall list, GFWList replacement, universal ad blocker, or exhaustive catalog of each service's CDN/API domains. The suffix rules may need adjustment for a particular carrier, app version, or location. A pass in local tests does not prove that every app works; inspect Quantumult X's match/activity logs and disable or change a rule if it causes a problem.

The supported rule syntax follows the official [Quantumult X sample configuration](https://github.com/crossutility/Quantumult-X/blob/master/sample.conf). All domain lists in this repository are maintained here rather than fetched from an upstream rules project.
